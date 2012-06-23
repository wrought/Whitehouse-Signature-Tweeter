#!/usr/bin/python

from geopy import geocoders
import logging
from config import *
import sqlite3
import time

# start logging
logger = logging.getLogger('geocoder')

# Uses geopy to create objects for each service

googl = geocoders.Google()

yahoo = geocoders.Yahoo('Need App ID')
dotus = geocoders.GeocoderDotUS()
geona = geocoders.GeoNames()
wikip = geocoders.MediaWiki("http://en.wikipedia.org/wiki/%s")

# Replace this with sqlite query of unique locations
#locations = ["Los Angeles, CA", "Hoboken, NJ", ", FL", "Ontario, CA"]

print database

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
for row in c:
    locations.append(row)

insert_values = "(null, :city, :state, :lat, :long)"
# loop through locations, make request and store in db only if needed
for loc in locations:
    loc_dict = {"city": loc[0],
                "state": loc[1],
                "lat": None,
                "long": None}
    try: 
        loc_s = "%s, %s" % (loc[0], loc[1])
        geocode_result = googl.geocode(loc_s, exactly_one=False)
        for geocode_entry in geocode_result:
            loc_dict = {"city": loc[0],
                        "state": loc[1],
                        "lat": None,
                        "long": None}
            place, (lat, lng) = geocode_entry
            loc_dict['lat'] = lat
            loc_dict['long'] = lng
            print geocode_entry
            logger.info(geocode_result)
            c.execute("INSERT INTO locations VALUES " + insert_values, loc_dict)
            conn.commit()
            time.sleep(.1)
    except Exception as e:
        print "\n\nSomething goofy, logging...\n\n"
        print e
        logger.exception(e)
    # store in DB here

c.close

