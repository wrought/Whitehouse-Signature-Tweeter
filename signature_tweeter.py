#!/usr/bin/python

from time import strftime
import sys
import requests
import json
from bs4 import BeautifulSoup

#dictionary to convert month strings to ints
months = {'January': 1, 'February': 2, 'March': 3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

#open db connection
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
    # save the_name to the sqlite db

    # Debug:
    print "\n" + str(the_name)
    
    first_name = the_name.split(' ')[0]
    last_name = the_name.split(' ')[1]

    # break up details into component pieces
    the_details = entry.find("div", {"class" : "details" }).get_text().replace("      ","").replace("    ","")
    the_details = the_details.split('\n')
    # months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    location = the_details[1].split(',')
    if location[0] != "":
        city = location[0]
        state = location[1].replace(" ","")

        # Debug
        print city + " " + state
    else:
        city = ""
        state = ""
        # save city and state to sqlite db
    full_date = the_details[2].split()
    month = str(months[full_date[0]])
    day = full_date[1].replace(",","")
    year = full_date[2]
    sig_date = str(year) + '-' + month + '-' + day

    # Debug:
    print month + " " + day + " " + year

    full_sig = the_details[3].split()
    sig_num = int(full_sig[2].replace(',',''))
    # Debug:
    print sig_num

    #database insertion
    #verify that signature doesn't exist already
    query = "SELECT signatures.sig_num FROM signatures WHERE signatures.sig_num =  " +  str(sig_num)
    c.execute(query)
    row = c.fetchone()
    if (row == None):
        print str(sig_num) + " not found"
        #Add signature to the DB
        if (city != ""):
            c.execute("INSERT INTO signatures VALUES (null,?, ?, ?, ?, ?, ?, ?)", (wh_url_id2, str(sig_num), first_name, last_name, sig_date, city, state)) 
        else:
            c.execute("INSERT INTO signatures VALUES (null,?, ?, ?, ?, ?, null, null)", (wh_url_id2, str(sig_num), first_name, last_name, sig_date))
    else:
        print str(sig_num) + " found"

#commit changes to the database and close the cursor        
conn.commit()
c.close()

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

