# Project_4

This was the final project for a class and we had to utilize APIs and visualization software in any way that we wanted. I used the Facebook API to analyze Facebook events with certain keywords in it. 
I thought it would be interesting to see where the events are created, what time they are for, where they were held, etc. I used the word “party” and many synonyms, and created a function that would 
find the last 100 Facebook events with that keyword in it. I was able to cache events with the following keywords: party, celebration, blowout, festivity, and shindig. I use Plotly for my visualizations, 
because it allowed me to create a variety of graphs (bar graph and map scatter plot). I also saved the data I got from the event keywords into a database. I had one table for each party synonym. Each 
table included the event name, the start time and date, the state, country, description, and location coordinates. Some of the events did not list certain information, and for those I wrote “N/A” into the table.
