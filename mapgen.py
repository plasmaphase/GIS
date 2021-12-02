# Import pandas
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium import CircleMarker
from statistics import mean

colnames = ['Latitude', 'Longitude', 'Sale_Price']
#load specifc columns only by name
df = pd.read_csv(
    'latlong.csv',
    skipinitialspace=True,
    header = 0,
    sep = ',',
    dtype={'Sale_Price': str},
    usecols = colnames
)

map = folium.Map(location=[44.86023251970677, -93.73302265124681], zoom_start=12)

df = df[['Latitude', 'Longitude', 'Sale_Price']]
df['Sale_Price'] = df['Sale_Price'].replace( '[\$,)]','', regex=True ).replace( '[(]','-',   regex=True ).astype(float)

df = df.dropna()
#df['Sale_Price'] = (df['Sale_Price'] - df['Sale_Price'].min()) / (df['Sale_Price'].max() - df['Sale_Price'].min())    
#print(df['Sale_Price'].max())
#print(df['Sale_Price'].min())
#print(mean(df['Sale_Price']))

df.rename(columns=df.iloc[0]).drop(df.index[0])
#print(df)

# Adding each home as a marker to the map
for index, row in df.iterrows():
    popup_text = "Price: {}<br> Latitude: {}<br> Longitude: {}"
    popup_text = popup_text.format(row['Sale_Price'],
                                    row['Latitude'],
                                    row['Longitude'])

    # Changing the color based on buckets of cost
    price = row['Sale_Price']
    if price < 100000:
        color = "#00FFFF"
    elif price >= 100000 and price < 300000:
        color = "#85CB33"
    elif price >= 300000 and price < 1000000:
        color = "#F9B700"
    elif price >= 1000000 and price < 5000000:
        color = "#FF33FF"
    else:
        color = "#FF0000"

    #print(price/1000000)
    CircleMarker([row['Latitude'], row['Longitude']], radius=(price/1000000), fill=True, color=color, popup=popup_text).add_to(map)

#HeatMap(df, name="House Prices", radius=5, blur=2, max_zoom=45).add_to(map)

df.to_csv("data.csv")
map.save('map.html')