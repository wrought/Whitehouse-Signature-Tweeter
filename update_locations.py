#!/usr/bin/python

from geopy import geocoders
import logging
from config import *
import sqlite3
import time

# Connect to db
conn = sqlite3.connect(database)
c = conn.cursor()

# start logging
logger = logging.getLogger('main.update_locations')

# Store response of query
res = c.execute('''
SELECT 
    upper(s.location_city),
    upper(s.location_state)
FROM signatures as s

LEFT OUTER JOIN locations as l
    ON l.location_city LIKE s.location_city
    AND l.location_state LIKE s.location_state

WHERE l.loc_id IS NULL

GROUP BY upper(s.location_city), upper(s.location_state)
''')

# @TODO

#while row is not None:
#   locations.append(row)

locations = []
for row in c:
    locations.append(row)

for loc in locations:
    insert_values = "(null, :city, :state)"
    loc_dict = {"city": loc[0],
                "state": loc[1]}
    c.execute("INSERT INTO locations VALUES " + insert_values, loc_dict)
    logger.info("Inserting... city: " + unicode(loc_dict["city"]) + " state: " + unicode(loc_dict["state"]))
    conn.commit()

c.close()

