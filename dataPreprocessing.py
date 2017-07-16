from stop_words import get_stop_words
import nltk
from nltk import word_tokenize
from bs4 import BeautifulSoup
import urllib.request
import time
import string
from collections import defaultdict, Counter
import os
import re

def popDict(dataDict, path, filename):
    with open(path + '/' + filename, 'r') as f:
       for line in f.readlines():
            line = line.strip()
            if re.search('^Filename:', line):
                filename = re.search('^Filename:\s(.*)\.', line).groups(1)[0]
            elif re.search('^Author:', line):
                author = re.search('^Author:\s(.*)', line).groups(1)[0]
                dataDict[filename].append(author)
            elif re.search('^Citation Date:', line):
                citation_date = re.search('^Citation Date:\s(.*)', line).groups(1)[0]
                dataDict[filename].append(citation_date)
            elif re.search('^Abstract URL:', line):
                abstract_url = re.search('^Abstract URL:\s(.*)', line).groups(1)[0]
                dataDict[filename].append(abstract_url)
            elif re.search('^Title:', line):
                title = re.search('^Title:\s(.*)', line).groups(1)[0]
                dataDict[filename].append(title)
            elif re.search('^Abstract:', line):
                abstract = re.search('^Abstract:\s(.*)', line).groups(1)[0]
            else:
                abstract += line
    dataDict[filename].append(abstract)
    return dataDict

def nested_dict():
    return defaultdict(nested_dict)

def readURL(url):
    print(url)
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.URLError as e:
        print('Message on readURL error: ', e.reason)
        return None

    return html

def faculty():
    html = readURL("https://www.eecs.mit.edu/people/faculty-advisors")
    soup = BeautifulSoup(html, 'html.parser')

    names = list()
    divs = soup.find_all(class_="field-content card-title")
    for div in divs:
        names.append(div.get_text())
    return names

def getArticles(fac_lst):
    #Search papers in arXiv for each person in
    # arxiv.org/find/all/1/au:+(lastname)_(initial)/0/1/0/all/0/1
    abs_dict = nested_dict()
    fac_dict = nested_dict()
    count = 0
    for i in range(146, len(fac_lst)):
        try:
            fname, lname = fac_lst[i].split()
            fac_dict[i] = (lname, fname,)
        except:
            print('Error occurred:', count)
            count += 1
            continue
            # Not going to worry about rare exceptions of one name --
            # which there is at least one
        try:
            mirror = 'https://arxiv.org:443'
            search_str = mirror + '/find/all/1/au:+' + fac_dict[i][0] + '_' + fac_dict[i][1] + \
                         '/0/1/0/all/0/1'
            print('Search string', search_str)
        except:
            msg = "Cannot open %s" % search_str
            print(msg)
            print('Error occurred:', count)
            count += 1
            continue
        try:
            paper = readURL(search_str)
            soup = BeautifulSoup(paper, "html.parser")
            #print(soup.contents)
            spans = soup.find_all("span", class_="list-identifier")
        except:
            continue
        if len(spans) == 0:
            continue
        print(str(i) + " " + fac_dict[i][0] + ", " + fac_dict[i][1] + " has " + \
              str(len(spans)) + " abstract(s)")
        for span in spans:
            abs_url = 'https://arxiv.org/' + span.a["href"]
            html_text = readURL(abs_url)
            soup = BeautifulSoup(html_text, "html.parser");
            abstract = soup.find("blockquote", class_="abstract").text
            citation_date = soup.find("meta", {"name":"citation_date"})['content']
            abstract = abstract.replace("Abstract: ", "")
            title = soup.find("h1", class_="title").text
            pattern = '%Y/%m/%d'
            epoch = int(time.mktime(time.strptime(citation_date, pattern)))
            filename = str(str(epoch) + '_' + fac_dict[i][0] + '.txt')
            author = str(fac_dict[i][0] + ", " + fac_dict[i][1])
            abs_complete = str('Filename: ' + filename + '\n' + \
                'Author: ' + author + \
                '\n' + 'Citation Date: ' + citation_date + '\n' + \
                'Abstract URL: ' + abs_url + '\n' + title + '\n' + \
                'Abstract: ' + abstract)
            try:
                print(abs_complete)
                if not os.path.exists('./Abstracts20170711'):
                    os.makedirs('./Abstracts20170711')
                target_dir = r"./Abstracts20170711"
                fullname = os.path.join(target_dir, filename)
                with open(fullname, "w") as f:
                        f.write(abs_complete)
                f.close()
                print("   stored in %s" % filename)
            except:
                print("   FAILURE: could not store in %s !" % filename)

def step1PreProcess(dataDict):
    temp = list()
    for k in dataDict.keys():
#        if 'Karger' in k:
        temp = dataDict[k][4].lower()
        temp1 = re.sub('['+string.punctuation+']', '', temp)
        words = word_tokenize(temp1)
        # create English stop words list
        en_stop = get_stop_words('en')
        stopped_tokens = [i for i in words if not i in en_stop]

        # According to NLTK documentation:
        # "Observe that the Porter stemmer correctly handles the word lying
        # (mapping it to lie), while the Lancaster stemmer does not."
        # See documentation. Stemming will not be performed on this data.
        #porter = nltk.PorterStemmer()
        #lancaster = nltk.LancasterStemmer()
        #stemmedWords = [porter.stem(t) for t in stopped_tokens]
        #print(stemmedWords)
        dataDict[k].append(Counter(stopped_tokens))
        #print(dataDict[k][5])
    return dataDict


if __name__ == '__main__':
    pass