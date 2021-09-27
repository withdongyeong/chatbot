import torch
from torch import nn
from torch.autograd import Variable


class LSTM(nn.Module):
    def __init__(self, token2idx, max_sequence, vocab_size, embed_size, hid_size, n_layers, dropout, bidirectional,
                 n_category):
        super(LSTM, self).__init__()
        self.vocab_size = vocab_size  # 고유한 단어의 수
        self.embed_size = embed_size  # 임베딩 차원의 크기
        self.padding_index = token2idx['<PAD>']  # 패딩 토큰

        self.embed = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embed_size,
            padding_idx=self.padding_index
        )

        self.max_sequence = max_sequence  # 한 문장의 최대 길이
        self.hid_size = hid_size  # LSTM 뉴런의 갯수
        self.n_layers = n_layers  # LSTM layer의 수
        self.drouput = dropout  # 드롭아웃
        self.n_category = n_category  # 분류 카테고리 갯수
        self.bidirectional = bidirectional  # optinal, True : bidirectional

        self.lstm = nn.LSTM(embed_size, hid_size, n_layers, batch_first=True, bidirectional=True)

        if bidirectional:
            input_dim = 2 * hid_size * max_sequence
        else:
            input_dim = hid_size * max_sequence

        self.lin = nn.Linear(input_dim, n_category)
        self.outputs = []

    def init_hidden(self, batch_size):
        # 최초에 h_0와 c_0의 초기값 부여 (n_layers, batch_size, hid_size(n_neuron))
        # bidirectional일 경우, (2*n_layers, batch_size, hid_size)
        if self.bidirectional:
            h_0 = Variable(torch.randn(2 * self.n_layers, batch_size, self.hid_size)) * 0.1
            c_0 = Variable(torch.randn(2 * self.n_layers, batch_size, self.hid_size)) * 0.1
        else:
            h_0 = Variable(torch.randn(self.n_layers, batch_size, self.hid_size)) * 0.1
            c_0 = Variable(torch.randn(self.n_layers, batch_size, self.hid_size)) * 0.1
        return (h_0, c_0)

    def forward(self, x, x_sequence_length):
        # init h randomly
        batch_size = x.size(0)
        self.h_c = self.init_hidden(batch_size)

        # embedding
        x = self.embed(x)  # sequence_length(max_len), batch_size, embed_size

        # packing for LSTM
        x = torch.nn.utils.rnn.pack_padded_sequence(x, x_sequence_length, batch_first=True)

        # LSTM
        output, self.h_c = self.lstm(x, self.h_c)

        # unpack
        # unpacking 과정에서, size(1) S가 가장 긴 sequence 길이를 갖는 data에 맞춰진다.
        # S가 max_sequence_length로 고정되는 것이 아님을 주의
        x, _ = torch.nn.utils.rnn.pad_packed_sequence(output, batch_first=True)
        # print(x.shape)

        # flatten
        x = x.contiguous()
        x = x.view(batch_size, -1)

        # fully-connect
        logit = self.lin(x)

        return logit