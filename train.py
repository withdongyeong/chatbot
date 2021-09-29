import os
import pickle
import random
from collections import Counter, defaultdict

import numpy as np
import torch
from torch import nn
from torch.autograd import Variable
import torch.nn.functional as F
from torch.utils.data import random_split, DataLoader

import customDataset

# 파라미터 설정
from nlpModel import LSTM

from konlpy.tag import Komoran

# 롤 0
# 오버워치 1
# 배그 2
# 로스트아크 3
custom_encoidng = {
    0: '롤',
    1: '오버워치',
    2: '배틀그라운드',
    3: '로스트아크'
}

# Sequence Length를 맞추기 위한 padding
def add_padding(token_ls, max_len):
    pad = '<PAD>'
    seq_length_ls = []

    for i, tokens in enumerate(token_ls):
        seq_length = len(tokens)

        # 짧으면 padding을 추가
        if seq_length < max_len:
            seq_length_ls.append(max_len)
            token_ls[i] += [pad] * (max_len - seq_length)

        # 길이가 길면, max_len까지의 token만 사용
        elif seq_length >= max_len:
            seq_length_ls.append(max_len)
            token_ls[i] = tokens[:max_len]

    return token_ls, seq_length_ls

# 단어에 대한 idx 부여
def convert_token_to_idx_from_dict(token_ls, dict):
    for tokens in token_ls:
        yield [dict[token] if token in dict else 0 for token in tokens]
    return

# 단어에 대한 idx 부여
def conver_token_to_idx_for_make_dict(token_ls, dict):
    for tokens in token_ls:
        yield [dict[token] for token in tokens]
    return

def sort_by_sequence_length(x, y, seq_len):
    sorted_idx = np.argsort(np.array(seq_len))[::-1]

    x = Variable(torch.LongTensor(np.array(x)[sorted_idx]))
    y = Variable(torch.LongTensor(np.array(y)[sorted_idx]))
    seq_len = Variable(torch.LongTensor(np.array(seq_len)[sorted_idx]))

    return x, y, seq_len

def train():
    dataPath = "./train"
    batch_size = 4
    train_ratio = 0.8
    epochs = 100
    lr = 0.01
    # 토크나이저 쓸지, 그냥 띄어쓰기로 단어 분리할지 결정
    useTokenizer = True

    # 데이터셋을 만들고, 학습 및 테스트 데이터셋으로 분리
    # 데이터셋 만들기
    print("-" * 10)
    print("start making dataset and vocabulary with ", dataPath)
    dataset = customDataset.textDataset(dataPath)

    # random_split 함수를 통해 dataset을 비율을 맞춰 2개의 Subset으로 분리함
    num_train = int(len(dataset) * train_ratio)
    train_dataset, test_dataset = \
        random_split(dataset, [num_train, len(dataset) - num_train])

    # data loader 정의
    dataLoader_train = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
    dataLoader_test = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    print("finished making dataset and vocabulary with ", dataPath)
    print("-"*10)

    x_train, y_train, x_test, y_test = [], [], [], []
    tokenizer = Komoran()

    for labels, txts in dataLoader_train:
        for label in labels:
            y_train.append(int(label))
        for txt in txts:
            if useTokenizer:
                # print(type(txt))
                x_train.append(tokenizer.morphs(txt))
            else:
                x_train.append(txt.split(" "))

    for labels, txts in dataLoader_test:
        for label in labels:
            y_test.append(int(label))
        for txt in txts:
            if useTokenizer:
                x_test.append(tokenizer.morphs(txt))
            else:
                x_test.append(txt.split(" "))

    max_sequence_length = 20
    x_train, x_train_seq_length = add_padding(x_train, max_sequence_length)
    x_test, x_test_seq_length = add_padding(x_test, max_sequence_length)

    # pad는 0으로 지정
    token2idx = defaultdict(lambda: len(token2idx))
    token2idx['<PAD>'] = 0

    x_train = list(conver_token_to_idx_for_make_dict(x_train, token2idx))
    x_test = list(conver_token_to_idx_for_make_dict(x_test, token2idx))

    idx2token = {val : key for key,val in token2idx.items()}

    # save dict
    with open('chatbot.pickle', 'wb') as fw:
        pickle.dump(idx2token, fw)

    x_train, y_train, x_train_seq_length = sort_by_sequence_length(x_train, y_train, x_train_seq_length)
    x_test, y_test, x_test_seq_length = sort_by_sequence_length(x_test, y_test, x_test_seq_length)

    model = LSTM(
        token2idx = token2idx,
        max_sequence = max_sequence_length,
        vocab_size = len(token2idx),
        embed_size = 32,
        hid_size = 32,
        n_layers = 2,
        dropout = 0.2,
        bidirectional = True,
        n_category = 6
    )

    def adjust_learning_rate(optimizer, epoch, init_lr=0.001, lr_decay_epoch=10):
        """Decay learning rate by a factor of 0.1 every lr_decay_epoch epochs."""
        lr = init_lr * (0.1**(epoch // lr_decay_epoch))

        if epoch % lr_decay_epoch == 0:
            print('LR is set to %s'%(lr))

        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

        return optimizer


    train_idx = np.arange(x_train.size(0))
    test_idx = np.arange(x_test.size(0))
    optimizer = torch.optim.Adam(model.parameters(), lr)
    criterion = nn.CrossEntropyLoss(reduction='sum')

    loss_ls = []

    acc = 0
    best_acc = 0
    for epoch in range(1, epochs + 1):
        model.train()

        # input 데이터 순서 섞기
        random.shuffle(train_idx)
        x_train, y_train = x_train[train_idx], y_train[train_idx]
        x_train_seq_length = x_train_seq_length[train_idx]

        train_loss = 0

        for start_idx, end_idx in zip(range(0, x_train.size(0), batch_size),
                                      range(batch_size, x_train.size(0) + 1, batch_size)):
            # batch 뽑기
            x_batch = x_train[start_idx: end_idx]
            y_batch = y_train[start_idx: end_idx].long()
            x_batch_seq_length = x_train_seq_length[start_idx: end_idx]

            # sequence 순서대로 정렬하기
            x_batch, y_batch, x_batch_seq_length = sort_by_sequence_length(x_batch, y_batch, x_batch_seq_length)
            # print(idx2token)
            # print(x_batch)
            # print(x_batch_seq_length)
            # print(y_batch)
            # exit()
            scores = model(x_batch, x_batch_seq_length)
            predict = F.softmax(scores, dim=1).argmax(dim=1)

            acc = (predict == y_batch).sum().item() / batch_size

            loss = criterion(scores, y_batch)
            train_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print('Train epoch : %s,  loss : %s,  accuracy :%.3f' % (epoch, train_loss / batch_size, acc))
        print('=================================================================================================')

        loss_ls.append(train_loss)
        optimizer = adjust_learning_rate(optimizer, epoch, lr, 10)  # adjust learning_rate while training

        if (epoch) % 3 == 0:
            model.eval()
            scores = model(x_test, x_test_seq_length)
            predict = F.softmax(scores, dim=1).argmax(dim=1)
            acc = (predict == y_test.long()).sum().item() / y_test.size(0)
            loss = criterion(scores, y_test.long())

            if acc >= best_acc:
                best_acc = acc
                print("best_acc updated(saved)", best_acc)
                pathDir = "./runs"
                if not os.path.isdir(pathDir):
                    os.mkdir(pathDir)
                torch.save(model.state_dict(), pathDir + os.path.sep + "best_"+ '%.3f'% best_acc + ".pth")

            print('*************************************************************************************************')
            print('*************************************************************************************************')
            print('Test Epoch : %s, Test Loss : %.03f , Test Accuracy : %.03f' % (epoch, loss.item() / y_test.size(0), acc))
            print('*************************************************************************************************')
            print('*************************************************************************************************')

def predict(text, label):
    max_sequence_length = 20
    useTokenizer = True
    # load dict
    with open('chatbot.pickle', 'rb') as fr:
        idx2token = pickle.load(fr)

    token2idx = {val: key for key, val in idx2token.items()}
    targetLabel = [label]
    if useTokenizer:
        target = [Komoran().morphs(text)]
    else:
        target = [text.split(" ")]

    target, target_seq_length = add_padding(target, max_sequence_length)
    target_seq_length = [max_sequence_length]
    target = list(convert_token_to_idx_from_dict(target, token2idx))
    target = Variable(torch.LongTensor(np.array(target)))
    y_train = Variable(torch.LongTensor(np.array(targetLabel)))
    target_seq_length = Variable(torch.LongTensor(np.array(target_seq_length)))

    model = LSTM(
        token2idx=token2idx,
        max_sequence=max_sequence_length,
        vocab_size=len(token2idx),
        embed_size=32,
        hid_size=32,
        n_layers=2,
        dropout=0.5,
        bidirectional=True,
        n_category=6
    )
    loadPath = "./predict_model.pth"
    model.load_state_dict(torch.load(loadPath))
    model.eval()

    scores = model(target, target_seq_length)
    predict = F.softmax(scores, dim=1).argmax(dim=1)
    score = F.softmax(scores, dim=1).squeeze().detach().numpy()[predict.item()]

    return predict.item(), score

if __name__ == "__main__" :
    # train
    # train()

    # predict
    predict("안녕", 0)


