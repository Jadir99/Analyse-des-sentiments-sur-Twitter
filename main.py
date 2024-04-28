
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import matplotlib as plt
df=pd.read_excel("test.xlsx")
import string 
df['Tweets']=df['Tweets'].str.lower()
df['UserTags']=df['UserTags'].str.lower()
df.head()
import contractions 
def replace_contractions(text):
    return contractions.fix(text)
replace_contractions("don't")

df['Tweets']=df['Tweets'].apply(lambda x:replace_contractions(x))
import re
# remove hashtags and mentions in text:
def remove_hashtags_mentions_URLS(text):
    without_hashtag=re.sub(r'#\S*','',text)
    without_mentions =re.sub(r'@\S*','',without_hashtag)
    return re.sub(r'https?://\S+','',without_mentions)
#applicate the function in the dataframe
df['Tweets']=df['Tweets'].apply(lambda x:remove_hashtags_mentions_URLS(x))
df['UserTags']=df['UserTags'].apply(lambda x:remove_hashtags_mentions_URLS(x))
def removePunctuation(text):
    clean_words = [''.join(char for char in word if char not in string.punctuation) for word in text]
    return''.join(clean_words)
df['Tweets']=df['Tweets'].apply(lambda x:removePunctuation(x))
df['UserTags']=df['UserTags'].apply(lambda x:removePunctuation(x))
ang=stopwords.words('english')
fr=stopwords.words('french')
arabe=stopwords.words('arabic')
def remove_stopWords(text):
    # clean from stopword
    return ' '.join([word for word in text.split() if word not in ang])  
print(remove_stopWords("jadir i am you are we not have and enaugh"))
df['Tweets']=df['Tweets'].apply(lambda x:remove_stopWords(x))
df['UserTags']=df['UserTags'].apply(lambda x:remove_stopWords(x))
#steeming verbs en inf 
from nltk.stem import SnowballStemmer
def stemming(text):
    eng=SnowballStemmer("english")
    return ' '.join([eng.stem(word) for word in text.split()])
df['Tweets']=df['Tweets'].apply(lambda x:stemming(x))
from nltk import WordNetLemmatizer 
l=  WordNetLemmatizer()
def lemmatizer(text):
    return l.lemmatize(text) 
from spellchecker import SpellChecker
S=SpellChecker()
def correct_spellings(text):
    return ' '.join([S.correction(word )for word in text.split()])
df.to_csv(r"clear_tweets.csv", index=False)
df.to_excel(r"clear_tweets.xlsx", index=False)
from textblob import TextBlob
negative=[]
neutral=[]
positive=[]
# analyse the sentiment :
def get_tweet_sentiment(tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            # positive.append
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
sentiments=[]
for tweet in df['Tweets']:
     sentiments.append(get_tweet_sentiment(tweet))
df['sentiments']=sentiments
import matplotlib.pyplot as plt
fig, ax=plt.subplots()
sentiments=['negative','neutral','positive']
counts=[len(df[df['sentiments'] == 'neutral']),len(df[df['sentiments'] == 'negative']),len(df[df['sentiments'] == 'positive'])]
bar_labels=['red','green','blue']
bar_colors=['tab:red','tab:green','tab:blue']
ax.bar(sentiments,counts,label=bar_labels,color=bar_colors)
plt.show()