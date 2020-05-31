import copy
import math
import urllib.request
import json
from bs4 import BeautifulSoup
from bs4.element import Comment
import plotly.graph_objects as go
from plotly.subplots import make_subplots

positive_freq = []
negative_freq = []
wordAll = []
freqAll = []

posword_freq = {}
negword_freq = {}
stopWordList = {}
probability = {}

stopword_file = open("assets/stopwords.txt", "r")
nltk_stopwords = stopword_file.read().lower().split("\n")
# print(nltk_stopwords)
positive_file = open("assets/allpositivewords.txt", "r")
allpositivewords = positive_file.read().lower().split(",  ")
# print(allpositivewords)
negative_file = open("assets/allnegativewords.txt", "r", encoding="UTF8")
allnegativewords = negative_file.read().lower().split(",    ")
print(allnegativewords)

transport = ["bus", "flight", "taxi", "ktm"]
urls = ["https://www.malaysiakini.com/news/502024",
        "https://www.channelnewsasia.com/news/asia/malaysia-airlines-auckland-aborted-takeoff-mh145-new-zealand-12241318",
        "https://www.malaymail.com/news/malaysia/2019/12/13/taxi-drivers-must-transform-and-adopt-latest-technology-says-loke/1818997",
        "https://themalaysianreserve.com/2020/02/03/to-awaken-the-sleeping-and-sluggish-giant"]


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def extract_text(url):

    opener = AppURLopener()
    response = opener.open(url)
    html = response.read()
    rawstring = text_from_html(html)
    wordstring = rawstring.lower()

    # print(wordstring.lower())
    wordlist = wordstring.split()
    # print("wordlist")
    # print(wordlist)
    wordfreq = [wordlist.count(w) for w in wordlist]

    # print("String\n" + wordstring + "\n")
    # print("List\n" + str(wordlist) + "\n")
    # print("Frequencies\n" + str(wordfreq) + "\n")
    # print("Pairs\n" + str(list(zip(wordlist, wordfreq))))

    # file = open('assets/bus.txt', 'w+', encoding='utf8')
    # file.write(wordstring)
    # file.close

    return wordstring, wordlist, wordfreq


stopWordListx = {}


def countStopWordList(words, i, txt):
    stopwordFreq = []
    stopwords = []
    temp = {}
    for word in words:
        if word in nltk_stopwords and word not in stopwords:
            stopwords.append(word)
            stopwordFreq.append(words.count(word))
    temp['wordFreq'] = stopwordFreq
    temp['wordList'] = stopwords
    stopWordListx[i] = copy.deepcopy(temp)


def countStopWord(words, i, txt):
    stopwordFreq = []
    stopwords = []
    temp = {}
    for word in words:
        if word in nltk_stopwords and word not in stopwords:
            stopwords.append(word)
            freq = rabinKarp(word, txt)
            # print(freq)
            stopwordFreq.append(freq)
    temp['wordList'] = stopwords
    temp['wordFreq'] = stopwordFreq
    stopWordList[i] = copy.deepcopy(temp)


def removeStopwords(words):
    return [word for word in words if word not in nltk_stopwords]


def countPositiveWords(words, i, txt):
    posWordFreq = []
    posWords = []
    temp = {}
    for word in words:
        if word in allpositivewords and word not in posWords:
            posWords.append(word)
            freq = rabinKarp(word, txt)
            posWordFreq.append(freq)
    temp['wordList'] = posWords
    temp['wordFreq'] = posWordFreq
    posword_freq[i] = copy.deepcopy(temp)


def countNegativeWords(words, i, txt):
    negWordFreq = []
    negWords = []
    temp = {}
    for word in words:
        if word in allnegativewords and word not in negWords:
            negWords.append(word)
            freq = rabinKarp(word, txt)
            negWordFreq.append(freq)
    temp['wordList'] = negWords
    temp['wordFreq'] = negWordFreq
    negword_freq[i] = copy.deepcopy(temp)


def rabinKarp(pat, txt):
    # q is a prime number
    q = 1217
    d = 256
    M = len(pat)
    N = len(txt)
    freq = i = j = p = t = 0
    # p = hash value for pattern
    # t = hash value for txt
    h = 1

    # The value of h would be "pow(d, M-1)%q"
    for i in range(M-1):
        h = (h*d) % q

    # Calculate the hash value of pattern and first window
    # of text
    for i in range(M):
        p = (d*p + ord(pat[i])) % q
        t = (d*t + ord(txt[i])) % q

    # Slide the pattern over text one by one
    for i in range(N-M+1):
        # Check the hash values of current window of text and
        # pattern if the hash values match then only check
        # for characters on by one
        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break

            j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == M:
                # print("Pattern found at index " + str(i))
                freq += 1

        # Calculate hash value for next window of text: Remove
        # leading digit, add trailing digit
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M])) % q

            # We might get negative values of t, converting it to
            # positive
            if t < 0:
                t = t+q

    return freq


def plotStopwords():
    traces = []
    for i in range(len(transport)):
        x = stopWordList[i]['wordList']
        y = stopWordList[i]['wordFreq']
        traces.append(go.Bar(x=x, y=y, name=transport[i]))

    cols = 2
    rows = math.ceil(len(transport)/cols)

    fig = make_subplots(rows=rows, cols=cols, vertical_spacing=0.5/rows)

    for i in range(len(traces)):
        row = i//cols
        col = i % cols
        fig.add_trace(traces[i], row=row+1, col=col+1)

    fig.update_layout(title_text="Number of stopwords per entry")
    fig.show()


for i in range(len(urls)):
    txt, wordlist, wordfreq = extract_text(urls[i])
    countStopWord(wordlist, i, txt)

    # print(
    #     str(list(zip(stopWordList[i]['wordList'], stopWordList[i]['wordFreq']))))
    # print()
    # print()
    # countStopWordList(wordlist, i, txt)
    # print(
    #     str(list(zip(stopWordListx[i]['wordList'], stopWordListx[i]['wordFreq']))))
    # print('--------------------------------------------------------------------------------------------------------------------')

    wordlist = removeStopwords(wordlist)
    countPositiveWords(wordlist, i, txt)
    countNegativeWords(wordlist, i, txt)

    try:
        with open('assets/news-{}.txt'.format(transport[i]), 'w', encoding='utf-8')as outfile:
            outfile.write(txt)
    except Exception as e:
        print(e)
    try:
        with open('assets/stopwordFreq-{}.txt'.format(transport[i]), 'w', encoding='utf-8')as outfile:
            json.dump(stopWordList[i], outfile, ensure_ascii=False)
    except Exception as e:
        print(e)
    try:
        with open('assets/positiveWordFreq-{}.txt'.format(transport[i]), 'w', encoding='utf-8')as outfile:
            json.dump(posword_freq[i], outfile, ensure_ascii=False)
    except Exception as e:
        print(e)
    try:
        with open('assets/negativeWordFreq-{}.txt'.format(transport[i]), 'w', encoding='utf-8')as outfile:
            json.dump(negword_freq[i], outfile, ensure_ascii=False)
    except Exception as e:
        print(e)


# outside for loop
plotStopwords()
