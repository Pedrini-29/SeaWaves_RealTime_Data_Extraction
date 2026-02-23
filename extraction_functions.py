#Import useful packages and data
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import pandas as pd
import datetime

import requests
import json
import os

#defining web scraping function
def scraping_method(url,station,origin):
    if origin in {"REDEXT","REDCOS","ODASMAWS"}:
        return portus_table_scraping(station)
    elif origin=="METOFFICE":
        return met_office_table_scraping(url)
    elif origin == "LABOUEE":
        return labouee_table_scraping(url)

def portus_table_scraping(station):
    table_dict={}
    parameters = ["Hm0","Hmax","MeanDir","MeanDirPeak","Tm02","Tp"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    from_date= yesterday.strftime("%Y%m%d")
    to_date=str(int(from_date)+2)
    for parameter in parameters:
        URL=f"https://poem.puertos.es/portus/StationData?code={station}&params={parameter}&from={from_date}@0000&to={to_date}@0000"
        raw_data=requests.get(URL)
        if raw_data.text == "Internal Server Error":
            #print("No data availavle")
            continue
        raw_list=json.loads(raw_data.text)
        try:
            raw_recent=raw_list[-1][-1]
        except IndexError:
            #print("No data available")
            continue
        date_last, value = raw_recent[0], raw_recent[1][0]
        table_dict[f"{parameter}"]=[value]
        #print(date_last,value)
    #print(table_dict)

    table_df=pd.DataFrame(table_dict)
    try:
        table_df["Fecha  (GMT)"]=datetime.datetime.fromtimestamp(date_last)
    except UnboundLocalError:
        print("No data available from this buoy")
    table_df=table_df.rename(columns={'Hm0': 'Altura Signif. del Oleaje (m)', 'Hmax': 'Altura Máxima del Oleaje (m)', 'MeanDir': 'Direcc. Media de Proced. (º)', 'MeanDirPeak': 'Direcc. de pico de proced. (º)', 'Tm02': 'Periodo Medio Tm02 (s)', 'Tp': 'Periodo de Pico (s)'})
    table_df["StationCode"]=station

    return table_df

def met_office_table_scraping(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html = driver.page_source.encode("utf-8")
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    #saves values from the table as td objects
    td_objs=[BeautifulSoup(f"{td}","html.parser").td for td in soup.find_all("td")]

    #initialise category containers
    temperature_td = []
    wind_td = []
    humidity_td = []
    pressure_td = []
    dew_point_td = []
    sea_temperature_td = []
    wave_height_td = []
    wave_period_td = []


    #fill category containers with td data
    for td in td_objs:
        if td["data-test-label"].startswith("temp"):
            temperature_td.append(td)
        elif td["data-test-label"].startswith("wind"):
            wind_td.append(td)
        elif td["data-test-label"].startswith("humidity"):
            humidity_td.append(td)
        elif td["data-test-label"].startswith("pressure"):
            pressure_td.append(td)
        elif td["data-test-label"].startswith("dewPoint"):
            dew_point_td.append(td)
        elif td["data-test-label"].startswith("waveHeight"):
            wave_height_td.append(td)
        elif td["data-test-label"].startswith("wavePeriod"):
            wave_period_td.append(td)
        elif td["data-test-label"].startswith("seaTemp"):
            sea_temperature_td.append(td)

    #initialize empty dictionary
    df_dict={}

    #data extraction
    for i in range(len(temperature_td)):

        temperature=temperature_td[i]
        wind=wind_td[i]
        humidity=humidity_td[i]
        pressure=pressure_td[i]
        dew_point=dew_point_td[i]
        sea_temperature=sea_temperature_td[i]
        wave_height=wave_height_td[i]
        wave_period=wave_period_td[i]

        #extract date and time
        date_raw=temperature["data-test-label"].split('-')
        day_time_raw=date_raw[-1].split("T")
        time_raw=day_time_raw[1].split(":")
        year,month,day=date_raw[1],date_raw[2],day_time_raw[0]
        hour,minutes=time_raw[0],time_raw[1]
        #print(year,month,day,hour,minute)

        #extract temperature
        temperature=temperature.div["data-value"]

        #extract wind speed and direction (kt)
        wind_raw = wind.div["aria-label"].split(" ")
        wind_speed, wind_direction = wind_raw[0], wind_raw[2]

        #extract humidity (%)
        humidity=humidity.span["data-value"]

        #extract pressure (hPa)
        pressure=pressure.span["data-value"].split('.')[0]
        
        #extract dew point (°C)
        dew_point=dew_point.span["data-value"]

        #extract sea temperature (°C)
        sea_temperature=sea_temperature.span["data-value"]

        #extract wave height (m) and period (s)
        wave_height=wave_height.span["data-value"]
        wave_period=wave_period.span["data-value"]

        if i == 0:
            df_dict["Temperatura (°C)"]= [f"{temperature}"]
            df_dict["Altura Signif. del Oleaje (m)"]= [f"{wave_height}"]
            df_dict["Periodo Medio Tm02 (s)"]= [f"{wave_period}"]
            df_dict["Temperatura del mar (°C)"]= [f"{sea_temperature}"]
            df_dict["Presión atmosférica (hPa)"]= [f"{pressure}"]
            df_dict["Viento (kt)"]= [wind_speed]
            df_dict["Dirección del viento"]= [wind_direction]
            df_dict["Punto de rocío (°C)"]= [f"{dew_point}"]
            df_dict["Humedad"]= [f"{humidity}%"]
            df_dict["Fecha  (GMT)"]=[f"{year}-{month}-{day} {hour}:{minutes}:00"]
        else:
            df_dict["Temperatura (°C)"].append(f"{temperature}")
            df_dict["Altura Signif. del Oleaje (m)"].append(f"{wave_height}")
            df_dict["Periodo Medio Tm02 (s)"].append (f"{wave_period}")
            df_dict["Temperatura del mar (°C)"].append (f"{sea_temperature}")
            df_dict["Presión atmosférica (hPa)"].append(f"{pressure}")
            df_dict["Viento (kt)"].append(wind_speed)
            df_dict["Dirección del viento"].append(wind_direction)
            df_dict["Punto de rocío (°C)"].append(f"{dew_point}")
            df_dict["Humedad"].append(f"{humidity}%")
            df_dict["Fecha  (GMT)"].append(f"{year}-{month}-{day} {hour}:{minutes}:00")

    df = pd.DataFrame(df_dict)
    return df

    

def labouee_table_scraping(url):
    '''This function take an URL of the real time buoys webpage from the website https://labouee.app/en and extracts the real time data which wwill be plotted in an interactive map
    input -> URL, output -> pandas dataframe with the most recent buoy reading'''
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)
    html = driver.page_source.encode("utf-8")
    driver.quit()

    #Tidy up the HTML code
    soup = BeautifulSoup(html, "html.parser")

    #saves values from the table
    td_texts = [td.get_text(strip=True) for td in soup.find_all("td")]
    #print(td_texts)
    # drop leading empty strings
    while td_texts and td_texts[0] == '':
        del td_texts[0]

    # Check if td_texts is empty after cleaning
    if not td_texts or len(td_texts) < 6:
        print(f"Warning: Expected at least 6 data elements, but found {len(td_texts)}. URL: {url}")
        return pd.DataFrame()  # Return empty dataframe instead of crashing

    #we are interested in the fist 8 values
    #extract date and time values for last observation from the raw_extract 
    date_last_raw=td_texts[0].split(" ")
    month_dict = {"jan": 1, "feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
    month_last=month_dict[date_last_raw[0].lower()]
    year_last=datetime.date.today().year
    day_last=date_last_raw[1].replace(',','')
    time_last=date_last_raw[2]
    date_last=f"{year_last}-{month_last}-{day_last} {time_last}:00"
    #extract wave values and wave energy
    wave_sig_last=td_texts[1].replace('kJ','').split("m")[0]
    wave_energy=td_texts[1].replace('kJ','').split("m")[1]
    wave_max=td_texts[2].replace('m','')
    wave_period=td_texts[3].replace('s','')
    #extract sea temperature
    sea_temperature=td_texts[5].replace('°C','')

    #convert extracted data to dictionary
    df_dict={"Fecha  (GMT)":date_last,"Altura Signif. del Oleaje (m)":wave_sig_last,"Altura Máxima del Oleaje (m)":wave_max,"Energía del Oleaje (kJ)":wave_energy,"Periodo Medio Tm02 (s)":wave_period,"Temperatura del mar (°C)":sea_temperature}

    #convert disctionary in pd dataframe
    df = pd.DataFrame([df_dict])
    return df

