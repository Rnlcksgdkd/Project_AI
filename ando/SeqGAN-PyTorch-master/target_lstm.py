# -*- coding: utf-8 -*-

import os
import random

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class TargetLSTM(nn.Module):
    """Target Lstm """
    def __init__(self, num_emb, emb_dim, hidden_dim, use_cuda):
        super(TargetLSTM, self).__init__()
        self.num_emb = num_emb
        self.emb_dim = emb_dim
        self.hidden_dim = hidden_dim
        self.use_cuda = use_cuda
        self.emb = nn.Embedding(num_emb, emb_dim)
        self.lstm = nn.LSTM(emb_dim, hidden_dim, batch_first=True)
        self.lin = nn.Linear(hidden_dim, num_emb)
        self.softmax = nn.LogSoftmax()
        self.init_params()

    def forward(self, x):
        """
        Args:
            x: (batch_size, seq_len), sequence of tokens generated by generator
        """
        emb = self.emb(x)
        h0, c0 = self.init_hidden(x.size(0))
        output, (h, c) = self.lstm(emb, (h0, c0))
        pred = self.softmax(self.lin(output.contiguous().view(-1, self.hidden_dim)))
        return pred

    def step(self, x, h, c):
        """
        Args:
            x: (batch_size,  1), sequence of tokens generated by generator
            h: (1, batch_size, hidden_dim), lstm hidden state
            c: (1, batch_size, hidden_dim), lstm cell state
        """
        emb = self.emb(x)
        output, (h, c) = self.lstm(emb, (h, c))
        pred = F.softmax(self.lin(output.view(-1, self.hidden_dim)), dim=1)
        return pred, h, c


    def init_hidden(self, batch_size):
        h = Variable(torch.zeros((1, batch_size, self.hidden_dim)))
        c = Variable(torch.zeros((1, batch_size, self.hidden_dim)))
        if self.use_cuda:
            h, c = h.cuda(), c.cuda()
        return h, c

    def init_params(self):
        for param in self.parameters():
            param.data.normal_(0, 1)

    def sample(self, batch_size, seq_len):
        res = []
        with torch.no_grad():
            x = Variable(torch.zeros((batch_size, 1)).long())
            if self.use_cuda:
                x = x.cuda()
            h, c = self.init_hidden(batch_size)
            samples = []
            for i in range(seq_len):
                output, h, c = self.step(x, h, c)
                x = output.multinomial(1)
                samples.append(x)
            output = torch.cat(samples, dim=1)
            return output
        return None
