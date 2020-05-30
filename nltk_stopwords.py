import nltk
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
# print(stopwords)
# print(stopwords[0])

with open('assets/stopwords.txt', 'w', encoding='utf8') as file:
    for i in range(len(stopwords)):
        if i < len(stopwords)-1:
            file.write(stopwords[i]+'\n')
        else:
            file.write(stopwords[i])
