import os
import tweepy
from nameko.rpc import rpc

def create_api():
    consumer_key = os.environ.get('TWITTER_API_KEY')
    consumer_secret = os.environ.get('TWITTER_API_SECRET_KEY')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print(e)        

    return api


class TweetClass:
    name = 'tweetbot_service'
    
    @rpc
    def create(self, tweet_message):
        api = create_api()
        api.update_status(tweet_message)

        return 'Tweet Successful'

        
        
