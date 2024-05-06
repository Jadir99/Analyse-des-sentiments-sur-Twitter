## importation :
from flask import Flask ,render_template
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from flask import request
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
import string 
import contractions 
from nltk.stem import SnowballStemmer
from nltk import WordNetLemmatizer 
from textblob import TextBlob

# login + extraction data from twitter

def login(hashtag):
    """
    function for login and extract data from 
    """

    if '#' in hashtag:
        hashtag = hashtag.replace('#','')

    PATH = "C:/Users/hp/Downloads/edgedriver_win64/msedgedriver.exe"
    driver = webdriver.Edge(PATH)

    url="https://twitter.com/search?q=%23"+hashtag+"&src=typed_query&f=top"
    driver.get(url)

    # Setup the log in
    sleep(6)
    username = driver.find_element(By.XPATH,"//input[@name='text']")
    username.send_keys("jadir99")
    next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
    next_button.click()

    sleep(3)
    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys('jadir99jadir99')
    log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
    log_in.click()
    UserTags = []
    TimeStamps = []
    Tweets = []

    while len(UserTags)<=50:
        
        # Find all the tweet article elements on the page
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        # Extract data from each article
        for article in articles:
            try:
                if(article.find_element(By.XPATH, ".//span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']")):
                    UserTag = article.find_element(By.XPATH, ".//span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']").text
                    if (UserTag not in UserTags):
                        UserTags.append(UserTag)
                if(article.find_element(By.XPATH, ".//time")):
                    TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                    if TimeStamp not in TimeStamps and TimeStamp is not None:
                        TimeStamps.append(TimeStamp)
                if(article.find_element(By.XPATH, ".//time")):
                    Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                    if Tweet not in Tweets and Tweet is not None:
                        Tweets.append(Tweet)
            except NoSuchElementException:
                continue        
            except StaleElementReferenceException:
                continue

        # Scroll down to the bottom of the page
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(3)  # Wait for the page to load more articles
    df = pd.DataFrame(zip(UserTags,TimeStamps,Tweets)
                ,columns=['UserTags','time','Tweets'])
    df.to_csv(r"tweets"+hashtag+".csv", index=False)
    df.to_excel(r"tweets.xlsx", index=False)
    return "tweets"+hashtag+".csv"



# beggin of cleaning the data :

#function for make data logic for machine  dont => do not
def replace_contractions(text):
    return contractions.fix(text)

#function to remove hashtags and mensioons in and urls :
def remove_hashtags_mentions_URLS(text):
    without_hashtag=re.sub(r'#\S*','',text)
    without_mentions =re.sub(r'@\S*','',without_hashtag)
    return re.sub(r'https?://\S+','',without_mentions)


# remove punctuation :
def removePunctuation(text):
    clean_words = [''.join(char for char in word if char not in string.punctuation) for word in text]
    return''.join(clean_words)

# remove the stopwords :
# fr=stopwords.words('french')
# arabe=stopwords.words('arabic')
def remove_stopWords(text):
    ang=stopwords.words('english')
    # clean from stopword
    return ' '.join([word for word in text.split() if word not in ang])

    #steeming :
def stemming(text):
    eng=SnowballStemmer("english")
    return ' '.join([eng.stem(word) for word in text.split()])

#lematization :
def lemmatizer(text):
    l=  WordNetLemmatizer()
    return l.lemmatize(text) 
 

# analyse the sentiment pour chaque tweet  :
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
        

# function call all the subfunctions
def clean_data(path):
    df=pd.read_csv(str(path))
    # make all lower 
    df['Tweets']=df['Tweets'].str.lower()
    df['UserTags']=df['UserTags'].str.lower()

    # make correige les faux d'ortographe 
    df['Tweets']=df['Tweets'].apply(lambda x:replace_contractions(str(x)))

    # applciate the fucntion for claen from urls hashtasg ...
    df['Tweets']=df['Tweets'].apply(lambda x:remove_hashtags_mentions_URLS(x))
    df['UserTags']=df['UserTags'].apply(lambda x:remove_hashtags_mentions_URLS(str(x)))
    
    # applicate function to remove punctuation 
    df['Tweets']=df['Tweets'].apply(lambda x:removePunctuation(x))
    df['UserTags']=df['UserTags'].apply(lambda x:removePunctuation(x))
    
    # aplicate the funtion remove_stopWords in dataframe 
    df['Tweets']=df['Tweets'].apply(lambda x:remove_stopWords(x))
    df['UserTags']=df['UserTags'].apply(lambda x:remove_stopWords(x))
    

    # applaying this function in the datframe 
    df['Tweets']=df['Tweets'].apply(lambda x:stemming(x))
      
    # save modification 
    df.to_csv(r"clear"+path, index=False)

    ## ise textblob to analyse the sentiment 
    sentiments=[]
    for tweet in df['Tweets']:
        sentiments.append(get_tweet_sentiment(tweet))
    df['sentiments']=sentiments

    fig, ax=plt.subplots()
    sentiments=['negative','neutral','positive']
    counts=[len(df[df['sentiments'] == 'neutral']),len(df[df['sentiments'] == 'negative']),len(df[df['sentiments'] == 'positive'])]
    bar_labels=['red','green','blue']
    bar_colors=['tab:red','tab:green','tab:blue']
    ax.bar(sentiments,counts,label=bar_labels,color=bar_colors)
    plt.savefig("static/img/"+''.join(path.split('.csv'))+'sentiments_bar_plot.png', bbox_inches='tight', pad_inches=0)

    # wordlcloud 
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Tweets'].values))

    # Display the generated word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("static/img/"+''.join(path.split('.csv'))+'wordcloud.png', bbox_inches='tight', pad_inches=0)
    # return path of images 
    return [''.join(path.split('.csv'))+"wordcloud.png",''.join(path.split('.csv'))+"sentiments_bar_plot.png"]

