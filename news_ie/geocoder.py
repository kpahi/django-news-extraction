from geopy import geocoders


def find_lat_lng(locations):
    g = geocoders.GoogleV3(domain='maps.google.pl')
    for l in locations:
        # location_coord is a list [location,coordintae]
        location_coord = g.geocode(l)
        # if coordintae found from 1st location done[pass] else continue loop
        if location_coord:
            pass
            print(location_coord[1])
    return location_coord[1]
