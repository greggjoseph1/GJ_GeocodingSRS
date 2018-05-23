#!/usr/bin/python

# Bring in resources
import googlemaps


def geocode(address):
    gmaps = googlemaps.Client(key='AIzaSyDA-IfaBH36LojL7Xwugxq0wcj1sLyfrf8')
    data = gmaps.geocode(address)
    result = {
      "lat": data[0]['geometry']['location']['lat'],
      "lng": data[0]['geometry']['location']['lng']
    }
    return result


loc = geocode('5000 donnelly street, stonefields, auckland')

print(loc['lat'])
print(loc['lng'])
