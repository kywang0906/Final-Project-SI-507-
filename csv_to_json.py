import json
import pandas as pd


def csv_data():
    """
    Merge all the data from csv files.
    """
    df1 = pd.read_csv('Detroit_geo.csv').drop(columns='Index')
    df2 = pd.read_csv('Chicago_geo.csv').drop(columns='Index')
    df3 = pd.read_csv('Montreal_geo.csv').drop(columns='Index')
    df4 = pd.read_csv('Toronto_geo.csv').drop(columns='Index')
    return pd.concat([df1,df2,df3,df4]).reset_index().drop(columns='index').dropna()

def to_json(): 
    """
    Convert all the csv files into a json file for further use.
    """
    csv = csv_data()
    json_data = {'US':{'Chicago':[], 'Detroit':[]},'CA':{'Toronto':[],'Montreal':[]}}

    def iterate_cities(country, city):
        ct = csv.loc[csv['City']==city]
        for _, row in ct.iterrows():
            hotel_info = []
            hotel_info.append(row['Hotel']) # 0
            hotel_info.append(row['Address']) # 1
            hotel_info.append(row['Popularity']) # 2
            hotel_info.append(row['Latitude']) # 3
            hotel_info.append(row['Longitude']) # 4
            json_data[country][city].append(hotel_info)
    
    iterate_cities('US','Chicago')
    iterate_cities('US','Detroit')
    iterate_cities('CA','Toronto')
    iterate_cities('CA','Montreal')

    with open("all_data.json", "w") as outfile:
        json.dump(json_data, outfile, indent=3)

if __name__ == '__main__':
    to_json()
    print('---finish--')