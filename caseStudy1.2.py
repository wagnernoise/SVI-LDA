import os
from dataPreprocessing import *


def main():
    # Scrape Data from arXiv
    response = input('Do you want download faculty names (Y/N): ')
    if response in ('Y', 'y'):
        fac_names = faculty()
        getMITAbstracts = input('Do you want to pull down abstracts from MIT papers? (Y/N): ')
        if getMITAbstracts in ('Y', 'y'):
            getArticles(fac_names)
        print(fac_names)

    # Load Data from 'Abstracts' directory
    corpusDict = defaultdict(list)
    path = './Abstracts'
    for filename in os.listdir(path):
        popDict(corpusDict, path, filename)

    # Converting all text to lowercase, tokenizing, and assigning the part of speech (POS)
    corpusDict = step1PreProcess(corpusDict)

if __name__ == '__main__':
    main()



