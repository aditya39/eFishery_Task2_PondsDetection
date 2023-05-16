import pygeohash as pgh

# Define the latitude and longitude you want to encode
lat = 37.7749
lng = -122.4194



gh =pgh.encode(lat,lng)

print(gh)

