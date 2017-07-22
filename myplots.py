#!/usr/bin/python

from matplotlib import pyplot as plt
from collections import defaultdict, Counter
import numpy as n
import os


def plotAbstracts(dict):
    l2 = list()
    for k, v in dict.items():
        l2.append(v[2][0])
    print(l2)
    yearCount = Counter(l2)
    count = 0
    y2 = Counter()
    for k, v in yearCount.items():
        if int(k) < 2010:
            count += v
            continue
        y2[k] = v
    y2['2009'] = count
    years = list(map(int, list(yearCount.keys())))
    absCount = list(map(int, list(yearCount.values())))

# plot 1
    fig = plt.figure()
    ax = fig.add_subplot(1,2,1)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.minorticks_on()
    plt.xlim(1990, 2018, 1)
    plt.ylim(0, 300, 5)

    Colors = 'rgbkmc'
    ax.bar(years, absCount, align='center',width=0.5, color=Colors)
    ax.set_xlabel('Year \n Fig: 1')
    ax.set_ylabel('Number of Abstracts')
    plt.title('MIT EECS: Number of arXiv Abstracts by Year')
    plt.axvline(2009, linewidth=2.0, ls='--', color='red')
#     plt.show()
# plot 2
    y3 = list(map(int, list(y2.keys())))
    abs3 = list(map(int, list(y2.values())))


    ax1 = fig.add_subplot(1, 2, 2)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.minorticks_on()
    plt.xlim(2008, 2018, 1)
    plt.ylim(0, 300, 10)

    Colors = 'rgbkmc'
    ax1.bar(y3, abs3, align='center',width=0.5, color=Colors)
    ax1.set_xlabel('Year \n Fig: 2')


    plt.title('MIT EECS: Groups for Analysis\n (Fig 2: 2009 is sum of all prior) ')

    plt.show()


def plotDepartments(dict):

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    x1 = list()
    y1 = list()
    l2 = list()
    for k, v in dict.items():
        l2.append(v[9])
    deptCount = Counter(l2)
    # plot 1
    for k, v in deptCount.items():
        x1.append(k)
        y1.append(v)

    print('x1: ', x1)
    print('y1: ', y1)
    x = n.arange(len(deptCount))
    print('x: ', x)

    y = deptCount.values()
    print('y: ', y)

    Colors = 'rgbkm'
    width = 0.35
    fig, ax = plt.subplots()
    chart = ax.bar(x , y1, width, color=Colors)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of Abstracts by Department')
    ax.set_xlabel('Fig 3: MIT EECS Departments ')
    ax.set_title('MIT EECS: Number of Articles by Department')
    ax.set_xticklabels(['','CSAIL', 'LIDS', 'RLE', 'UNK', 'MTL'])

    # plt.xticks(x + 0.5, data.keys(), rotation='vertical')
    # plt.show()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(0, 600, 10)
    #ax.set_xticklabels(list(deptCount.keys()))
    autolabel(chart)
    plt.show()

def plotWordCountByDepartment(dict):
    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    x = list()
    y = list()
    x1 = list()
    y1 = list()
    x2 = list()
    y2 = list()
    x3 = list()
    y3 = list()
    x4 = list()
    y4 = list()
    x5 = list()
    y5 = list()

    csail = list()
    lids = list()
    rle = list()
    unk = list()
    mtl = list()

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

    for k, v in csailCount.most_common(5):
        x1.append(k)
        y1.append(v)
    for k, v in lidsCount.most_common(5):
        x2.append(k)
        y2.append(v)
    for k, v in rleCount.most_common(5):
        x3.append(k)
        y3.append(v)
    for k, v in unkCount.most_common(5):
        x4.append(k)
        y4.append(v)
    for k, v in mtlCount.most_common(5):
        x5.append(k)
        y5.append(v)

    for i in range(0,5):
        x.append(x1[i])
        y.append(y1[i])
        x.append(x2[i])
        y.append(y2[i])
        x.append(x3[i])
        y.append(y3[i])
        x.append(x4[i])
        y.append(y4[i])
        x.append(x5[i])
        y.append(y5[i])

    N = 10
    width = 0.4  # the width of the bars

    ind = n.arange(N)
    ind2 = n.arange(0, N, width) # the x locations for the groups
    xcsail = [x for x in ind if (x/0.4) % 5 == 0]
    xlids = n.array(xcsail) + 0.4
    xrle = n.array(xlids) + 0.4
    xunk = n.array(xrle) + 0.4
    xmtl = n.array(xunk) + 0.4

    fig, ax = plt.subplots()
    csailChart = ax.bar(xcsail , y1, width, color='r')
    lidsChart = ax.bar(xlids, y2, width, color='g')
    rleChart = ax.bar(xrle, y3, width, color='b')
    unkChart = ax.bar(xunk, y4, width, color='k')
    mtlChart = ax.bar(xmtl, y5, width, color='m')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Word Frequency')
    ax.set_xlabel('\nFigure 4: Word Frequency by Department Articles')
    ax.set_title('MIT EECS: Word Frequency per Department')
    # Move the category label further from x-axis
    ax.set_xticks(ind2)
    ax.set_xticklabels(x, rotation='vertical')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(0, 650, 10)
    ax.legend((csailChart[0], lidsChart[0], rleChart[0], unkChart[0], mtlChart[0]), ('CSAIL', 'LIDS', 'RLE', 'UNK', 'MTL'))
    autolabel(csailChart)
    autolabel(lidsChart)
    autolabel(rleChart)
    autolabel(unkChart)
    autolabel(mtlChart)
    plt.show()


def topN(lamb, n):
    lst = []
    for k in range(len(lamb)):
        lambdak = list(lamb[k, :])
        lambdak = lambdak / sum(lambdak)
        temp = zip(lambdak, range(len(lambdak)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        lst.append((k, temp[0][0]))
    top_indices = list(map(lambda y: y[0], sorted(lst, key = lambda x: x[1], reverse=True)[0:n]))
    return lamb[top_indices, :]

def gammaAnalysis(index, dataDict, fac_dict, vocab):
    gammaDict = defaultdict(dict)
    path1 = './gamma'
    gammaFiles = os.listdir(path1)
    gammaFiles = [file for file in gammaFiles if file.endswith('-' + str(index) + '.dat')]
    for file in gammaFiles:
        fileName = file
        gammaScores = []
        count = 0
        with open(path1 + '/' + file, 'r') as f:
            for line in f.readlines():
                gammaScores.append(line.split())
                count += 1
                name = 'topic' + str(count)
                gammaDict[fileName][name] = gammaScores[0]



def lambdaAnalysis(dataDict, fac_dict, vocab):
    path2 = './lambda'
    # lambdaFiles = os.listdir(path2)
    # lst = list()
    # for i in range(1,10):
    #     if i == 1: year = 2017
    #     if i == 2: year = 2016
    #     if i == 3: year = 2015
    #     if i == 4: year = 2014
    #     if i == 5: year = 2013
    #     if i == 6: year = 2012
    #     if i == 7: year = 2011
    #     if i == 8: year = 2010
    #     if i == 9: year = 2009
    #
    #     for j in range(240, 10, -10):
    #         file = (''.join([file for file in lambdaFiles if file.endswith( '-{0}-{1}.dat'.format(j, i))]), year, )
    #         print(type(file), file, file[0], file[1], type(file[0]))
    #         if file[0] == '':
    #             continue
    #         else:
    #             lst.append(file)
    #             break
    # print(len(lst), lst)
    # for file, y in lst:
    testlambda = n.loadtxt(path2 + '/lambda-1110.dat')
    num_topics = 5
    words_per_topic = 10
    word_topic = []
    count = 1
    for i in range(len(testlambda)):
        name = 'topic' + str(count)
        print('\n', name, '\n')
        testl = topN(testlambda, num_topics) # Number of topics desired
        lambdak = list(testl[i, :])
        lambdak = lambdak / sum(lambdak)
        temp = zip(lambdak, range(0, len(lambdak)))
        tmp1 = temp
        temp = sorted(temp, key=lambda x: x[0], reverse=True)
        for j in range(words_per_topic):
            for k, v in vocab.items():
                if v == temp[j][1]:
                    print('{0}\t   :\t   {1}'.format(k, str(round(temp[j][0], 6))))
                    word_topic.append((name , k, str(round(temp[j][0], 6))))
        count += 1

    word_topic = n.array(word_topic)
    # print(word_topic.shape, word_topic)
    # print(word_topic[:,2])

    word_values = list (map (float, word_topic[:,2]))
    fontsize_base = 300 #70 / max(word_values)  # font size for word with largest share in corpus
    print('Fontsize_base: ', fontsize_base)
    temp = 0
    for t in range(num_topics):
        plt.subplot(1, num_topics, t + 1)  # plot numbering starts with 1
        plt.ylim(0, words_per_topic + 0.5)  # stretch the y-axis to accommodate the words
        plt.xticks([])  # remove x-axis markings ('ticks')
        plt.yticks([])  # remove y-axis markings ('ticks')
        plt.title('Topic #{}'.format(t + 1))
        topic = str('topic{}'.format(t + 1))
        currenttopic = word_topic[word_topic[:, 0] == topic]
        # print ('Topic: ', topic, currenttopic)
        top_words_idx = n.argsort(currenttopic[:, 2])[::-1]  # descending order
        # print('top_words_idx1 ', top_words_idx)
        top_words = currenttopic[:,1]
        # print(top_words)
        top_words_shares = list(map(float, currenttopic[:,2]))
        # print(top_words_shares)
        total_share = n.sum(top_words_shares[:])
        # print('TOTAL SHARE: ', total_share)
        # print('top_words_shares: ', type(top_words_shares), top_words_shares)
        percshare = [(( x / total_share)* 100) for x in top_words_shares]
        print('Percentage share per word: ', percshare)
        for i, (word, share) in enumerate(zip(top_words, top_words_shares)):
                plt.text(0.3, words_per_topic - i - 0.5, word, fontsize=fontsize_base * share)
    plt.tight_layout()
    plt.show()
        ########### The numbers are the word-topic probabilities from \lambda.
    print(word_topic[:,(1,2)])
