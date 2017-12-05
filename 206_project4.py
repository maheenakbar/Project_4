import urllib
import facebook
import json
import sqlite3
import sys
from instagram.client import InstagramAPI

token = 'EAACIVYZCGWFwBAFe968IMYz8H6ycjYi6lKhOBnmnlYrrNGtj4zti9z2BJZCJb8IS7O9hVMfenUOQoeQf64xoP5mKqiwXT6BVLyo5ULsqQsd2M7ZCVCWKAivaMhLjAV8THAHScYjlN4jQa35NUAOMqOcMrBf8poptdZB0re0BZCwZDZD'
graph = facebook.GraphAPI(access_token = token, version = 2.11)
#app_id = '149901065738332'
#app_secret = '662d87f8853356f1826e02c1a0ae7e70'
#extended_token = graph.extend_access_token(app_id, app_secret)
#print (extended_token)
profile = graph.get_object('me', fields = 'name,location')
print(json.dumps(profile, indent = 4))

CACHE_FNAME = "206_project4_fb_cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

friends = graph.get_connections(id='me', connection_name='friends')
print(json.dumps(friends, indent = 4))


# I got the following code from this link: https://github.com/facebookarchive/python-instagram/blob/master/get_access_token.py
# It is how I got the access code in order to use the Instagram API, and I was lead to that github file from the following 
# link: http://www.pygopar.com/playing-with-instagrams-api/

'''client_id = '3b55954ddb6c41719e92bd2a8466fe50'
client_secret = 'd6af984c736f425996c91c3b96de266d'
redirect_uri = 'http://www.google.com'
scope = ['basic', 'comments', 'follower_list', 'likes', 'public_content']

insta_api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = insta_api.get_authorize_login_url(scope = scope)

code = 'dbe77ddeec1a495199660a90559a449d'
access_token = insta_api.exchange_code_for_access_token(code)'''

'''if len(sys.argv) > 1 and sys.argv[1] == 'local':
    try:
        from test_settings import *

        InstagramAPI.host = test_host
        InstagramAPI.base_path = test_base_path
        InstagramAPI.access_token_field = "access_token"
        InstagramAPI.authorize_url = test_authorize_url
        InstagramAPI.access_token_url = test_access_token_url
        InstagramAPI.protocol = test_protocol
    except Exception:
        pass

# Fix Python 2.x.
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass



client_id = input("Client ID: ").strip()
client_secret = input("Client Secret: ").strip()
redirect_uri = input("Redirect URI: ").strip()
raw_scope = input("Requested scope (separated by spaces, blank for just basic read): ").strip()
scope = raw_scope.split(' ')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope = scope)

print ("Visit this page and authorize access in your browser: "+ redirect_uri)

code = (str(input("Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)'''
#print ("access token: " )
#print (access_token)

# This is the end of the code that I got online from the github file
