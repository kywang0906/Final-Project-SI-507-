import pandas as pd
from math import asin, cos, sin, atan2, sqrt,radians, degrees


def main():
    # User Input
    country = collectCountry()
    city = collectCity(country)
    popularity = collectReviewNum()
    attractions_location = collectGeo()

    # Data
    data = organizedData()

    # Filter data by country, city and popularity
    filtered = data.loc[(data['Country']==country) & (data['City']==city) & (data['Popularity']>popularity)].reset_index()

    # Find the distances between all the hotels and the centroid of the user-input attractions
    target = center_geolocation(attractions_location)
    lat = [d for d in filtered['Latitude']]
    lon = [d for d in filtered['Longitude']]
    dis_to_target = []
    for i in range(len(lat)):
        dis_to_target.append(distance(target[0], target[1], lat[i], lon[i]))

    # Concatenate the Distance column into the filtered data
    distances = pd.DataFrame(dis_to_target, columns=['Distance']).reset_index()
    output = pd.concat([filtered,distances],axis=1).drop(columns='index')

    # Find the closest number
    closest = min(output['Distance'])

    # Print the closest hotel to the user-input attractions
    print('\n*****Hotel Recommendation*****')
    best_match = output.loc[output['Distance']==closest]['Hotel'].to_string().split('    ')[1]
    print(best_match)


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
    # radius of earth
    r = 6371
    # calculate the result
    return(c * r)


def organizedData():
    """
    Merge all the data.
    """
    df1 = pd.read_csv('Detroit_geo.csv').drop(columns='Index')
    df2 = pd.read_csv('Chicago_geo.csv').drop(columns='Index')
    df3 = pd.read_csv('Montreal_geo.csv').drop(columns='Index')
    df4 = pd.read_csv('Toronto_geo.csv').drop(columns='Index')
    return pd.concat([df1,df2,df3,df4]).reset_index().drop(columns='index').dropna()


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
            city = input('Which city do you plan to visit, Detroit or Chicago?\n(Any words other than "Detroit" or "Chicago" are ineffective.)\n')
            if city != "Detroit" and city != "Chicago":
                print('Ineffective Input')
            else:
                break
        elif country == "CA":
            city = input('Which city do you plan to visit, Montreal or Toronto?\n(Any words other than "Montreal" or "Toronto" are ineffective.)\n')
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
        review = input('How popular should the hotels you stay be?\n(Please enter a review number of the hotels you prefer to stay. The number range: 1~1500)\n')
        if (review.isdigit() == False) or int(review) < 1 or int(review) > 1500:
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
        print(f"---Pair {i+1}---")
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