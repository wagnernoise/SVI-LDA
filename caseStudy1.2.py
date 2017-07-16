import lda_vb
import dataPreprocessing as dp
from collections import defaultdict
import os
import itertools
import random

def main():
#    # Download MIT faculty member names
#    response = input('Do you want download faculty names (Y/N): ')
#    if response in ('Y', 'y'):
#        fac_names = dp.faculty()
#        # Scrape # Scrape Data from arXiv
#        getMITAbstracts = input('Do you want to pull down abstracts from MIT papers? (Y/N): ')
#        if getMITAbstracts in ('Y', 'y'):
#            do.getArticles(fac_names)
        # print(fac_names)

############################ Uncomment all of the code up to main() if you
#        just want to download your own abstract data. Otherwise the data is
# provided in the project sub-folder Abstracts.


    # Load Data from 'Abstracts' directory
    countAbs = 0 # gets the number of files in the ./Abstracts folder. This value sets parameter
    # 'D' -- total number of abstracts from arXiv
    corpusDict = defaultdict(list)
    path = './Abstracts'
    for filename in os.listdir(path):
        countAbs += 1
        dp.popDict(corpusDict, path, filename)


    # Converting all text to lowercase, tokenizing, and stemming
    corpusDict = dp.step1PreProcess(corpusDict)

    # Get unique list of all words from all Abstracts
    # Take list of preprocessed keys
    # and convert to a list of lists (one list is all preprocessed words in one abstract)
    l = list()
    l = [list(corpusDict[k][5].keys()) for k in corpusDict.keys()]
    #print(len(l), l)
    # Convert list of lists in one list
    # (words from one abstract combined with words from all abstracts)
    l = list(itertools.chain.from_iterable(l))
    #print(len(l), l)
    # 84483 words total

    # Convert to a Counter dictionary where it removes duplications and makes the word a key,
    # and the value is the count for that word. For example, algorithm shows up 350 times
    # out of the 1,120 abstracts.
    counter = dp.Counter(l)
    #print(len(l), l)
    #print(len(counter), counter)
    # Remove just the keys from counter and make a list of vocab (23901 unique words)
    # vocab: A set of words to recognize.When analyzing documents, any word not in this
    # set will be ignored.
    # Therefore, stemming will not be performed.
    vocab = list()
    vocab = [k for k in counter.keys()]

    # The number of documents to analyze each iteration
    batchsize = 64
    # The total number of documents in Abstracts folder
    D = countAbs
    # The number of topics
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

    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    lda = lda_vb.LDAVB(vocab, K, D, alpha, eta, tau, kappa)
    # Run until we've seen D documents. (Feel free to interrupt *much*
    # sooner than this.)


    # How many documents to look at
    documentstoanalyze = int(D / batchsize)

    docset = list()
    for i in range(documentstoanalyze):
        # Extract randomly selected abstracts, index[4], from corpusDict
        # and articlename/title index[3].
        key = random.choice(list(corpusDict.keys()))
        docset.append(corpusDict[key][4])
        print(type(docset), docset)
    # Give them to online LDA
    gamma, bound = lda.update_lambda_docs(docset)
    # Compute an estimate of held-out perplexity
    wordids, wordcts = onlineldavb.parse_doc_list(docset, lda._vocab)
    perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
    # print ('%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
    #       (iteration, lda._rhot, numpy.exp(-perwordbound)))

    # Save lambda, the parameters to the variational distributions
    # over topics, and gamma, the parameters to the variational
    # distributions over topic weights for the articles analyzed in
    # the last iteration.
    # if (iteration % 10 == 0):
    #     numpy.savetxt('lambda-%d.dat' % iteration, lda._lambda)
    #     numpy.savetxt('gamma-%d.dat' % iteration, gamma)




if __name__ == '__main__':
    main()



# import cPickle, string, numpy, getopt, sys, random, time, re, pprint
#
# import onlineldavb
# import wikiDownload
#
# def main():
#     """
#     Downloads and analyzes a bunch of random Wikipedia articles using
#     online VB for LDA.
#     """
#
#     # The number of documents to analyze each iteration
#     batchsize = 64
#     # The total number of documents in Wikipedia
#     D = 3.3e6
#     # The number of topics
#     K = 100
#
#     # How many documents to look at
#     if (len(sys.argv) < 2):
#         documentstoanalyze = int(D/batchsize)
#     else:
#         documentstoanalyze = int(sys.argv[1])
#
#     # Our vocabulary
#     vocab = file('./dictnostops.txt').readlines()
#     W = len(vocab)
#
#     # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
#     lda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
#     # Run until we've seen D documents. (Feel free to interrupt *much*
#     # sooner than this.)
#     for iteration in range(0, documentstoanalyze):
#         # Download some articles
#         (docset, articlenames) = \
#             wikiDownload.get_random_wikipedia_articles(batchsize)
#         # Give them to online LDA
#         (gamma, bound) = lda.update_lambda_docs(docset)
#         # Compute an estimate of held-out perplexity
#         (wordids, wordcts) = onlineldavb.parse_doc_list(docset, lda._vocab)
#         perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
#         print ('%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
#             (iteration, lda._rhot, numpy.exp(-perwordbound)))
#
#         # Save lambda, the parameters to the variational distributions
#         # over topics, and gamma, the parameters to the variational
#         # distributions over topic weights for the articles analyzed in
#         # the last iteration.
#         if (iteration % 10 == 0):
#             numpy.savetxt('lambda-%d.dat' % iteration, lda._lambda)
#             numpy.savetxt('gamma-%d.dat' % iteration, gamma)
#
# if __name__ == '__main__':
#     main()
