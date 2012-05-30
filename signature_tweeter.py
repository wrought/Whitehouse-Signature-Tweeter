#!/usr/bin/python

from time import gmtime, strftime, strptime
import sys
#import requests
#import json
#from bs4 import BeautifulSoup
from config import *
import os
import Queue
from parser import *
from tweeter import *

#open db connection
#import sqlite3
#conn = sqlite3.connect(database) # db defined in config.py
#c = conn.cursor()

# Start taking Logs
timestamp = strftime("%Y-%m-%d-%H:%M:%S")
log_name = "log-" + timestamp + ".log"
if not os.path.exists("log"):
    os.makedirs("log")
log = open("log/" + log_name, 'w')

twitter_Queue = Queue.Queue(100)
exit_event = threading.Event()


parser_thread = parser("parser", 20, wh_url_base, wh_url_id1, wh_url_id2, 
                       twitter_Queue, exit_event, database)
tweetbot = Tweeter(consumer_key, consumer_secret, access_token, access_token_secret, 
                   msg_preamble, msg_postamble, twitter_Queue, exit_event, 10)

parser_thread.start()
tweetbot.start()

raw_input("Press enter to end . . .")
exit_event.set()

log.close()

######################## EXTRA INFO #########################

# Sample of format of signatures from http request response
'''
<div class="name">Robert G</div><!--/name-->
<div class="details">
Los Angeles, CA<br/>
May 23, 2012<br/>
Signature # 13,711    </div>
</div>, <div class="entry entry-reg ">
<div class="name">Trystan G</div><!--/name-->
<div class="details">
<br/>
May 23, 2012<br/>
Signature # 13,710    </div>
</div>, <div class="entry entry-reg ">
<div class="name">Vinay S</div><!--/name-->
<div class="details">
Carmel, IN<br/>
May 23, 2012<br/>
Signature # 13,709    </div>
</div>
'''
