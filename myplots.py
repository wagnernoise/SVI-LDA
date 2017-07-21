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
# # plot 2
#     y3 = list(map(int, list(y2.keys())))
#     abs3 = list(map(int, list(y2.values())))
#
#
#     ax1 = fig.add_subplot(1, 2, 2, facecolor='grey')
#     ax1.spines['right'].set_visible(False)
#     ax1.spines['top'].set_visible(False)
#     ax1.minorticks_on()
#     plt.xlim(2008, 2018, 1)
#     plt.ylim(0, 300, 10)
#
#     Colors = 'rgbkmc'
#     ax1.bar(y3, abs3, align='center',width=0.5, color=Colors)
#     ax1.set_xlabel('Year \n Fig: 2')
#
#
#     plt.title('MIT EECS: Groups for Analysis\n (Fig 2: 2009 is sum of all prior) ')
#
#     plt.show()

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
    lambdaFiles = os.listdir(path2)
    lst = list()
    for i in range(1,10):
        if i == 1: year = 2017
        if i == 2: year = 2016
        if i == 3: year = 2015
        if i == 4: year = 2014
        if i == 5: year = 2013
        if i == 6: year = 2012
        if i == 7: year = 2011
        if i == 8: year = 2010
        if i == 9: year = 2009

        for j in range(240, 10, -10):
            file = (''.join([file for file in lambdaFiles if file.endswith( '-{0}-{1}.dat'.format(j, i))]), year, )
            print(type(file), file, file[0], file[1], type(file[0]))
            if file[0] == '':
                continue
            else:
                lst.append(file)
                break
    print(len(lst), lst)
    for file, y in lst:
        testlambda = n.loadtxt(path2 + '/' + file)
        count = 1
        for i in range(len(testlambda)):
            name = 'topic' + str(count) + '  year = ' + str(y) + '\n'
            print('\n', name)
            testl = topN(testlambda, 5) # Number of topics desired
            words_per_topic = 5
            lambdak = list(testl[i, :])
            lambdak = lambdak / sum(lambdak)
            temp = zip(lambdak, range(0, len(lambdak)))
            temp = sorted(temp, key=lambda x: x[0], reverse=True)
            for j in range(words_per_topic):
                for k, v in vocab.items():
                    if v == temp[j][1]:
                        print('{0}\t   :\t   {1}'.format(k, str(round(temp[j][0], 6))))
            count += 1
            s = n.random.dirichlet((10, 5, 10), 5).transpose()
            # alpha: array Parameter of the distribution(k dimension
                # for sample of dimension k)
                # # s = numpy.random.dirichlet((10, 5, 3), 10).transpose()
                # 4 (Final number) is the number of labs (number of strings or bars)
                # the 3 is number of lists - or topics within each sting
                # 20 is the number of elements per list (len(lst))

            plt.barh(range(5), s[0])
            plt.barh(range(5), s[1], left=s[0], color='g')
            plt.barh(range(5), s[2], left=s[0] + s[1], color='r')
            plt.title("Lengths of Strings")




# s = numpy.random.dirichlet((10, 5, 3), 20).transpose()
# plt.barh(range(20), s[0])
# plt.barh(range(20), s[1], left=s[0], color='g')
# plt.barh(range(20), s[2], left=s[0]+s[1], color='r')
# plt.title("Lengths of Strings")