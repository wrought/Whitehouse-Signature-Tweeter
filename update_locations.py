#!/usr/bin/python

from geopy import geocoders
import logging
from config import *
import sqlite3
import time

conn = sqlite3.connect(database)
c = conn.cursor()

res = c.execute('''
SELECT 
    s.location_city,
    s.location_state
FROM signatures as s

LEFT OUTER JOIN locations as l
    ON l.location_city = s.location_city
    AND l.location_state = s.location_state

WHERE l.loc_id IS NULL

GROUP BY s.location_city, s.location_state 
limit 5
''')

# @TODO

#while row is not None:
#   locations.append(row)

locations = []
for row in col:
    insert_values = "(null, :city, :state)"
    loc_dict = {"city": loc[0],
                "state": loc[1]}
    c.execute("INSERT INTO locations VALUES " + insert_values, loc_dict)
    logger.info("Inserting... city: " + loc_dict[0] + " state: " + loc_dict[1])
    conn.commit()

c.close()

