# %%
#Import useful packages and data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import pandas as pd
import requests
import json
import datetime

#useful packages for making map data
import branca

import folium 
from folium import Marker
from folium.plugins import MarkerCluster

#import neessary custom modules for data extractionand map design
from extraction_functions import scraping_method
from map_design_functions import fancy_html,marker_color

#run map on web browser
import webbrowser



# %%
df=pd.read_csv("dataset.csv",encoding="latin-1")

# %%
df.head()

# %%
#defining web scraping function

# %%
#extracting URLs from the dataframe
URLs=df[["StationCode","Conjunto de datos","URL"]]
URLs

# %%
import asyncio

def scraping_sync(row, idx, total):
    temp_table = scraping_method(
        row["URL"],
        row["StationCode"],
        str(row["Conjunto de datos"])
    )
    print(f"{idx + 1}/{total}")
    temp_table["StationCode"] = row["StationCode"]
    return temp_table

# %%
async def scrape_all(URLs, max_concurrent=5):
    loop = asyncio.get_running_loop()
    sem = asyncio.Semaphore(max_concurrent)

    async def run_one(row, idx):
        async with sem:
            return await loop.run_in_executor(
                None,
                scraping_sync,
                row,
                idx,
                len(URLs)
            )

    tasks = [
        run_one(row, idx)
        for idx, row in URLs.iterrows()
    ]

    return await asyncio.gather(*tasks)

# %%
#code extraction with asyncio
async def main():
    tables = await scrape_all(URLs, max_concurrent=5)
    return tables

#run the data extraction
tables = asyncio.run(main())

# %%
#code extraction without asyncio
'''tables=[]

for idx,row in URLs.iterrows():
    temp_table=scraping_method(row["URL"],row["StationCode"],str(row["Conjunto de datos"]))
    print(f"{idx+1}/{len(URLs)}")
    temp_table['StationCode']=row['StationCode']
    tables.append(temp_table)'''


# %%
#select only most recent data
recent = []

for table in tables:
    try:
        recent.append(table.loc[0])
    except KeyError:
        continue


# %%
recent

# %%
#NON SERVE

#insert two columns with longitude and latitude value in recent
for i in range(0,len(recent)):
    recent[i]['Latitude']=df.loc[df["StationCode"] == recent[i]["StationCode"], "Latitude"].iloc[0]
    recent[i]['Longitude']=df.loc[df["StationCode"] == recent[i]["StationCode"], "Longitude"].iloc[0]

# %%
#make a pandas dataframe with the most recent informations for each station
temp_list=[recent[0]]
for i in range(1,len(recent)):
    temp_list[0]=pd.concat([temp_list[0],recent[i]],axis=1)

recent_df=temp_list[0].T.reset_index()


# %%
#Create the map
m_3 = folium.Map(location=[43.26,-2.93], zoom_start=4.5)

#this makes the popups transparent
css = """
<style>
.leaflet-popup-content-wrapper {
    background: transparent;
    box-shadow: none;
}

.leaflet-popup-tip {
    background: transparent;
    box-shadow: none !important;
}
.leaflet-popup-close-button {
    display: none !important;
}

</style>
"""
m_3.get_root().html.add_child(folium.Element(css))

#make the popup close on a mouse click
js = """
<script>
map.on('click', function () {
    map.closePopup();
});
</script>
"""

m_3.get_root().html.add_child(folium.Element(js))

#data extraction
for idx, row in recent_df.iterrows():

    sign_wave=row['Altura Signif. del Oleaje (m)']
    
    html = fancy_html(row)  # Pass recent_df to the function
    iframe = branca.element.IFrame(html=html, width=400, height=300)
    popup = folium.Popup(iframe, parse_html=True)

    folium.Marker([row['Latitude'], row['Longitude']], popup=popup, icon=folium.Icon(color=marker_color(sign_wave),icon_color="white",icon="water",angle=0,prefix='fa')).add_to(m_3)
                
m_3.save("buoys.html")

webbrowser.open("buoys.html")


