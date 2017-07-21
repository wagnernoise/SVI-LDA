#!/usr/bin/python

from lda_vb import *
import dataPreprocessing as dp
from collections import defaultdict, Counter
import os
import itertools
import myplots as mp



def main(response):

    # Download MIT faculty member names
    # Remove comments below to download your own set of abstracts -- or use the ones I provided.
    # fac_dict = dp.faculty()
    # fac_names = []
    # file = open('facutly.txt', 'w')
    # for k, v in fac_dict.items():
    #     fac_names.append((k,v,))
    #     file.write(v +'\t' + k + '\n')
    # file.close()
    # print(fac_dict)
    # print(fac_names)

    file = open('facutly.txt', 'r')
    fac_dict = defaultdict(list)
    for line in file.readlines():
        try:
            dept, fname, lname = line.strip().split()
            fac_dict[dept].append((lname, fname,))
        except:
            print('Fix this name in the file: ', line)
    # print('There are ' + str(len(fac_dict)) + ' departments (counting "UNK").')
    # for k, v in fac_dict.items():
    #     print('In the ' + k + ' department, there are ' + str(len(fac_dict[k])) + ' faculty members.')

    # Scrape # Scrape Data from arXiv



    # Load Data from 'Abstracts' directory
    countAbs = 0 # gets the number of files in the ./Abstracts folder. This value sets parameter
    # 'D' -- total number of abstracts from arXiv
    corpusDict = defaultdict(list)
    path = './Abstracts'
    for filename in os.listdir(path):
        countAbs += 1
        dp.popDict(corpusDict, path, filename)

    for k, v in corpusDict.items():
        if int(v[2]) <= 2009:
            corpusDict[k][2] = (v[2], 9,)
        elif int(v[2]) == 2010:
            corpusDict[k][2] = (v[2], 8,)
        elif int(v[2]) == 2011:
            corpusDict[k][2] = (v[2], 7,)
        elif int(v[2]) == 2012:
            corpusDict[k][2] = (v[2], 6,)
        elif int(v[2]) == 2013:
            corpusDict[k][2] = (v[2], 5,)
        elif int(v[2]) == 2014:
            corpusDict[k][2] = (v[2], 4,)
        elif int(v[2]) == 2015:
            corpusDict[k][2] = (v[2], 3,)
        elif int(v[2]) == 2016:
            corpusDict[k][2] = (v[2], 2,)
        elif int(v[2]) == 2017:
            corpusDict[k][2] = (v[2], 1,)


    # Convert to a Counter dictionary where it removes duplications and makes the word a key,
    # and the value is the count for that word. For example, algorithm shows up 350 times
    # out of the 1,119 abstracts.
    # Converting all text to lowercase, tokenizing, and stemming

    corpusDict = dp.preProcess(corpusDict)

    # Removing names from fac_dict that don't have articles in the corpusDict
    for k, v in fac_dict.items():
        lst = list()
        for i in range(len(v)):
            if any(key.endswith(v[i][0]) for key in corpusDict):
                lst.append(v[i])
        fac_dict[k] = lst
        print('The key ' +  k + ' now has ' + str(len(fac_dict[k])) + ' list members - at end of iteration')

    # print('There are ' + str(len(fac_dict)) + ' departments (including "UNK").')
    # for k, v in fac_dict.items():
    #     print('In the ' + k + ' department, there are ' + str(len(fac_dict[k])) + ' faculty members with published papers.')

    # Add department to dictionary
    for k, v in corpusDict.items():
        #print(v[0][:v[0].index(',')])
        lname = v[0][:v[0].index(',')]
        for dept, name in fac_dict.items():
            for i in range(len(name)):
                if lname in name[i]:
                    #print('corpus key ', k, ' and fac dept and name ', dept, ' ' , name[i])
                    department = dept
        corpusDict[k].append(department)

    # Uncomment the following code to get the structure of corpusDict == there are now 9 items in the values list.
    for k, v in corpusDict.items():
        print('key: ', k)
        for i in range(len(v)):
            print('index: ', i, ' type: ', type(v[i]), ' value: ', v[i])
        break
    #
    mp.plotDepartments(corpusDict)
    #mp.plotAbstracts(corpusDict)
    K = 5
    # alpha - parameter for per-document topic distribution
    alpha = 1./K
    # eta - parameter for per-topic vocab distribution
    eta = 1./K
    # tau - delay that down weights  early iterations
    tau = 1024
    # kappa - forgetting rate, controls how quickly
    # old information is forgotten; the larger the value, the slower it is)
    kappa = 0.7


    # lst = [corpusDict[k][8] for k in corpusDict.keys()]
    # print(lst)
    counter = Counter(list(itertools.chain.from_iterable([corpusDict[k][8] for k in corpusDict.keys()])))
    # Unique list of words from Titles
    vocab = [k for k in counter.keys()]
    #Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    D = countAbs
# Initialize LDAVB Class onlineLDA
    lda = LDAVB(vocab, K, D, alpha, eta, tau, kappa)
    print('vocab: ', len(vocab), type(vocab), len(counter))
    print('lda._vocab: ', len(lda._vocab), type(lda._vocab))
    # How many documents to look at
    docset = list()
    if response == ('X'):
        countIter = 1
        total = 0
        for i in range(1, 10):
            docset = list()
            ldaDict = defaultdict()
            for k in corpusDict.keys():
                if corpusDict[k][2][1] == i:
                    ldaDict[k] = corpusDict[k]
            # The above pulls out documents by group which is based on year:
            #   1990-2009
            #   2010
            #   2011
            #   ...
            #   2017
            D = len(corpusDict) # We want the total number of documents - not just the number for this iteration
            print('Number of documents in group ', i,' is ', len(ldaDict))
            total += len(ldaDict)
            if i == 9:
                print('Total sum of groups = ', total, ' which should = ', countAbs, ' (total number of abstracts)')
            for k in ldaDict.keys():
                docset.append(' '.join(ldaDict[k][6]))
                #print(len(docset), docset)
            # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
            documentsToAnalyze = int(len(ldaDict))
            print('documentsToAnalyze:', documentsToAnalyze)
            for j in range(1, documentsToAnalyze + 1):
                countIter = j
                # print('j', j)
                # print('This is j:', j, ' and documents to analyze: ', documentsToAnalyze)
                # print('And this is countIter: ', countIter)
                gamma, bound = lda.update_lambda_docs(docset)
                # Compute an estimate of held-out perplexity
                wordids, wordcts = parse_doc_list(docset, lda._vocab)
                perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
                print ('Iteration {0}:  rho_t = {1},  held-out perplexity estimate = {2}'.format(countIter , lda._rhot, n.exp(-perwordbound)))
                # Save lambda, the parameters to the variational distributions
                # over topics, and gamma, the parameters to the variational
                # distributions over topic weights for the articles analyzed in
                # the last iteration.
                if (countIter % 10 == 0):
                    n.savetxt('./lambda/lambda1-{0}-{1}.dat'.format(countIter, i), lda._lambda)
                    n.savetxt('./gamma/gamma1-{0}-{1}.dat'.format(countIter, i), gamma)

    if response == ('P'):
        countIter = 1
        total = 0
        D = len(corpusDict)  # We want the total number of documents - not just the number for this iteration
        for k in corpusDict.keys():
            docset.append(' '.join(corpusDict[k][6]))
        documentsToAnalyze = int(len(corpusDict) * 0.8)
        print('documentsToAnalyze:', documentsToAnalyze)
        for j in range(1, documentsToAnalyze + 1):
            countIter = j
            gamma, bound = lda.update_lambda_docs(docset)
            # Compute an estimate of held-out perplexity
            wordids, wordcts = parse_doc_list(docset, lda._vocab)
            perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
            print('Iteration {0}:  rho_t = {1},  held-out perplexity estimate = {2}'.format(countIter, lda._rhot, n.exp(-perwordbound)))
            # Save lambda, the parameters to the variational distributions
                # over topics, and gamma, the parameters to the variational
                # distributions over topic weights for the articles analyzed in
                # the last iteration.
            if (countIter % 10 == 0):
                n.savetxt('./lambda/lambda1-{0}.dat'.format(countIter), lda._lambda)
                n.savetxt('./gamma/gamma1-{0}.dat'.format(countIter), gamma)


                                    # if response == 'R':
    #     ldaDict = corpusDict.copy()
    #     index = 0
    #     lst = lda._vocab
    #     mp.lambdaAnalysis(ldaDict, fac_dict, lst)


if __name__ == '__main__':

    # response = ''
    # while response not in ('P', 'R'):
    #     response = input('Do you want to (P)rocess data, or (R)eport on Topic Distibution? (P/R): ')
    #
    # if response in ('P'):
    #     fac_names = dp.faculty()
    #     dp.getArticles(fac_names)
    #     print(fac_names)
    #     print('After the data has been scraped off arXiv webiste')
    #     print('you will need to open the filed with a text editor')
    #     print('with regex search and replace capability and replace')
    #     print('Title: end of line with a space (put title on same line')
    #     print('as the lable Title:. Same with Abstract:. Sorry, I got')
    #     print('lazy and was having to swap IP addresses too often to')
    #     print('get it downloaded. Then comment out this block so you go to main()')
    response = 'P'
    main(response)

