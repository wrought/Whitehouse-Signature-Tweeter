#!/usr/bin/python

from time import strftime
import sys
import requests
import json
from bs4 import BeautifulSoup
from config import *

import sqlite3
conn = sqlite3.connect(database) # db defined in config.py
c = conn.cursor()

# Some useful values
timestamp = strftime("%Y-%m-%d-%H:%M:%S")

# Create White House URL from components (defined in config.py)
wh_url = wh_url_base + wh_url_id1  + "/" + str(wh_url_num) + "/" + wh_url_id2

# call curl command (make http get request)
r = requests.get(wh_url)
response = r.content
status_code = r.status_code

# Break out JSON payload (all values)
response = json.loads(response)["markup"]

soup = BeautifulSoup(response)

'''
the_text = soup.get_text()
the_text = the_text.replace('/name',"").replace("      ","")
'''

# print soup
for entry in soup.find_all("div", {"class" : "entry-reg"}):
    the_name = entry.div.string
    # save the_name to the sqlite db

    # Debug:
    print "\n" + str(the_name).replace("  "," ").replace("   "," ")

    # break up details into component pieces
    the_details = entry.find("div", {"class" : "details" }).get_text().replace("      ","").replace("    ","")
    the_details = the_details.split('\n')
    # months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    location = the_details[1].split(',')
    #Debug:
    print location
    if len(location) > 1:
        city = location[0]
        state = location[1].replace(" ","")
        # Debug
        print city + " " + state
        # save city and state to sqlite db

    if len(location) == 1:
        state = location[0]
        print state
        # save state (likely country)
    full_date = the_details[2].split()
    month = full_date[0]
    day = full_date[1].replace(",","")
    year = full_date[2]

    # Debug:
    print month + " " + day + " " + year

    full_sig = the_details[3].split()
    sig_num = int(full_sig[2].replace(',',''))
    # Debug:
    print sig_num

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

# Store data in signatures.db

    # first, clean payload
#for sig in payload:
    # Need regex for patterns:
    # "\n \n \n \n" to separate signatures
    # " <\/div>\n \n <\/div>\n \n" to be removed
    # "<\/div>\n"
    # This might be the regex of bad stuff: (\\n|<\\/div>| <\\/div>|\\n | \\n)

# "      " is the space separation


    # Use HTML library to grab cotents of identified div elements
    # Oddly, these elements have double-quotes escaped... could
    # run a python funct to clean that too, may not need to...

    # Check if we have this entry in the DB. If not, add it.

# Output into a reasonable format, e.g. RSS, JSON, etc.

# Send out a tweet (if it's new!!!!!)

