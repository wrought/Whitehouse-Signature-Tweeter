#!/usr/bin/python


#This script finds the max signature number from the signatures db
#then goes through and picks out signature numbers that are missing
#in the signature table and writes them to standard output

import sqlite3
conn = sqlite3.connect('signatures.db')
c = conn.cursor()

c.execute("SELECT MAX(sig_num) FROM signatures")
sig_max = c.fetchone()[0]
print "Max(sig_num): " + str(sig_max)

c.execute('''
DROP TABLE IF EXISTS sig_num_range
''')

c.execute('''
CREATE TABLE sig_num_range
(sig_num INTEGER PRIMARY KEY ASC)''')

for i in range(sig_max):
    c.execute("INSERT INTO sig_num_range VALUES (null)")

c.execute('''
SELECT * from sig_num_range as r
LEFT JOIN signatures as s
ON s.sig_num = r.sig_num
WHERE s.sig_num IS NULL''')

row = c.fetchone()
while row:
    print row[0]
    row = c.fetchone()
    
conn.commit()
c.close()
