# Import libraries
import googlemaps
from datetime import datetime
# Set coords
coords_0 = '43.70721,-79.3955999'
coords_1 = '43.7077599,-79.39294'
# Init client
gmaps = googlemaps.Client(key='AIzaSyAieOd9Qyw7J0giJbiwdBPCYsEiS4GYqb0')
# Request directions
now = datetime.now()
directions_result = gmaps.directions(
    coords_0, coords_1, mode="transit", departure_time=now, units="metric")

# Get distance
distance = 0
legs = directions_result[0].get("legs")
for leg in legs:
    distance = distance + leg.get("distance").get("value")
print(distance)
