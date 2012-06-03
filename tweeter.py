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
    
    def __init__(self, c_key, c_sec, a_tok, a_tok_s, msg_preamble, msg_postamble, 
                 q, signature_count, exit_event, delay):
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
        self.signature_count = signature_count
        self.exit_event = exit_event
        self.exitflag = False

        self.delay = delay

        self.msg_preamble = msg_preamble
        self.msg_postamble = msg_postamble
    
    # @TODO
    def run(self):
        old_next_person = None
        while not self.exitflag:
            people = ""
            rightlength = False
            while not rightlength and not self.exit_event.wait(0):
                next_person = None
                if old_next_person == None:
                    #print "DEBUG: tweeter: q.empty()=" + str(self.q.empty())
                    if not self.q.empty():
                        next_person = self.q.get()
                    else:
                        pass
                        #print "DEBUG: tweeter: nothing in q"
                else:
                    next_person = old_next_person
                    old_next_person = None
                
                #throw out names that are too long
                if (next_person == None) or (len(next_person) > 40):
                    next_person = None
                
                if next_person != None:
                    print "DEBUG: tweeter: adding person: " + next_person
                    currentlength = len((self.msg_preamble % self.signature_count.get()) 
                                        + people + self.msg_postamble)
                    nextlength = len((self.msg_preamble % self.signature_count.get()) 
                                     + self.add_to_msg(people, next_person) + self.msg_postamble)
                    if nextlength > 120:
                        old_next_person = next_person
                        rightlength = True
                    else:
                        people = self.add_to_msg(people, next_person)
                else:
                    if self.exit_event.wait(1):
                        self.exit()
                print "DEBUG: tweeter: msg = " + self.msg_preamble + people + self.msg_postamble
            if not self.exitflag:
                self.tweet((self.msg_preamble % self.signature_count.get()) 
                           + people + self.msg_postamble)
            if self.exit_event.wait(self.delay):
                self.exit()
        print "Exiting: tweeter"
    
    def add_to_msg(self, items, next_item):
        if len(items) == 0:
            return next_item
        else:
            return items + ', ' + next_item
    
    def exit(self):
        self.exitflag = True
    def tweet(self, message):
        # Debugging
        print "Your tweet: " + message
        # Alternative
        self.api.update_status(message)
