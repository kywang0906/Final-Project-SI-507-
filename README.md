## Final Project of SI507: Hotel Recommendation Tool ##
### Description ###
This tool asks users to input their preference of travel information and provides them with a hotel recommendation.
### How the tool works ###
1. Users are asked to choose between the US and Canada for the next trip.
2. Users are asked to input a city they plan to visit (either Detroit or Chicago for visiting the US and either Montreal or Toronto for visiting Canada).
3. Users are asked to enter a review number which represents the popularity of the hotel they hope to stay for their trip.
4. Users are asked to enter three pairs of latitudes and longitudes of the attractions they are going to visit.
5. Based on the given information, the tool provides the users with a hotel recommendation that is the closest to all the attractions they plan to visit.
### Data Sources ###
1.	[TripAdvisor Official Website](https://www.tripadvisor.com/): see the directory "data_from_tripadvisor" in which the files collected by *tripadvisor_data.py*
2.  [TomTom API](https://developer.tomtom.com/geocoding-api/documentation/product-information/introduction): see the directory "data_from_tomtom" in which the files collected by *lat_and_lon.py*
### How to get the API Key ###
1. Register an account at the [TomTom Developer website](https://developer.tomtom.com/).
2. Log in to the TomTom Developer Portal.
3. Find your API key in the KEYS tab of the Dashboard.
### Data Structure ###
A tree that contains Country, City, and other hotel information (including Hotel, Address, Popularity, Latitude, and Longitude). See *csv_to_json.py*
### Interactive Technology ###
Command line prompts
### Required Packages ###
None
### Main Project ###
See *interactive.py*
