import json
from math import asin, cos, sin, atan2, sqrt,radians, degrees
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def main():
    # User Input
    country = collectCountry()
    city = collectCity(country)
    popularity = collectReviewNum()
    attractions_location = collectGeo()

    # Data
    with open('all_data.json', 'r') as f:
        data = json.loads(f.read())

    # Filter data by country, city and popularity
    filtered = []
    for hotel in data[country][city]:
        if hotel[2] >= popularity:
            filtered.append(hotel)

    # Find the distances between all the hotels and the centroid of the user-input attractions
    target = center_geolocation(attractions_location)
    lat = [d[3] for d in filtered]
    lon = [d[4] for d in filtered]
    dis_to_target = []
    for i in range(len(lat)):
        dis_to_target.append(distance(target[0], target[1], lat[i], lon[i]))

    # Append the values of distance into the filtered data
    for i in range(len(filtered)):
        filtered[i].append(dis_to_target[i])

    # Find the closest hotel to the centroid of the three attractions
    closest = min(dis_to_target)
    for info in filtered:
        if info[-1] == closest:
            best = info

    # Show the outcome
    print('\n*****Hotel Recommendation*****')
    print('\n[Hotel Name]: '+best[0])
    print('\n[Number of reviews]: '+str(best[2]))
    print('\n[Distance to the centroid of your designeated attractions]: '+str(best[-1])+' km')
    print('\n[Address]: '+best[1])
    show_browser = input('\nWould you like to search this hotel on Google Maps? \n(Enter "y" to see it or enter anything else to break.)')
    if show_browser == 'y':
        map_url = 'https://www.google.com/maps'
        # option = webdriver.ChromeOptions()
        # option.add_experimental_option("detach", True) # Not to close the browser automatically
        # browser = webdriver.Chrome(options=option)
        browser = webdriver.Chrome()
        browser.get(map_url)
        locate_on_map = browser.find_element(By.CSS_SELECTOR, '#searchboxinput')
        locate_on_map.send_keys(best[1])
        time.sleep(5)
        locate_on_map.send_keys(Keys.ENTER)
    time.sleep(20)
    browser.close()
    print('\nEnjoy your trip!')
    

def center_geolocation(geolocations):
    """
    Find the centroid of the input geolocations.
    -
    Reference: https://www.twblogs.net/a/5b8de0302b717718834139fa (A webpage written in Chinese)
    """
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
       
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


def distance(lat1, lon1, lat2, lon2):
    """
    Find the distance between two pairs of input latitudes and longitudes.
    -
    Reference: https://www.geeksforgeeks.org/program-distance-two-points-earth/
    """
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    # radius of earth (kilometor)
    r = 6371
    # calculate the result
    return(c * r)


def collectCountry():
    """
    Filter data for the assigned country.
    """
    while True:
        country = input('Which country do you plan to visit, the US or CA?\n(Any words other than "US" or "CA" are ineffective.)\n')
        if country != 'US' and country != 'CA':
            print('Ineffective Input')
        else:
            break
    return country


def collectCity(country):
    """
    Filter data for the assigned city.
    """
    while True:
        if country == 'US':
            city = input('\nWhich city do you plan to visit, Detroit or Chicago?\n(Any words other than "Detroit" or "Chicago" are ineffective.)\n')
            if city != "Detroit" and city != "Chicago":
                print('Ineffective Input')
            else:
                break
        elif country == "CA":
            city = input('\nWhich city do you plan to visit, Montreal or Toronto?\n(Any words other than "Montreal" or "Toronto" are ineffective.)\n')
            if city != "Montreal" and city != "Toronto":
                print('Ineffective Input')
            else:
                break
        else:
            print('Ineffective Input')
    return city


def collectReviewNum():
    """
    Filter data for the assigned number of reviews.
    """
    while True:
        review = input('\nHow popular should the hotels you stay be?\n(Please enter a review number of the hotels you prefer to stay. The number range: 1~2000)\n')
        if (review.isdigit() == False) or int(review) < 1 or int(review) > 2000:
            print('Ineffective Input')
        else:
            break
    return int(review)


def isfloat(num):
    """
    Check whether the input data is a float.
    """
    try:
        float(num)
        return True
    except ValueError:
        return False


def collectGeo():
    """
    Get input latitudes and longitudes.
    """
    threePairs = []   
    for i in range(3):
        latAndLong = []
        print(f"\n---Pair {i+1}---")
        while True:
            att1 = input("Latitude: ")
            if isfloat(att1) == False:
                print('Ineffective Input')
            else:
                break
        latAndLong.append(float(att1))
        while True:
            att2 = input("Longitude: ")
            if isfloat(att2) == False:
                print('Ineffective Input')
            else:
                break
        latAndLong.append(float(att2))
        threePairs.append(latAndLong)
    return threePairs


if __name__ == '__main__':
    main()
