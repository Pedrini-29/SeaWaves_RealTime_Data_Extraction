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

from extraction_functions import scraping_method

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
recent_df

# %%
#function to change the marker colour with different wave hights
def marker_color(wave):
    wave=float(wave)
    if wave > 6:
        return "black"
    elif wave > 4:
        return "red"
    elif wave > 2:
        return "orange"
    elif wave > 1:
        return "green"
    elif wave > 0.5:
        return "blue"
    else:
        return "gray"
    
def fancy_html(row):
    
    # Access values from the row, fallback to 'N/A'
    altura_signif = row.get('Altura Signif. del Oleaje (m)', 'N/A') if isinstance(row, dict) else row.get('Altura Signif. del Oleaje (m)', 'N/A')
    altura_max = row.get('Altura Máxima del Oleaje (m)', 'N/A') if isinstance(row, dict) else row.get('Altura Máxima del Oleaje (m)', 'N/A')
    dir_media = row.get('Direcc. Media de Proced. (º)', 'N/A') if isinstance(row, dict) else row.get('Direcc. Media de Proced. (º)', 'N/A')
    dir_pico = row.get('Direcc. de pico de proced. (º)', 'N/A') if isinstance(row, dict) else row.get('Direcc. de pico de proced. (º)', 'N/A')
    periodo_medio = row.get('Periodo Medio Tm02 (s)', 'N/A') if isinstance(row, dict) else row.get('Periodo Medio Tm02 (s)', 'N/A')
    periodo_pico = row.get('Periodo de Pico (s)', 'N/A') if isinstance(row, dict) else row.get('Periodo de Pico (s)', 'N/A')
    fecha = row.get('Fecha  (GMT)', 'N/A') if isinstance(row, dict) else row.get('Fecha  (GMT)', 'N/A')
    energia = row.get('Energía del Oleaje (kJ)', 'N/A') if isinstance(row, dict) else row.get('Energía del Oleaje (kJ)', 'N/A')
    temp_mar = row.get('Temperatura del mar (°C)', 'N/A') if isinstance(row, dict) else row.get('Temperatura del mar (°C)', 'N/A')
    
    #print(altura_signif,altura_max,dir_media,dir_pico,periodo_medio,periodo_pico,fecha,energia,temp_mar)

    station = row['StationCode']
    lat = row['Latitude']
    lon = row['Longitude']

    left_col_colour = "#208AB7"
    right_col_colour = "#C5DCE7"

    html = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station}</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura máxima (Hmax)</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{altura_max} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. media</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{dir_media}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. pico</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{dir_pico}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo medio (Tm02)</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{periodo_medio} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo de pico</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{periodo_pico} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Energía del oleaje</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{energia} kJ</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Temperatura mar</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{temp_mar} °C</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitude</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitude</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""

    return html


# %%
#Create the map
m_3 = folium.Map(location=[43.26,-2.93], zoom_start=4.5)

for idx, row in recent_df.iterrows():

    sign_wave=row['Altura Signif. del Oleaje (m)']
    
    html = fancy_html(row)  # Pass recent_df to the function
    iframe = branca.element.IFrame(html=html, width=400, height=300)
    popup = folium.Popup(iframe, parse_html=True)

    folium.Marker([row['Latitude'], row['Longitude']], popup=popup, icon=folium.Icon(color=marker_color(sign_wave),icon_color="white",icon="water",angle=0,prefix='fa')).add_to(m_3)
                
m_3.save("buoys.html")

webbrowser.open("buoys.html")


