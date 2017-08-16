# uFSWD-P5
Udacity Full Stack Web Development - Project 5

This project requires the student to create a client-side web application using Google Maps API and one other third party API.

For this exercise, I have decided to display the nearby parks in locality within 5kms radius. I use Google APIs to search for nearby
location, and then use this location to populate a list and generate markers on the Google Maps.

When a particular park is chosen either by clicking on the marker or sidebar list, an information window is created with basic information about
park retrieved from Google Places API and FourSquare API.

For the mobile responsive sidebar, I followed the tutorial based on https://www.bootstrapzero.com/bootstrap-template/off-canvas-sidebar

I have also used Knockout Framework to monitor the list to update the DoM in realtime.

You can open index.html to look at the output.