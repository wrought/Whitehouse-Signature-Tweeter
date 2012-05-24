#!/usr/bin/python

from time import strftime
import sys
import requests
import json
from bs4 import BeautifulSoup

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
for entry in soup.find_all("div", {"class" : "entry entry-reg "}):
   the_name = entry.div.string
   print str(the_name) + '\n'
   the_details = entry.find("div", {"class" : "details" }).get_text().replace("      ","")
   print str(the_details) + '\n'

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

