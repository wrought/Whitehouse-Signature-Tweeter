#!/usr/bin/python

import sys
import logging
from config import *
import sqlite3

'''
migrates signatures table
adds: FK loc_id to locations
removes: location_other
'''

# Connect to db
conn = sqlite3.connect(database)
c = conn.cursor()

# start logging
logger = logging.getLogger('main.db_migration_2')

c.execute('''
CREATE TRIGGER update_FK_loc_id_signatures AFTER INSERT ON locations 
  BEGIN
    UPDATE signatures SET loc_id = NEW.loc_id 
    WHERE UPPER(location_city) = UPPER(NEW.location_city)
      AND UPPER(location_state) = UPPER(NEW.location_state);
  END;''')

conn.commit()
c.close()
