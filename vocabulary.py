#!/usr/bin/python

from collections import defaultdict, Counter
import numpy as n
import os
import itertools

def vocabulary(dict, topN):

    csail = list()
    lids = list()
    rle = list()
    unk = list()
    mtl = list()
    x1 = list()
    x2 = list()
    x3 = list()
    x4 = list()
    x5 = list()


    for k, v in dict.items():
        if v[9] == 'CSAIL':
            for i in range(len(v[8])):
                csail.append(v[8][i])
        elif v[9] == 'LIDS':
            for i in range(len(v[8])):
                lids.append(v[8][i])
        elif v[9] == 'RLE':
            for i in range(len(v[8])):
                rle.append(v[8][i])
        elif v[9] == 'UNK':
            for i in range(len(v[8])):
                unk.append(v[8][i])
        elif v[9] == 'MTL':
            for i in range(len(v[8])):
                mtl.append(v[8][i])
    csailCount = Counter(csail)
    lidsCount = Counter(lids)
    rleCount = Counter(rle)
    unkCount = Counter(unk)
    mtlCount = Counter(mtl)


    for k, v in csailCount.most_common(topN):
        x1.append(k)
    for k, v in lidsCount.most_common(topN):
        x2.append(k)
    for k, v in rleCount.most_common(topN):
        x3.append(k)
    for k, v in unkCount.most_common(topN):
        x4.append(k)
    for k, v in mtlCount.most_common(topN):
        x5.append(k)

    vocab = Counter(itertools.chain(x1, x2, x3, x4, x5))
    print('Vocabulary: ', type(vocab), len(vocab), vocab)

    return vocab