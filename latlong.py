# Import pandas
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv(
    'latlong.csv',
    skipinitialspace=True,
    header=0,
    sep=',',
)

loc = Nominatim(user_agent="GetLoc")
gc = RateLimiter(loc.geocode, min_delay_seconds=2, max_retries=5)

for index, row in df.iterrows():
    if row is not None:
        curloc = gc(row['Property_Address'])
        if curloc is not None:
            df['Latitude'][index] = curloc.latitude
            df['Longitude'][index] = curloc.longitude
            print(str(index))
            df.to_csv('latlong.csv')
