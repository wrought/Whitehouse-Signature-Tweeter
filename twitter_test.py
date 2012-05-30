#!/usr/bin/python

from tweeter import *
from config import *
import Queue
import time
import threading

twitterQueue = Queue.Queue(100)

exitEvent = threading.Event()

tweetbot = Tweeter(consumer_key, consumer_secret, access_token, access_token_secret, 
                   msg_preamble, msg_postamble, twitterQueue, exitEvent, 10)

tweetbot.start()

for i in range(30):
    print "DEBUG: MAIN: twitterQueue.put(Jack " + str(i) + ")"
    twitterQueue.put("Jack " + str(i))

#while not twitterQueue.empty():
#    print "DEBUG: MAIN: get:" + twitterQueue.get()

raw_input("press enter to exit . . . ")
exitEvent.set()


