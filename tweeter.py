#!/usr/bin/python

import tweepy

class Tweeter:
    
# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key=""
    consumer_secret=""

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
    access_token=""
    access_token_secret=""

    auth = ""
    api = ""
    
    def __init__(self, c_key, c_sec, a_tok, a_tok_s):
        self.consumer_key = c_key
        self.consumer_secret = c_sec
        self.access_token = a_tok
        self.access_token_secret = a_tok_s
        
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = tweepy.API(self.auth)
        
        #test to see if logged in
        print self.api.me().name

    def tweet(self, message):
        self.api.update_status(message)
