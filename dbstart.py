#!/usr/bin/python

from config import *
import sys 

import sqlite3
conn = sqlite3.connect(database)
c = conn.cursor()

"""
initialize sqlite table
table name: signatures
sig_id The primary key for the table
page The text identifier for the url where the entry came from
sig_num the signature number as described on whitehouse
first_name the signatory's first name
last_initial the signatory's last initial
location_city the signatory's city
location_state the signatory's state
location_other holds nonstandard locations when only thing available
time_added GMT timestamp for when the entry is recorded
"""
try:
    c.execute('''
CREATE TABLE signatures
(sig_id INTEGER PRIMARY KEY ASC
,page TEXT
,sig_num INTEGER
,first_name TEXT
,last_initial TEXT
,sig_date DATE
,location_city TEXT
,location_state TEXT
,location_other TEXT
,time_added DATETIME)''')

except sqlite3.OperationalError:
    print "\n Error: You probably already have a signatures table in \"" + database + "\" database...\n"
    print sys.exc_info()[1]

try:
    c.execute('''
CREATE TABLE locations
(loc_id INTEGER PRIMARY KEY ASC
,location_city TEXT
,location_state TEXT)''')
except sqlite3.OperationalError:
    print "\n Error: You probably already have a locations table in \"" + database + "\" database...\n"
    print sys.exc_info()[1]

try:
    c.execute('''
CREATE TABLE responses
(r_id INTEGER PRIMARY KEY ASC
,loc_id INTEGER
,response TEXT
,service TEXT
,FOREIGN KEY(loc_id) REFERENCES locations(loc_id))''')
except sqlite3.OperationalError:
    print "\n Error: You probably already have a responses \"" + database + "\" database...\n"
    print sys.exc_info()[1]
