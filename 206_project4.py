import urllib
import facebook
import json
import sqlite3
import sys
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

# This is the link I used to know what API functions to use: http://facebook-sdk.readthedocs.io/en/latest/api.html

# This sets up my credentials to be able to use plotly
plotly.tools.set_credentials_file(username = 'maheenak', api_key ='rWSKmckdQDGohXjqnGSB')
# I create a scatterplot of a map which I used MapBox for through plotly; I needed an access token for this
mapbox_access_token = 'pk.eyJ1IjoibWFoZWVuYWtiYXIiLCJhIjoiY2piN2hpMndvNDBkZzJxbzl0Nzh3enFtYiJ9.MvI-Gs0gmg5f72zYvdKUEA'

token = 'EAAOJEiXVpEMBAJJsR44JOWyJH6LRJZAiYqnZA7TqZAXKBZBHQZAvVqb8xYEFBS5QpWc9tzeY0oeseZBSxJYH5DSsD8II2pfZCdMUM0YXUbUp0m46DbyYZCA08Siibvf9TRpYGpUsaZBl8SyfaV6hQMq9Qdvpui6F8CBcZD'

graph = facebook.GraphAPI(access_token = token, version = 2.11)

CACHE_FNAME = "206_project4_fb_cache.json"

# The caching stuff
try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

# I use this dictionary later so my printed data and visualizations have the actual month instead of the number
month_dict = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September',
              '10': 'October', '11': 'November', '12': 'December'}
# Similar concept as the month_dict, but for times
time_dict = {'00': '12 am', '01': '1 am', '02': '2 am', '03': '3 am', '04': '4 am', '05': '5 am', '06': '6 am', '07': '7 am', '08': '8 am',
             '09': '9 am', '10': '10 am', '11': '11 am', '12': '12 pm', '13': '1 pm', '14': '2 pm', '15': '3 pm', '16': '4 pm', '17': '5 pm',
             '18': '6 pm', '19': '7 pm', '20': '8 pm', '21': '9 pm', '22': '10 pm', '23': '11 pm'}
latitudes = []
longitudes = []
times = {}

# Input: a word that is contained in Facebook events.
# Returns: a dictionary that contains different information for each event that
# contains that keyword in it.
# This checks if that word is already in my cache. If it is, it just uses that.
# Otherwise, it uses the Facebook API to get and cache that data.
def get_events(key_word):
    word = 'events: ' + key_word
    if word in CACHE_DICTION:
        results = CACHE_DICTION[word]
    else:
        # gets last 100 instances of FB events with the given keyword
        results = graph.search(q = key_word, type = 'event', limit = 100)
        CACHE_DICTION[word] = results
        f = open(CACHE_FNAME, "w")
        # updates the json file with whatever is in CACHE_DICTION
        f.write(json.dumps(CACHE_DICTION))
        f.close

    return results['data']

# These lines call the 'get_events()' function with different keywords
party_data = get_events('party')
celebration_data = get_events('celebartion')
blowout_data = get_events('blowout')
festivity_data = get_events('festivity')
shindig_data = get_events('shindig')

# Creating empty dictionaries to be used later
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

# This part of the code creates the tables for each word related to 'party'
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

# Input: 'event_item' is a dictionary that contains information about an
# event from Facebook (the name, start time, location, etc). 'dict_input' is
# also a dictionary, one that is used to keep track of what month of the year
# each event is scheduled for.
# Returns: One row that is to be inputted into the table for that particular
# event. (I create a for loop later that inserts all the rows).
def add_data(event_item, dict_input):
    insert_list = [event_item['name'], event_item['start_time']]

    # splits the date time information given in the event dictionary to get the
    # data I want (the start hour and the month)
    date = event_item['start_time'].split('-')
    time = event_item['start_time'].split('T')
    time_more = time[1].split(':')
    hour = time_more[0]

    if date[1][0] == '0':
        month = date[1][1]
    else:
        month = date[1]

    if time_dict[hour] in times:
        times[time_dict[hour]] += 1
    else:
        times[time_dict[hour]] = 1

    # This part is modifying the dict_input dictionary
    if month in dict_input:
        dict_input[month] += 1
    else:
        dict_input[month] = 1

    # Have to check if certain information was included for each event. Many of
    # them did not have a location specified. If this was the case, I made that
    # field 'N/A' in the database.
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

    # Sets up the row that's going to be inserted into the table.
    insert_list.append(state)
    insert_list.append(country)
    insert_list.append(description)
    insert_list.append(latitude_point)
    insert_list.append(longitude_point)

    return insert_list

# Input: Nothing. I use the data I collected previously.
# This function adds the data I cached earlier to the table corresponding to
# each 'party' synonym. It utilizes the function 'add_data(),' which I created
# to avoid having redundant code, because I didn't want to type out the same
# thing over and over again for each table.
# Returns: Nothing. This just modifies the tables that I created earlier.
def add_data_to_tables():
    # loops through each event in party_data and uses the add_data function to
    # create the row that's going to be inserted.
    for event in party_data:
        # This calls the add_data() function for each item in party_data.
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
cur.close()

# This part sorts the month dictionaries in descending order, to see what month
# these events occur most frequently
sorted_party_months = sorted(party_months.items(), key = lambda x: x[1], reverse = True)
sorted_celebration_months = sorted(celebration_months.items(), key = lambda x: x[1], reverse = True)
sorted_blowout_months = sorted(blowout_months.items(), key = lambda x: x[1], reverse = True)
sorted_festivity_months = sorted(festivity_months.items(), key = lambda x: x[1], reverse = True)
sorted_shindig_months = sorted(shindig_months.items(), key = lambda x: x[1], reverse = True)

# Input: Nothing.
# This function creates a dictionary that adds up the numbers of the
# dictionaries I created previously, to total up what month events occur in.
# For example, if the 'party' dictionary had 12 events for January, the
# 'celebration' one had 1, the 'blowout' one had 10, the 'festivity' one had
# 0, and the 'shindig' one had 5, the value for total['January'] would be 28.
# Returns: The 'total' dictionary
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

total_months = create_total()
# Sorts the total_months dictionary so we can see what month the events occur
# most frequently in total
sorted_total_months = sorted(total_months.items(), key = lambda x: x[1], reverse = True)
times_tup = sorted(times.items(), key = lambda x: x[1], reverse = True)

# Input: Nothing.
# This function creates a bar graph with the x-axis as months and the y-axis
# as the number of times an event occurred in that month from the FB data.
# Returns: Nothing.
def create_bar_graph():

    x_axis = []
    y_axis = []
    index = 1
    while index < 13:
        to_append = str(index)
        x_axis.append(month_dict[to_append])
        y_axis.append(total_months[to_append])
        index += 1

    # this is the data that will go into the bar graph
    graph = go.Bar(
        x = x_axis,
        y = y_axis,
        marker = dict (
            color = 'rgb(178, 102, 255)'
        )
    )

    # this sets up the name of the graph and its axes
    layout = go.Layout(
        title = 'Event Occurrences with \'Party\' Like Term in Title',
        xaxis = dict(
            title = 'Number of Occurrences'
            ),
        yaxis = dict(
            title = 'Month'
        )
    )
    data = [graph]
    fig = go.Figure(data = data, layout = layout)
    py.plot(fig, filename = 'total_occurrences_graph')

# Input: Nothing.
# This function creates a map with plots of the locations that were provided
# for each of the events, using their coordinates. I created two lists in the
# beginning of my program, called 'latitudes' and 'longitudes' so I had the
# necessary data saved.
# Returns: Nothing.
def create_map():

    data = [
        go.Scattermapbox(
            lat = latitudes,
            lon = longitudes,
            mode = 'markers',
            marker = dict (
                size = 9,
                color = 'rgb(153, 0, 76)'
            )
        )
    ]

    layout = go.Layout(
        autosize = True,
        hovermode = 'closest',
        mapbox = dict(
            # the access token from the beginning of the file
            accesstoken = mapbox_access_token,
            bearing = 0,
            center = dict(
                lat = 38.92,
                lon = -77.07
            ),
            pitch = 0,
            zoom = 10
        ),
    )

    fig = dict(data = data, layout=layout)
    py.plot(fig, filename = 'Map of Event Locations')

create_bar_graph()
create_map()

# Input: A tuple. In this case, I created this function to print out the
# sorted tuples I created from the dictionaries of what month the events
# occurred in.
# I mainly created this function to print out my data and show it in my report.
# Returns: Nothing.
def print_sorted_tuples(tup_input):
    for tup in tup_input:
        month = str(tup[0])
        print ('{}: {}'.format(month_dict[month], tup[1]))
    print ('\n')

print ('\'Party\' event occurrences sorted: ')
print_sorted_tuples(sorted_party_months)

print ('\'Celebration\' event occurrences sorted: ')
print_sorted_tuples(sorted_celebration_months)

print ('\'Blowout\' event occurrences sorted: ')
print_sorted_tuples(sorted_blowout_months)

print ('\'Festivity\' event occurrences sorted: ')
print_sorted_tuples(sorted_festivity_months)

print ('\'Shindig\' event occurrences sorted: ')
print_sorted_tuples(sorted_shindig_months)

print ('Total event occurrences sorted: ')
print_sorted_tuples(sorted_total_months)

# Here, I'm printing a lot of the data I found just so you guys can see
# the various data I collected.
print ('I saved the hour that each event was scheduled to start and sorted it by frequency: ')
for item in times_tup:
    print ('Time: {}, Frequency: {}'.format(item[0], item[1]))
print ('\n')

print ('I saved the latitude and longitude coordinates of each event: ')
coor = 0
for coor in range(len(latitudes)):
    print ('({} , {})'.format(latitudes[coor], longitudes[coor]))
