# Import pandas
import pandas as pd
# importing geopy library
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

#colnames = ['Property_Address']
#load specifc columns only by name
df = pd.read_csv(
    'latlong.csv',
    skipinitialspace=True,
    header = 0,
    sep = ',',
    #usecols = colnames
)

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")
#applying the rate limiter wrapper
gc = RateLimiter(loc.geocode, min_delay_seconds=2, max_retries=5)

#df['Latitude'] = ""
#df['Longitude'] = ""

for index, row in df.iterrows():
    if index > 16012:
    #print("Idx: " + str(index) + "Row: " + row)
        if row is not None:
            curloc = gc(row['Property_Address'])
            if curloc is not None:
                df['Latitude'][index] = curloc.latitude
                df['Longitude'][index] = curloc.longitude
                #print("Lat: ", curloc.latitude, "Long: ", curloc.longitude)
                #dfloc = dfloc.append({'Latitude': curloc.latitude,
                #                        'Longitude': curloc.longitude,
                #                        }, ignore_index=True)
                print(str(index))
                df.to_csv('latlong.csv')
                
