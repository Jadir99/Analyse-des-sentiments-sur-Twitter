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
from selenium.webdriver.edge.service import Service

# login + extraction data from twitter

def login(hashtag):
    """
    function for login and extract data from 
    """

    if '#' in hashtag:
        hashtag = hashtag.replace('#','')

    PATH ='C:\\Users\\hp\\Downloads\\edge_driver\\msedgedriver.exe'
    
    service = Service(PATH)
    driver = webdriver.Edge(service=service)


    url="https://twitter.com/search?q=%23"+hashtag+"&src=typed_query&f=top"
    driver.get(url)

    # Setup the log ina
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

    while len(Tweets) <= 50:
        # Find all the tweet article elements on the page
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        # Extract data from each article
        for article in articles:
            try:
                UserTag = article.find_element(By.XPATH, ".//div[@dir='ltr']//span").text
                TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

                UserTags.append(UserTag)
                TimeStamps.append(TimeStamp)
                Tweets.append(Tweet)
            except NoSuchElementException:
                continue        
            except StaleElementReferenceException:
                continue

        time.sleep(1)
        # Scroll down to the bottom of the page
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(3)  # Wait for the page to load more articles

    # Create a DataFrame and save to CSV and Excel
    df = pd.DataFrame(list(zip(UserTags, TimeStamps, Tweets)), columns=['UserTags', 'time', 'Tweets'])
    csv_file = f"static\\csv_files\\tweets{hashtag}.csv"
    excel_file = f"static\\excel_files\\tweets{hashtag}.xlsx"
    df.to_csv(csv_file, index=False)
    df.to_excel(excel_file, index=False)

    driver.quit()
    
    return "tweets"+hashtag+".csv"




## this is for login and inspect the 

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import time

def search_byname(name):
    """
    Function to log in and extract data (username, date, and tweet text) from Twitter based on a username.
    """
    
    if '@' in name:
        name = name.replace('@', '')

    PATH = 'C:\\Users\\hp\\Downloads\\edge_driver\\msedgedriver.exe'
    
    service = Service(PATH)
    driver = webdriver.Edge(service=service)

    url = 'https://x.com/i/flow/login'
    driver.get(url)

    # Setup the login
    time.sleep(6)
    username = driver.find_element(By.XPATH, "//input[@name='text']")
    username.send_keys("jadir99")
    next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
    next_button.click()

    time.sleep(3)
    password = driver.find_element(By.XPATH, "//input[@name='password']")
    password.send_keys('jadir99jadir99')
    time.sleep(3)
    log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
    log_in.click()
    time.sleep(3)
    url = f"https://twitter.com/{name}"
    driver.get(url)

    UserTags = []
    TimeStamps = []
    Tweets = []

    while len(Tweets) <= 50:
        # Find all the tweet article elements on the page
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        # Extract data from each article
        for article in articles:
            try:
                UserTag = article.find_element(By.XPATH, ".//div[@dir='ltr']//span").text
                TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

                UserTags.append(UserTag)
                TimeStamps.append(TimeStamp)
                Tweets.append(Tweet)
            except NoSuchElementException:
                continue        
            except StaleElementReferenceException:
                continue

        time.sleep(1)
        # Scroll down to the bottom of the page
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(3)  # Wait for the page to load more articles

    # Create a DataFrame and save to CSV and Excel
    df = pd.DataFrame(list(zip(UserTags, TimeStamps, Tweets)), columns=['UserTags', 'time', 'Tweets'])
    csv_file = f"static\\csv_files\\tweets{name}.csv"
    excel_file = f"static\\excel_files\\tweets{name}.xlsx"
    df.to_csv(csv_file, index=False)
    df.to_excel(excel_file, index=False)

    driver.quit()
    
    return csv_file













# beggin of cleaning the data :

#function for make data logic for machine  dont => do not
def replace_contractions(text):
    return contractions.fix(text)

#function to remove hashtags and mensioons in and urls :
def remove_hashtags_mentions_URLS(text):
    without_hashtag=re.sub(r'#\S*','',str(text))
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
    df=pd.read_csv("static\\csv_files\\"+str(path))
    # make all lower 
    df['Tweets']=df['Tweets'].str.lower()
    df['UserTags']=df['UserTags'].str.lower()

    # make correige les faux d'ortographe 
    # df['Tweets']=df['Tweets'].apply(lambda x:replace_contractions(str(x)))

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
    # df['Tweets']=df['Tweets'].apply(lambda x:stemming(x))
      
    # save modification
    df.to_csv(path, index=False)

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

