#!/usr/bin/python

from time import gmtime, strftime, strptime
import sys
import requests
import json
from bs4 import BeautifulSoup
from config import *
import os

#open db connection
import sqlite3
conn = sqlite3.connect(database) # db defined in config.py
c = conn.cursor()

# Start taking Logs
timestamp = strftime("%Y-%m-%d-%H:%M:%S")
log_name = "log-" + timestamp + ".log"
if not os.path.exists("log"):
    os.makedirs("log")
log = open("log/" + log_name, 'w')

page_num = wh_url_num
previous_change_made = True

while wh_url_id2 != '' and previous_change_made:
    # Create White House URL from components (defined in config.py)
    wh_url = wh_url_base + wh_url_id1  + "/" + str(page_num) + "/" + wh_url_id2
    print "nextURL: " + str(page_num) + "/" + wh_url_id2
    log.write("nextURL: " + str(page_num) + "/" + wh_url_id2 + "\n")
    # call curl command (make http get request)
    r = requests.get(wh_url)
    response = r.content
    status_code = r.status_code

    # Break out JSON payload (all values)
    response = json.loads(response)["markup"]

    soup = BeautifulSoup(response)

    previous_change_made = False # @TODO

    #print soup
    for entry in soup.find_all("div", {"class" : "entry-reg"}):
        signature_dict = { "page":None, 
                           "sig_num":None,
                           "first_name":None,
                           "last_initial":None,
                           "sig_date":None,
                           "location_city":None,
                           "location_state":None,
                           "location_other":None,
                           "time_added": None}

        signature_dict['page'] = wh_url_id2
        #first and last name
        the_name = entry.div.string
        clean_name = the_name.replace("  "," ").replace("   "," ")
        if not "@" in clean_name:
            signature_dict['first_name'] = clean_name.split(' ')[0]
	else:
            signature_dict['first_name'] = clean_name.split('@')[0]
        name_length = len(clean_name)
        if name_length > 1:
            clean_name_split = clean_name.split(' ')
            clean_name_split.remove(clean_name_split[0])
            signature_dict['last_initial'] = " ".join(clean_name_split)
        else:
            print "No last initials provided"
            log.write("No last initials provided\n")
        print "\n" + clean_name
        log.write("\n" + clean_name.encode('utf-8') + "\n")

        # break up details into component pieces
        the_details = entry.find("div", {"class" : "details" }).get_text().replace("      ","").replace("    ","")
        the_details = the_details.split('\n')
        # months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
        location = the_details[1].split(',')

        #location
        if len(location) > 1:
            signature_dict['location_city'] = location[0]
            signature_dict['location_state'] = location[1].replace(" ","")
            # Debug
            print signature_dict['location_city'] + " " + signature_dict['location_state']
            log.write(signature_dict['location_city'].encode('utf-8') + " " + signature_dict['location_state'].encode('utf-8') + "\n")
        elif len(location) == 1:
            signature_dict['other_location'] = location[0]
            print signature_dict['other_location']
            log.write(signature_dict['other_location'].encode('utf-8') + "\n")
        else:
            print "Location parsing error with: " + location
            log.write("Location parsing error with: " + location.encode('utf-8') + "\n")
        full_date = the_details[2].split()
        month = full_date[0]
        day = full_date[1].replace(",","")
        year = full_date[2]
        
        strp_sig_date = strptime(year + ' ' + month + ' ' + day, "%Y %B %d")
        signature_dict['sig_date'] = strftime("%Y-%m-%d %H:%M:%S", strp_sig_date)

        # Debug:
        print month + " " + day + " " + year
        log.write(month + " " + day + " " + year + "\n")

        full_sig = the_details[3].split()
        signature_dict['sig_num'] = full_sig[2].replace(',','')
        # Debug:
        print signature_dict['sig_num']
        log.write(signature_dict['sig_num'] + "\n")

        #database insertion
        #verify that signature doesn't exist already
        query = "SELECT signatures.sig_num FROM signatures WHERE signatures.sig_num =  " + signature_dict['sig_num']
        c.execute(query)
        row = c.fetchone()
        if (row == None):
            print "DB: " + signature_dict['sig_num'] + " not found"
            log.write("DB: " + signature_dict['sig_num'] + " not found\n")
            #Add signature to the DB
            signature_dict['time_added'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_values = "(null, :page, :sig_num, :first_name, :last_initial, :sig_date, :location_city, :location_state, :location_other, :time_added)"
            c.execute("INSERT INTO signatures VALUES " + insert_values, signature_dict) 
            previous_change_made = True
        else: 
            print "DB: " + signature_dict['sig_num'] + " found"
            log.write("DB: " + signature_dict['sig_num'] + " found\n")

    anchors = soup.find_all("a", {"class" : "load-next"})

    if len(anchors) == 1:
        anchor = anchors[0]
        wh_url_id2 = anchor.get('href').split('last=')[1]
        page_num += 1
    else:
        print "nextURL: not found"
        log.write("nextURL: not found\n")
        wh_url_id2 = ''

    if complete_flag:
        previous_change_made = True 
 
# commit changes to the database, close the cursor, and close log
conn.commit()
c.close()
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
