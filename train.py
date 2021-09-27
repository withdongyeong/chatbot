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

dataPath = "./test"
batch_size = 1000
train_ratio = 0.8
epochs = 5
lr = 0.01

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
        x_train.append([' '.join(tokenizer.morphs(txt))])
        # x_train.append([txt])

print(x_train)
print(y_train)

for labels, txts in dataLoader_test:
    for label in labels:
        y_test.append(int(label))
    for txt in txts:
        x_test.append([txt])

print(x_test)
print(y_test)

# Sequence Length를 맞추기 위한 padding
def add_padding(token_ls, max_len):
    pad = '<PAD>'
    seq_length_ls = []

    for i, tokens in enumerate(token_ls):
        seq_length = len(tokens)

        # 짧으면 padding을 추가
        if seq_length < max_len:
            seq_length_ls.append(seq_length)
            token_ls[i] += [pad] * (max_len - seq_length)

        # 길이가 길면, max_len까지의 token만 사용
        elif seq_length >= max_len:
            seq_length_ls.append(max_len)
            token_ls[i] = tokens[:max_len]

    return token_ls, seq_length_ls

max_sequence_length = 30
x_train, x_train_seq_length = add_padding(x_train, max_sequence_length)
x_test, x_test_seq_length = add_padding(x_test, max_sequence_length)


# Sequence Length를 맞추기 위한 padding
def add_padding(token_ls, max_len):
    pad = '<PAD>'
    seq_length_ls = []

    for i, tokens in enumerate(token_ls):
        seq_length = len(tokens)

        # 짧으면 padding을 추가
        if seq_length < max_len:
            seq_length_ls.append(seq_length)
            token_ls[i] += [pad] * (max_len - seq_length)

        # 길이가 길면, max_len까지의 token만 사용
        elif seq_length >= max_len:
            seq_length_ls.append(max_len)
            token_ls[i] = tokens[:max_len]

    return token_ls, seq_length_ls

max_sequence_length = 30
x_train, x_train_seq_length = add_padding(x_train, max_sequence_length)
x_test, x_test_seq_length = add_padding(x_test, max_sequence_length)

# 단어에 대한 idx 부여
def convert_token_to_idx(token_ls):
    for tokens in token_ls:
        yield [token2idx[token] for token in tokens]
    return

token2idx = defaultdict(lambda: len(token2idx))
pad = token2idx['<PAD>']

x_train = list(convert_token_to_idx(x_train))
x_test = list(convert_token_to_idx(x_test))

idx2token = {val : key for key,val in token2idx.items()}

print(' '.join([idx2token[x] for x in x_train[0]]))


def sort_by_sequence_length(x, y, seq_len):
    sorted_idx = np.argsort(np.array(seq_len))[::-1]

    x = Variable(torch.LongTensor(np.array(x)[sorted_idx]))
    y = Variable(torch.LongTensor(np.array(y)[sorted_idx]))
    seq_len = Variable(torch.LongTensor(np.array(seq_len)[sorted_idx]))

    return x, y, seq_len

x_train, y_train, x_train_seq_length = sort_by_sequence_length(x_train, y_train, x_train_seq_length)
x_test, y_test, x_test_seq_length = sort_by_sequence_length(x_test, y_test, x_test_seq_length)

model = LSTM(
    token2idx = token2idx,
    max_sequence = 30,
    vocab_size = len(token2idx),
    embed_size = 32,
    hid_size = 32,
    n_layers = 2,
    dropout = 0.5,
    bidirectional = True,
    n_category = 15
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

    if (epoch) % 5 == 0:
        model.eval()
        scores = model(x_test, x_test_seq_length)
        predict = F.softmax(scores, dim=1).argmax(dim=1)
        acc = (predict == y_test.long()).sum().item() / y_test.size(0)
        loss = criterion(scores, y_test.long())

        print('*************************************************************************************************')
        print('*************************************************************************************************')
        print('Test Epoch : %s, Test Loss : %.03f , Test Accuracy : %.03f' % (epoch, loss.item() / y_test.size(0), acc))
        print('*************************************************************************************************')
        print('*************************************************************************************************')