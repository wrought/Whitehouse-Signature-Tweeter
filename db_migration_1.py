#!/usr/bin/python

import sys
import logging
from config import *
import sqlite3

# Connect to db
conn = sqlite3.connect(database)
c = conn.cursor()

# start logging
logger = logging.getLogger('db_migration_1')

logger.info("renaming signatures to signatures_bu . . .")
try:
    c.execute("ALTER TABLE signatures RENAME to signatures_bu")
except Exception as e:
    logger.exception(e)
    sys.exit(1)

try:
    logger.info("making new signatures table")
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
,loc_id INTEGER
,time_added DATETIME
,FOREIGN KEY (loc_id) REFERENCES loc_id ''')

except Exception as e:
    logger.exception(e)
    c.execute("ALTER TABLE signatures_bu RENAME to signatures")
    logger.info("renaming signatures_bu to signatures")
    sys.exit(1)

try:
    logger.info("pulling data out of signatures_bu")
    c.execute('''
INSERT INTO signatures VALUES
(
  SELECT
    NULL AS sig_id,
    s.page,
    s.sig_num,
    s.first_name,
    s.last_initial,
    s.sig_date,
    s.location_city,
    s.location_state,
    s.NULL as loc_id,
    s.time_added
  FROM signatures_bu AS s
)''')

except Exception as e:
    logger.exception(e)
    c.execute("DROP TABLE signatures")
    c.execute("ALTER TABLE signatures_bu RENAME to signatures")
    logger.info("renaming signatures_bu to signatures")
    sys.exit(1)
       



