import urllib
import facebook
import json
import sqlite3

token = 'EAACIVYZCGWFwBAFyUkERkkpBZCI4NYZCH1OvtiPnLORypw3iNaf2nfTfj1qryO6v9ZCwa3oXzVBHlN3nwUqTeXsHSt0mZCXHqZCyDAwVWSxOxnudtbDyXl3Tfxs4uPwuBIZABoR4kH5XorOIdfMd8ZAA45H2DlbnMzSWhyvwPZAZAFIdda9S06QA8lNn0iOCjcOnMZD'
graph = facebook.GraphAPI(access_token = token, version = 2.11)

CACHE_FNAME = "206_project4_cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}


