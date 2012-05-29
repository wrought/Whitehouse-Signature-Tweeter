#!/usr/bin/python

from tweeter import *
from config import *

tweetbot = Tweeter(consumer_key, consumer_secret, access_token, access_token_secret, msg_preamble, msg_postamble)

tweetbot.tweet("What's crappenin' world? This is Jack's new twitter bot")
