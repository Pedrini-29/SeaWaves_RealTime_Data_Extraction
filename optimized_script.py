# %%
#Import useful packages and data

import pandas as pd

#useful packages for making map data
import branca

import folium 
from folium import Marker
from folium.plugins import MarkerCluster

#import neessary custom modules for data extractionand map design
from extraction_functions import scraping_method
from map_design_functions import fancy_html,marker_color,c_height,c_width

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

css = """
<style>
/* Popup container */
.leaflet-popup-content-wrapper {
    background: #ffffff !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    border-radius: 6px;
}

/* Popup arrow */
.leaflet-popup-tip {
    background: #ffffff !important;
    box-shadow: none !important;
}

/* Popup content spacing */
.leaflet-popup-content {
    margin: 12px 16px 16px 16px;
}

/* Close button styling */
.leaflet-popup-close-button {
    display: block !important;
    color: red !important;
    font-size: 22px !important;
    font-weight: bold;
    top: 6px !important;
    right: 8px !important;
    width: 26px !important;
    height: 26px !important;
    line-height: 26px !important;
    text-align: center;
}

/* Optional: hover effect for better UX */
.leaflet-popup-close-button:hover {
    color: darkred !important;
    cursor: pointer;
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
    #print(df.loc[df["StationCode"]==row["StationCode"]]["Conjunto de datos"])
    conjunto=df.loc[df["StationCode"]==row["StationCode"],"Conjunto de datos"].values[0]
    html = fancy_html(row, conjunto)  # Pass recent_df to the function
    iframe = branca.element.IFrame(html=html, width=c_width(conjunto), height=int(c_height(conjunto)))
    popup = folium.Popup(iframe, parse_html=True)

    #if df.loc[df["StationCode"]==row["StationCode"],"Conjunto de datos"].isin(["REDCOS","REDEXT"]).any():
    folium.Marker([row['Latitude'], row['Longitude']], popup=popup, icon=folium.Icon(color=marker_color(sign_wave),icon_color="white",icon="water",angle=0,prefix='fa')).add_to(m_3)
                
m_3.save("buoys.html")

webbrowser.open("buoys.html")


