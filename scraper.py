import tweepy
import pandas as pd
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Twitter API credentials
API_KEY = 'Vux18RvLzcCz3UnQTkSJHvlR1'
API_SECRET_KEY = 'J3HPmAqU82YVp0PnRW8tqYvA0zs5GGIVIcSyZQpMGTwzqsDSGM'
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAANdzvQEAAAAAXM12uPe8pLCz8Cx5SPJ4BAS46Qc%3DI3cUV37apT6iq77tPZbZZBbRTBTamp1ZpszV7XEmb6La0q2udh'
ACCESS_TOKEN_SECRET = 'AAAAAAAAAAAAAAAAAAAAANdzvQEAAAAAXM12uPe8pLCz8Cx5SPJ4BAS46Qc%3DI3cUV37apT6iq77tPZbZZBbRTBTamp1ZpszV7XEmb6La0q2udh'

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Define the search query and date
query = "Indian Budget"
start_date = "2024-07-23"

# Fetch tweets
tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", since=start_date, tweet_mode='extended').items(1000)

# Store tweets in a DataFrame
tweet_list = [[tweet.full_text, tweet.created_at] for tweet in tweets]
df = pd.DataFrame(tweet_list, columns=["Tweet", "Timestamp"])

# Function to clean tweet text
def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)  # Remove URLs
    tweet = re.sub(r'@\S+', '', tweet)  # Remove mentions
    tweet = re.sub(r'#', '', tweet)  # Remove hashtags
    tweet = re.sub(r'\n', '', tweet)  # Remove line breaks
    tweet = re.sub(r'[^A-Za-z0-9 ]+', '', tweet)  # Remove special characters
    return tweet

# Clean the tweets
df['Cleaned_Tweet'] = df['Tweet'].apply(clean_tweet)

# Function to analyze sentiment
def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

# Apply sentiment analysis
df['Sentiment'] = df['Cleaned_Tweet'].apply(get_sentiment)

# Plot the sentiment distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='Sentiment', data=df, palette="coolwarm")
plt.title('Sentiment Analysis of Tweets on Indian Budget (Starting from July 23, 2024)')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Save the results to a CSV file
df.to_csv("budget_sentiment_analysis.csv", index=False)
