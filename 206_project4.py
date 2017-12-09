import urllib
import facebook
import json
import sqlite3
import sys
from instagram.client import InstagramAPI

token = 'EAAOJEiXVpEMBAJJsR44JOWyJH6LRJZAiYqnZA7TqZAXKBZBHQZAvVqb8xYEFBS5QpWc9tzeY0oeseZBSxJYH5DSsD8II2pfZCdMUM0YXUbUp0m46DbyYZCA08Siibvf9TRpYGpUsaZBl8SyfaV6hQMq9Qdvpui6F8CBcZD'

graph = facebook.GraphAPI(access_token = token, version = 2.11)

CACHE_FNAME = "206_project4_fb_cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

month_dict = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September',
              '10': 'October', '11': 'November', '12': 'December'}
latitudes = []
longitudes = []

def get_events(key_word):
    word = 'events: ' + key_word
    if word in CACHE_DICTION:
        results = CACHE_DICTION[word]
    else:
        #gets last 100 instances of FB events with the given key word
        results = graph.search(q = key_word, type = 'event', limit = 100)
        CACHE_DICTION[word] = results
        f = open(CACHE_FNAME, "w")
        #updates the json file with whatever is in CACHE_DICTION
        f.write(json.dumps(CACHE_DICTION))
        f.close

    return results['data']

def get_connections(key_word):

    word = 'connections: ' + key_word

    if word in CACHE_DICTION:
        results = CACHE_DICTION[word]
    else:
        results = graph.get_connections(id = 'me', connection_name = key_word)
        CACHE_DICTION[word] = results
        f = open(CACHE_FNAME, "w")
        f.write(json.dumps(CACHE_DICTION))
        f.close

    return results['data']

party_data = get_events('party')
celebration_data = get_events('celebartion')
blowout_data = get_events('blowout')
festivity_data = get_events('festivity')
shindig_data = get_events('shindig')
my_posts = get_connections('posts')

party_months = {}
celebration_months = {}
blowout_months = {}
festivity_months = {}
shindig_months = {}

sorted_party_months = {}
sorted_celebration_months = {}
sorted_blowout_months = {}
sorted_festivity_months = {}
sorted_shindig_months = {}

conn = sqlite3.connect('206_project4.sqlite')
cur = conn.cursor()

# This part of the code creates the tables for each word related to
# 'party'
cur.execute('DROP TABLE IF EXISTS Party')
cur.execute('CREATE TABLE Party (name TEXT, date_time DATETIME, state TEXT, country TEXT, description TEXT, latitude NUMBER, longitude NUMBER)')

cur.execute('DROP TABLE IF EXISTS Celebration')
cur.execute('CREATE TABLE Celebration (name TEXT, date_time DATETIME, state TEXT, country TEXT, description TEXT, latitude NUMBER, longitude NUMBER)')

cur.execute('DROP TABLE IF EXISTS Blowout')
cur.execute('CREATE TABLE Blowout (name TEXT, date_time DATETIME, state TEXT, country TEXT, description TEXT, latitude NUMBER, longitude NUMBER)')

cur.execute('DROP TABLE IF EXISTS Festivity')
cur.execute('CREATE TABLE Festivity (name TEXT, date_time DATETIME, state TEXT, country TEXT, description TEXT, latitude NUMBER, longitude NUMBER)')

cur.execute('DROP TABLE IF EXISTS Shindig')
cur.execute('CREATE TABLE Shindig (name TEXT, date_time DATETIME, state TEXT, country TEXT, description TEXT, latitude NUMBER, longitude NUMBER)')


def add_data(event_item, dict_input):
    insert_list = [event_item['name'], event_item['start_time']]



    date = event_item['start_time'].split('-')
    month = date[1]

    if month_dict[month] in dict_input:
        dict_input[month_dict[month]] += 1
    else:
        dict_input[month_dict[month]] = 1

    if 'place' in event_item:
        if 'location' in event_item['place']:
            if 'latitude' in event_item['place']['location']:
                latitude_point = event_item['place']['location']['latitude']
                latitudes.append(latitude_point)
                longitude_point = event_item['place']['location']['longitude']
                longitudes.append(longitude_point)
            else:
                latitude_point = 'N/A'
                longitude_point = 'N/A'
            if 'state' in event_item['place']['location']:
                state = event_item['place']['location']['state']
            else:
                state = 'N/A'
            if 'country' in event_item['place']['location']:
                country = event_item['place']['location']['country']
            else:
                country = 'N/A'
        else:
            state = 'N/A'
            country = 'N/A'
            latitude_point = 'N/A'
            longitude_point = 'N/A'
    else:
        state = 'N/A'
        country = 'N/A'
        latitude_point = 'N/A'
        longitude_point = 'N/A'
    if 'description' in event_item:
        description = event_item['description']
    else:
        description = 'N/A'

    insert_list.append(state)
    insert_list.append(country)
    insert_list.append(description)
    insert_list.append(latitude_point)
    insert_list.append(longitude_point)

    return insert_list

def add_data_to_tables():
    for event in party_data:
        insert = add_data(event, party_months)
        cur.execute('INSERT INTO Party (name, date_time, state, country, description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)', insert)
        conn.commit()

    for event in celebration_data:
        insert = add_data(event, celebration_months)
        cur.execute('INSERT INTO Celebration (name, date_time, state, country, description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)', insert)
        conn.commit()

    for event in blowout_data:
        insert = add_data(event, blowout_months)
        cur.execute('INSERT INTO Blowout (name, date_time, state, country, description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)', insert)
        conn.commit()

    for event in festivity_data:
        insert = add_data(event, festivity_months)
        cur.execute('INSERT INTO Festivity (name, date_time, state, country, description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)', insert)
        conn.commit()

    for event in shindig_data:
        insert = add_data(event, shindig_months)
        cur.execute('INSERT INTO Shindig (name, date_time, state, country, description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)', insert)
        conn.commit()

add_data_to_tables()

# This part sorts the month dictionaries in descending order, to see what month
# these events occur most frequently
sorted_party_months = sorted(party_months.items(), key = lambda x: x[1], reverse = True)
sorted_celebration_months = sorted(celebration_months.items(), key = lambda x: x[1], reverse = True)
sorted_blowout_months = sorted(blowout_months.items(), key = lambda x: x[1], reverse = True)
sorted_festivity_months = sorted(festivity_months.items(), key = lambda x: x[1], reverse = True)
sorted_shindig_months = sorted(shindig_months.items(), key = lambda x: x[1], reverse = True)

def create_total():
    total = {}

    for key in party_months:
        if key in total:
            total[key] += party_months[key]
        else:
            total[key] = party_months[key]

    for key in celebration_months:
        if key in total:
            total[key] += celebration_months[key]
        else:
            total[key] = celebration_months[key]

    for key in blowout_months:
        if key in total:
            total[key] += blowout_months[key]
        else:
            total[key] = blowout_months[key]

    for key in festivity_months:
        if key in total:
            total[key] += festivity_months[key]
        else:
            total[key] = festivity_months[key]

    for key in shindig_months:
        if key in total:
            total[key] += shindig_months[key]
        else:
            total[key] = shindig_months[key]

    return total

total_sorted_months = sorted(create_total().items(), key = lambda x: x[1], reverse = True)

print (sorted_party_months)
print (sorted_celebration_months)
print (sorted_blowout_months)
print (sorted_festivity_months)
print (sorted_shindig_months)
print (total_sorted_months)
print (latitudes)
print (longitudes)
print (len(latitudes))
print (len(longitudes))
