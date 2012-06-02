#!/usr/bin/python

import tweepy
import threading
import Queue
import logging

logger = logging.getLogger('tweeter')

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

#get logger
    
    
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

        self.q = q
        self.signature_count = signature_count
        self.exit_event = exit_event
        self.exitflag = False

        self.delay = delay

        self.msg_preamble = msg_preamble
        self.msg_postamble = msg_postamble

        logger.debug("constructed")
    # @TODO
    def run(self):
        old_next_person = None
        while not self.exitflag:
            people = ""
            rightlength = False
            while not rightlength and not self.exit_event.wait(0):
                next_person = None
                if old_next_person == None:
                    logger.debug("checking name queue . . .")
                    if not self.q.empty():
                        next_person = self.q.get()
                        logger.debug(". . . retrieved %s" % next_person)
                    else:
                        logger.debug(". . . nothing in queue")
                        pass
                        #print "DEBUG: tweeter: nothing in q"
                else:
                    logger.debug("bypassing queue and using %s" % old_next_person)
                    next_person = old_next_person
                    old_next_person = None
                
                #throw out names that are too long
                #short circuits if == None
                if (next_person == None) or (len(next_person) > 40):
                    logger.debug("name too long or None, throwing away")
                    next_person = None
                
                if next_person != None:
                    logger.debug("checking adding person to msg: " + next_person)
                    currentlength = len((self.msg_preamble % self.signature_count.get()) 
                                        + people + self.msg_postamble)
                    logger.debug("current msg length: %s" % currentlength)
                    nextlength = len((self.msg_preamble % self.signature_count.get()) 
                                     + self.add_to_msg(people, next_person) + self.msg_postamble)
                    logger.debug("possible next msg length: %s" % currentlength)
                    if nextlength > 120:
                        logger.debug("msg was already the correct length. Getting ready to tweet . . .")
                        logger.debug("stowing %s" % old_next_person)
                        old_next_person = next_person
                        rightlength = True
                    else:
                        logger.debug("adding %s to msg" % next_person)
                        people = self.add_to_msg(people, next_person)
                else:
                    if self.exit_event.wait(1):
                        self.exit()
                logger.debug('current tweet build: %s' % (self.msg_preamble % self.signature_count.get()) + people + self.msg_postamble) 
                #print "DEBUG: tweeter: msg = " + self.msg_preamble + people + self.msg_postamble
            if not self.exitflag:
                self.tweet((self.msg_preamble % self.signature_count.get()) 
                           + people + self.msg_postamble)
            if self.exit_event.wait(self.delay):
                self.exit()
        logger.info('exiting thread')
        print "Exiting: tweeter"
    
    def add_to_msg(self, items, next_item):
        if len(items) == 0:
            return next_item
        else:
            return items + ', ' + next_item
    
    def exit(self):
        logger.debug("initializing exit procedure")
        self.exitflag = True
    def tweet(self, message):
        # Debugging
        logger.info('tweeting msg: %s' % message)
        logger.debug('tweeting msg length: %s' % str(len(message)))
        if len(message) > 140:
            logger.error('tweet to long at %s characters.' % str(len(message)))
            return -1
        else:
            # print "Your tweet: " + message
            # Alternative
            self.api.update_status(message)
        logger.debug('tweet complete')
        return 0
        
