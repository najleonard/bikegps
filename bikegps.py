__author__ = 'nleonard1'
#22rasp pi adding random comment
import stravalib, urllib2, json, requests as r
import geopy, geopy.distance
import googlemaps
import os
from gps import *
from time import *
import time
import threading
import RPi.GPIO as GPIO
import math, numpy as np

STORED_ACCESS_TOKEN = "59415871d89656eaf18fb8bee6a999c0a332489e"

from stravalib import Client
from stravalib import unithelper

gpsd = None #seting the global variable

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)

os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


#client = Client()
client = Client(access_token=STORED_ACCESS_TOKEN)
gmaps = googlemaps.Client(key='AIzaSyAWAcpS14bsm6zgzOG2hnMBwRILtdwYEFY')

athlete = client.get_athlete(77138)
print("Hello, {}".format(athlete.firstname))

print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))

url = "https://www.strava.com/api/v3/segments/starred"
header = {'Authorization': 'Bearer 59415871d89656eaf18fb8bee6a999c0a332489e'}
response = r.get(url, headers=header).json()

#print(response)



for i in range(0,1): #len(response)):
	print(response[i]['name'])
	start_latitude = response[i]['start_latitude']
	start_longitude = response[i]['start_longitude']
	testPoint = geopy.Point(start_latitude,start_longitude)


#homePoint = geopy.Point(37.743958333,-122.432046667)

#dist = geopy.distance.distance(testPoint,homePoint).km

#route = gmaps.distance_matrix(origins=(homePoint.latitude,homePoint.longitude), destinations=(testPoint.latitude,testPoint.longitude),mode="bicycling",language="English",units="metric")

#distance = route["rows"][0]["elements"][0]["distance"]["value"]
#duration = route["rows"][0]["elements"][0]["duration"]["value"]

#directions = gmaps.directions((homePoint.latitude,homePoint.longitude),(testPoint.latitude,testPoint.longitude),mode="bicycling")

#print(directions)
#for i in directions[0]["legs"][0]["steps"]:
#	print i["html_instructions"]

#print ("Distance is %8.2fkm" % (distance/1000))
#print ("Duraction is %8.2f minutes" % (duration/60))

#print(dist)

SEGMENT = 229781
mysegment = client.get_segment(SEGMENT) #client.get_segment(,6795950158)

url = "https://www.strava.com/api/v3/segments/starred"
#response = urllib.urlopen(url)
#print(response)

print("My segment is {}".format(mysegment.name))


types = ['time', 'latlng', 'altitude', 'heartrate', 'temp', ]
streams = client.get_segment_streams(SEGMENT, types=types, resolution='high')
#streams = client.get_activity_streams(ACTIVITY, types=types, resolution='high')

#  Result is a dictionary object.  The dict's key are the stream type.
#if 'latlng' in streams.keys():
#    print(streams['latlng'].data)

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
      GPIO.output(25,GPIO.HIGH)
      os.system('clear')
  	 
      print
      print ' GPS reading'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print
      #print 'sats        ' , gpsd.satellites
      route = gmaps.distance_matrix(origins=(gpsd.fix.latitude,gpsd.fix.longitude), destinations=(testPoint.latitude,testPoint.longitude),mode="bicycling",language="English",units="metric")
      print route
      if np.invert(math.isnan(gpsd.fix.altitude)):
        distance = route["rows"][0]["elements"][0]["distance"]["value"]
        duration = route["rows"][0]["elements"][0]["duration"]["value"]
        print ("Distance is %8.2fkm" % (distance/1000))
        print ("Duraction is %8.2f minutes" % (duration/60))
        print ("Next direction:")
        directions = gmaps.directions((gpsd.fix.latitude,gpsd.fix.longitude),(testPoint.latitude,testPoint.longitude),mode="bicycling")
        print directions[0]["legs"][0]["steps"][0]["html_instructions"]
      time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    GPIO.output(25,GPIO.LOW)
  
  print "Done.\nExiting."
