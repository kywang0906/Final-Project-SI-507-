import pandas as pd
import numpy as np
import requests

CITY = "Detroit_1"
DATA = pd.read_csv(f"{CITY}.csv")
APIKEY = ''

def main():
    cache('Detroit_geo')
    print('---finish---')

def get_addresses():
    """
    Loop over the input csv file and store the data of column "Address" into a Python list.
  
    Parameters:
    no parameters
  
    Returns:
    addresses (list(str)): all the addresses in the read-in csv file 
    """
    addresses = []
    for d in DATA['Address']:
        addresses.append(d)
    return addresses

def get_lat_and_lon():
    """
    Call the API of TomTom (tomtom.com) to search the latitudes and longitudes of all the addresses in the input CSV file.
  
    Parameters:
    no parameters
  
    Returns:
    latitudes,longitudes (tuple(list)): all the latitudes and longitudes of the input addresses
    """
    addresses = get_addresses()
    latitudes = []
    longitudes = []

    for add in addresses:
        url = f'https://api.tomtom.com/search/2/geocode/{add}.json?key={APIKEY}'
        try:
            res = requests.get(url).json()
            if 'results' not in res or len(res['results']) == 0:
                latitudes.append(np.nan)
                longitudes.append(np.nan)
            else:
                latitudes.append(res['results'][0]['position']['lat'])
                longitudes.append(res['results'][0]['position']['lon'])  
        except ValueError:
            latitudes.append(np.nan)
            longitudes.append(np.nan)
    return (latitudes,longitudes)

def cache():
    """
    Organize the data of latitudes and longitudes into two dataframes and concatenate the dataframes with the original dataframes that are read from the csv file.
    Cache all the data into a new csv file.

    Parameters:
    no parameters
    
    Retruns:
    no return values
    """
    df1 = pd.DataFrame(get_lat_and_lon()[0], columns=['Latitude'])
    df2 = pd.DataFrame(get_lat_and_lon()[1], columns=['Longitude'])
    lat_and_lon = pd.concat([df1,df2],axis=1)
    geo_data = pd.concat([DATA,lat_and_lon],axis=1)
    geo_data.to_csv(f"{CITY}_geo.csv", index=False)


if __name__ == '__main__':
    main()