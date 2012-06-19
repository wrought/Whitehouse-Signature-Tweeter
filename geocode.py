#!/usr/bin/python

from geopy import geocoders
import logging
import config

# start logging
logger = logging.getLogger('geocoder')

# Uses geopy to create objects for each service

googl = geocoders.Google()

yahoo = geocoders.Yahoo('Need App ID')
dotus = geocoders.GeocoderDotUS()
geona = geocoders.GeoNames()
wikip = geocoders.MediaWiki("http://en.wikipedia.org/wiki/%s")

# Replace this with sqlite query of unique locations
locations = ["Los Angeles, CA", "Hoboken, NJ", ", FL", "Ontario, CA"]

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
    #loc_sentence = "%s: %.5f, %.5f" % (place, lat, lng)
    #logger.info(loc_sentence)
    #print loc_sentence
    geocode_result = None

