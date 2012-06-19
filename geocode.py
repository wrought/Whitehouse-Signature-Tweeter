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
locations = ["Los Angeles, CA", "Hoboken, NJ", ", FL"]

# loop through locations, make request and store in db only if needed
for loc in locations:
    place, (lat, lng) = googl.geocode(loc)
    # store in DB here
    loc_sentence = "%s: %.5f, %.5f" % (place, lat, lng)
    logger.info(loc_sentence)
    print loc_sentence

