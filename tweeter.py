#!/usr/bin/python

import tweepy
import threading
from collections import deque

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
    
    def __init__(self, c_key, c_sec, a_tok, a_tok_s, d)
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

        self.d = d
        self.exitflag = False

        self.msg_preamble = "wh.gov petition just signed by "
        self.msg_postamble = ""
    
    # @TODO
    def run(self):
        while not exitflag:
            people = ""
            rightLength = False
            while not rightlength:
                currentlength = len(msg_preamble + people + msg_postamble)
                next_person = list(self.d)[-1]

            # @TODO add in lock here later, as well as one in the parser thread...

                nextlength = len(msg_preamble + add_to_msg(people, next_person) + msg_postamble)
                if nextlength > 140:
                    rightlength = True
                else:
                    people = self.add_to_msg(people, self.d.pop())
            self.tweet(msg_preamble + people + msg_postamble)
                
    
    def add_to_msg(self, items, next_item):
        if len(items) == 0:
            return next_item
        else:
            return items + ', ' + next_item

    def tweet(self, message):
        # Debugging
        print "Your tweet: " + message
        # Alternative
        # self.api.update_status(message)
