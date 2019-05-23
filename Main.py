import json
import turtle
import urllib.request
import time
import reverse_geocoder as rg
import pprint
from geopy.geocoders import Nominatim

class ISSFinder:

    def setUpISS(self):
        url = 'http://api.open-notify.org/iss-now.json'
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
        # print(result)

        location = result['iss_position']
        lat = float(location['latitude'])
        lon = float(location['longitude'])
        print('The ISS is currently located at latitude', lat, 'longitude', lon)

        geolocator = Nominatim(user_agent = "test")
        location = geolocator.reverse(lat,lon)
        print('This should be somewhere near', location.address)
        # print(location.address)
        location = geolocator.geocode(location.address)
        print('Whose actual coordinates are ', location.latitude, location.longitude)
        # print((location.latitude, location.longitude))


        screen = turtle.Screen()
        screen.setup(720, 360)
        screen.setworldcoordinates(-180, -90, 180, 90)
        screen.bgpic('map.gif')

        screen.register_shape('iss.gif')
        iss = turtle.Turtle()
        iss.shape('iss.gif')
        iss.setheading(90)

        iss.penup()
        iss.goto(lon, lat)

        # Houston Space Center
        # lat = 29.5518
        # lon = -95.0983
        #
        # location = turtle.Turtle();
        # location.penup()
        # location.color('yellow')
        # location.goto(lon, lat)
        # location.dot(5)
        # location.hideturtle()


    def findWhenISS(self):
        print('Find out when the ISS will be over somewhere. Type esc anywhere to exit')

        check = 0
        buff = True
        while buff:
            print('Enter 1 to search by address, 2 to search by geocoordinates')
            try:
                check = input()
                check = int(check)
            except ValueError:
                if check == 'esc':
                    buff = False
                    return
                continue
            if check == 1:
                print('Enter an address:')
                address = input()
                if address == 'esc':
                    buff = False
                    return

                geolocator = Nominatim(user_agent="test")
                location = geolocator.geocode(address)
                lat = location.latitude
                lon = location.longitude
                print('I got ' + location.address + ' from your input')

            elif check == 2:
                print('Latitude:')
                lat = input()
                try:
                    lat = float(lat)
                except ValueError:
                    if lat == 'esc':
                        buff = False
                        return
                    print("Enter a real number")
                    continue
                print('Longitude:')
                lon = input()
                try:
                    lon = float(lon)
                except ValueError:
                    if lon == 'esc':
                        buff = False
                        return
                    print("Enter a real number")
                    continue

            else:
                 continue

            location = turtle.Turtle();
            location.penup()
            location.color('yellow')
            location.goto(lon, lat)
            location.dot(5)
            location.hideturtle()

            url = 'http://api.open-notify.org/iss-pass.json'
            url = url + '?lat=' + str(lat) + '&lon=' + str(lon)
            response = urllib.request.urlopen(url)
            result = json.loads(response.read())
            # print(result)

            over = result['response'][1]['risetime']
            style = ('Times New Roman', 6, 'bold')
            location.write(time.ctime(over), font=style)
            print('It will fly over on ' + time.ctime(over))

            # Tried to add functionality to report what area that lat, long was but it refused to play nice
            # coord = (lat, lon)
            # result = rg.search(coord)





class Main:


    url = 'http://api.open-notify.org/astros.json'
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    # print(result)

    people = result['people']

    print('Number of people in space:', result['number'], '\n')

    for p in people:
        print(p['name'], 'in the', p['craft'])

    print()

    buff = ISSFinder()
    buff.setUpISS()
    buff.findWhenISS()