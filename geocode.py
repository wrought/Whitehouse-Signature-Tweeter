#!/usr/bin/python

from geopy import geocoders
import logging
import config
import sqlite3

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

conn = sqlite3.connect(database)
c = conn.cursor()

c.execute('''
SELECT 
    d.location_city,
    d.location_state
FROM locations as l

LEFT JOIN
    (
    SELECT
        location_city,
        location_state,
    FROM signatures
    GROUP BY location_city, location_state
    ) as d
    ON l.location_city = d.location_city
    AND l.location_state = d.location_state

WHERE l.loc_id IS NULL 
''')


locations = []

# @TODO
'''
row = c.fetchone()
while row is not None:
    loc 
    locations.append(
'''
    
# loop through locations, make request and store in db only if needed
for loc in locations:
    try: 
        geocode_result = googl.geocode(loc, exactly_one=False)
        for geocode_entry in geocode_result:
             place, (lat, lng) = geocode_entry
             print geocode_entry
        logger.info(geocode_result)
    except Exception as e:
        print "\n\nSomething goofy, logging...\n\n"
        logger.exception(e)
    # store in DB here
