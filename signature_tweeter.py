#!/usr/bin/python

from time import strftime
import sys
import requests
import json

import sqlite3
conn = sqlite3.connect('signatures.db')
c = conn.cursor()

# Some useful values
timestamp = strftime("%Y-%m-%d-%H:%M:%S")

# Grab data from whitehouse.gov petition
wh_url_base = "https://wwws.whitehouse.gov/petition-tool/signatures/more/"
wh_url_id1 = "4fafe312709f037653000011"
wh_url_num = 1
wh_url_id2 = "4fbb32994bd504422b000039" # This one gets updated, don't ignore these

wh_url = wh_url_base + wh_url_id1  + "/" + str(wh_url_num) + "/" + wh_url_id2

# call curl command
payload = {}
r = requests.get(wh_url)
response = r.content
status_code = r.status_code

# Break out JSON payload (all values)
print r.status_code

# Store data in signatures.db

    # Check if we already have this page
    # If not, start to go through the page, saving entries to DB
    # 

# Send out a tweet (if it's new!!!!!)

