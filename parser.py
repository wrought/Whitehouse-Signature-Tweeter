#!/usr/bin/python

from time import *
import time
import sys
import requests
import json
from bs4 import BeautifulSoup
import os
import Queue
import threading
import sqlite3
import logging
from config import *

logger = logging.getLogger('parser')

class parser(threading.Thread):
    
    def __init__(self, name, delay, wh_url_base, wh_url_id1, starting_page, q, signature_count, exit_event, db):
        threading.Thread.__init__(self)
        self.delay = delay
        self.wh_url_base = wh_url_base
        self.wh_url_id1 = wh_url_id1
        self.starting_page = starting_page
        self.signature_count = signature_count
        self.q = q
        self.exit_event = exit_event
        self.exitFlag = False
        self.db = db
        
        self.conn = sqlite3.connect(self.db, check_same_thread = False)
        self.c = self.conn.cursor()
        logger.debug("constructed")
    
    def create_db_connection(self):
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        logger.debug("sqlite connection created")

    def run(self):
        while not self.exitFlag:
            next_page = self.starting_page
            page_num = 1
            previous_changes_made = True
            while next_page != '' and (previous_changes_made or complete_flag) and not self.exit_event.wait(0):
                #print "THREAD: parser: requesting . . ."
                soup = self.get_soup(page_num, next_page)
                if soup != -1:
                    previous_changes_made = False
                    #print "THREAD: parser: parsing . . ."
                    for entry in soup.find_all("div", {"class" : "entry-reg"}):
                        signature_dict = self.parse_entry(entry, next_page)
                        #print "THREAD: parser: writing . . ."
                        new = self.write_db(signature_dict)
                        if new:
                            #Write to tweeter Queue here
                            logger.debug("adding %s %s to the queue" % (signature_dict['first_name'], signature_dict['last_initial']))
                            self.q.put(signature_dict['first_name'] + ' ' + signature_dict['last_initial'])
                            logger.debug("updating signature_count . . .")
                            if signature_dict['sig_num'] > self.signature_count.get():
                                logger.info("new max signature count: %s" % signature_dict['sig_num'])
                                self.signature_count.set(signature_dict['sig_num'])
                            previous_changes_made = True
                    page_num += 1
                    next_page = self.get_next_page(soup)
            if self.exit_event.wait(self.delay):
                self.exit()
        logger.debug("closing sqlite connection . . .")
        self.c.close()
        logger.info('exiting thread')
        print "Exiting: parser"
    
    def exit(self):
        logger.debug("initializing exit procedure . . .")
        self.exitFlag = True
    
    #takes the page number and page, grabs json, returns soup
    def get_soup(self, page_num, page):
        wh_url = self.wh_url_base + self.wh_url_id1 + "/" + str(page_num) + "/" + page
        logger.debug("requesting %s" % wh_url)
        try:
            r = requests.get(wh_url, timeout = 3)
        except:
            print "THREAD: parser: requests.get() timed out"
            logger.warning("request to %s timed out" % wh_url)
            return -1
        logger.debug("get() successful")
        response = r.content
        status_code = r.status_code
        
        payload = json.loads(response)["markup"]        
        soup = BeautifulSoup(payload)
        logger.debug("soup created successfully")
        return soup

    #takes a signature_dict
    #returns True if it didn't find the sig_num and wrote the signature to the db
    #returns False otherwise
    def write_db(self, signature_dict):
        #database insertion
        #verify that signature doesn't exist already
        #print "THREAD: parser: querying . . ."
        query = "SELECT signatures.sig_num FROM signatures WHERE signatures.sig_num =  " + signature_dict['sig_num']
        self.c.execute(query)
        row = self.c.fetchone()
        if (row == None):
            print "DB: " + signature_dict['sig_num'] + " not found"
            logger.info("DB: " + signature_dict['sig_num'] + " not found")
            #Add signature to the DB
            signature_dict['time_added'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            insert_values = "(null, :page, :sig_num, :first_name, :last_initial, :sig_date, :location_city, :location_state, :location_other, :time_added)"
            logger.info("inserting %s: %s %s" % (signature_dict['sig_num'], 
                                                  signature_dict['first_name'], 
                                                  signature_dict['last_initial']))
            self.c.execute("INSERT INTO signatures VALUES " + insert_values, signature_dict)
            logger.debug("inserted. commiting . . .")
            self.conn.commit()
            return True
        else: 
            print "DB: " + signature_dict['sig_num'] + " found"
            logger.info("DB: " + signature_dict['sig_num'] + " found")
            return False

    #takes a signature entry, gives a signature_dict
    def parse_entry(self, entry, page):
        signature_dict = { "page":None, 
                       "sig_num":None,
                       "first_name":None,
                       "last_initial":None,
                       "sig_date":None,
                       "location_city":None,
                       "location_state":None,
                       "location_other":None,
                       "time_added": None}
        logger.debug("parsing signature entry")
        #page
        signature_dict['page'] = page

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
            logger.debug("No last initials provided\n")
        print "\n" + clean_name.encode('utf-8')
        logger.debug("name: " + clean_name.encode('utf-8'))

        # break up details into component pieces
        the_details = entry.find("div", {"class" : "details" }).get_text().replace("      ","").replace("    ","")
        the_details = the_details.split('\n')
        location = the_details[1].split(',')

        #location
        if len(location) > 1:
            signature_dict['location_city'] = location[0]
            signature_dict['location_state'] = location[1].replace(" ","")
            # Debug
            print signature_dict['location_city'] + " " + signature_dict['location_state']
            logger.debug("location: " + signature_dict['location_city'].encode('utf-8') + " " + signature_dict['location_state'].encode('utf-8'))
        elif len(location) == 1:
            signature_dict['other_location'] = location[0]
            print signature_dict['other_location']
            logger.debug("other location: " + signature_dict['other_location'].encode('utf-8'))
        else:
            print "Location parsing error with: " + location
            logger.warning("Location parsing error with: " + location.encode('utf-8') + "\n")
        full_date = the_details[2].split()
        month = full_date[0]
        day = full_date[1].replace(",","")
        year = full_date[2]
        
        strp_sig_date = strptime(year + ' ' + month + ' ' + day, "%Y %B %d")
        signature_dict['sig_date'] = strftime("%Y-%m-%d %H:%M:%S", strp_sig_date)

        # Debug:
        print month + " " + day + " " + year
        logger.debug("date: " + month + " " + day + " " + year)

        full_sig = the_details[3].split()
        signature_dict['sig_num'] = full_sig[2].replace(',','')
        # Debug:
        print signature_dict['sig_num']
        logger.debug("sig_num: " + signature_dict['sig_num'])

        logger.debug("parsing complete")
        return signature_dict
    
    #takes soup, returns next page to look at, null string if none
    def get_next_page(self, soup):
        logger.debug("finding next page")
        anchors = soup.find_all("a", {"class" : "load-next"})
        
        if len(anchors) == 1:
            anchor = anchors[0]
            wh_url_id2 = anchor.get('href').split('last=')[1]
            logger.debug("next page: %s" % wh_url_id2)
        else:
            print "nextURL: not found"
            logger.warning("nextURL: not found")
            wh_url_id2 = ''
        
        logger.debug("finding next page complete")
        return wh_url_id2




