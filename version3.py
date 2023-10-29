import googlemaps
from gmplot import gmplot
from datetime import datetime


gmaps = googlemaps.Client(key='AIzaSyC-xvwR94vP1lZa0JDOLhXMxxMh7g8STo0')

start_location = input("Enter the starting point: ")
end_location = input("Enter the destination (leave blank if not applicable): ")
keywords = input("Enter keywords for restaurant search: ")

# Function to add restaurant markers on the map
def add_restaurant_markers(gmap, location, radius, keywords):
    places_result = gmaps.places_nearby(
        location=location,
        radius=radius,
        keyword=keywords,
        type='restaurant'
    )

    for place in places_result.get('results', []):
        place_lat = place['geometry']['location']['lat']
        place_lng = place['geometry']['location']['lng']
        gmap.marker(place_lat, place_lng)

if end_location.strip():
    directions_result = gmaps.directions(start_location, end_location, departure_time=datetime.now())

    if not directions_result:
        print("Unable to retrieve directions")
    else:
        start_lat = directions_result[0]['legs'][0]['start_location']['lat']
        start_lng = directions_result[0]['legs'][0]['start_location']['lng']
        gmap = gmplot.GoogleMapPlotter(start_lat, start_lng, 13, apikey='AIzaSyC-xvwR94vP1lZa0JDOLhXMxxMh7g8STo0')

        for step in directions_result[0]['legs'][0]['steps']:
            end_lat = step['end_location']['lat']
            end_lng = step['end_location']['lng']
            add_restaurant_markers(gmap, (end_lat, end_lng), 1000, keywords)

        gmap.draw("route_map.html")
        print("Map with route and restaurants has been created and saved as route_map.html")

else:
    geocode_result = gmaps.geocode(start_location)

    if not geocode_result:
        print("Unable to find the location")
    else:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
        gmap = gmplot.GoogleMapPlotter(lat, lng, 15, apikey='AIzaSyC-xvwR94vP1lZa0JDOLhXMxxMh7g8STo0')
        add_restaurant_markers(gmap, (lat, lng), 1000, keywords)

        gmap.draw("location_map.html")
        print("Map with restaurants near the starting point has been created and saved as location_map.html")
