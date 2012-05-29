#!/usr/bin/python

import tweepy
import threading
import Queue

class Tweeter(threading.Thread):
    
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
    
    def __init__(self, c_key, c_sec, a_tok, a_tok_s, q)
        threading.Thread.__init__(self)
        self.consumer_key = c_key
        self.consumer_secret = c_sec
        self.access_token = a_tok
        self.access_token_secret = a_tok_s
        
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = tweepy.API(self.auth)
        
        #test to see if logged in
        print self.api.me().name

        self.q = q
        self.exitFlag = False

        self.msg_preamble = "#oamonday just signed by "
        self.msg_postamble = " bit.ly/J7tSiV"
    
    #TODO
    def run(self):
        while not exitFlag:
            people = ""
            rightLength = False
            while not rightLength:
                currentLength = len(msg_preamble + people + msg_postamble)
                next_person = self.q[-1]
                nextLength = len(msg_preamble + add_to_msg(people, next_person) + ms_postamble)
                
    
    def add_to_msg(self, items, next_item):
        if len(items) == 0:
            return next_item
        else:
            return items + ', ' + next_item

    def tweet(self, message):
        self.api.update_status(message)
