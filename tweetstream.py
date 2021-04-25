from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from wordcloud_gen import create_wordcloud
import pandas as pd
import numpy as np
import twitter_credentials
from PIL import Image

### twitter client ###
class TwitterClient():
    def __init__(self, twitter_user = None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

#twitter authenticator
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.ckey, twitter_credentials.csecret)
        auth.set_access_token(twitter_credentials.atoken, twitter_credentials.asecret)
        return auth

class TwitterStreamer():
    '''
    Class for streaming and processing live tweets
    '''
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #this handles twitter authentication and connection to twitter streaming api
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    '''
    This is a basic listener class that prints received tweets to stdout.
    '''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
            return True
        except BaseException as e:
            print("error on_data: %s" % str(e))
        return True

    def on_error(self, status): #status_code
        if status == 420:
            # Returning false on_data method in case rate limit occurs
            return False
        print(status)

class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing content from tweets
    '''
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns=['Tweets'])
        '''df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])'''
        #df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweet'] = np.array([tweet.retweet_count for tweet in tweets])

        return df
if __name__ == "__main__":
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    username = input("Enter username ( For example: realdonaldtrump , joe_sugg , narendramodi , etc.)")
    no_tweets = int(input("Enter number of tweets required"))
    tweets = api.user_timeline(screen_name=username, count=20)

    #print(dir(tweets[0]))
    #print(tweets[0].text)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print("Loading.....")
    print(df.head(no_tweets))

    textfile = ""
    for i in range(10):
        textfile += tweets[i].text
    print(textfile)
    create_wordcloud(textfile)
    Image.open("wc.png").show()



