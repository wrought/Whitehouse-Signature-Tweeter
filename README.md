Just a first trial.

##Instructions##

1.	Go to https://dev.twitter.com to make an app.  Be sure to generate your oauth token _after_ you change your app's permissions to read & write

2.	fill in details in config.py.bp and rename to config.py

3.	initialize the database

	    $dbstart.py

4.	Then run signature_tweeter.py to see it in action

	    $signature_tweeter.py

5.	Check out the resulting database by:
      
	    $sqlite3 signatures.db

Pretty nifty!

##Checkout:##

*	https://wwws.whitehouse.gov/petitions/!/petition/require-free-access-over-internet-scientific-journal-articles-arising-taxpayer-funded-research/wDX82FLQ
*	and some data: https://wwws.whitehouse.gov/petition-tool/signatures/more/4fafe312709f037653000011/1/4fbbf03b2ee8d0a55900005f
