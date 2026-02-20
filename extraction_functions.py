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
    '''This function take an URL of the real time buoys webpage from the website metoffice.gov.uk and extracts the real time data which wwill be plotted in an interactive map
    input -> URL, output -> pandas dataframe with the most recent buoy reading'''
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    driver.get(
        url
    )

    # wait up to 5 s, but return earlier if the table appears
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table")  # ideally a more specific selector
        )
    )

    html = driver.page_source
    driver.quit()

    #Tidy up the HTML code
    soup = BeautifulSoup(html, "html.parser")
    
    
    #saves values from the table
    td_texts = [td.get_text(strip=True) for td in soup.find_all("td")]

    td_texts_temp = td_texts.copy()

    #detect first offset
    offset = 0
    while td_texts_temp[offset].endswith("Celsius"):
        offset += 1

    #category containers
    temperature = []
    wind_raw = []
    humidity = []
    pressure = []
    dew_point = []
    sea_temperature = []
    wave_height = []
    wave_period = []

    categories = [
        temperature,
        wind_raw,
        humidity,
        pressure,
        dew_point,
        sea_temperature,
        wave_height,
        wave_period,
    ]

    #offsets for each block
    offsets = [offset, 24, 24 - offset]

    idx = 0  # pointer
    for block_offset in offsets:
        for cat in categories:
            cat.extend(td_texts_temp[idx:idx + block_offset])
            idx += block_offset
    
    #Remove the units of measurement
    temperature = [item.replace('°Celsius', '') for item in temperature]
    sea_temperature = [item.replace('°Celsius', '') for item in sea_temperature]
    pressure = [item.replace('hectopascals', '') for item in pressure]
    dew_point = [item.replace('°Celsius', '') for item in dew_point]
    wave_height = [item.replace('metres', '') for item in wave_height]
    wave_period = [item.replace('seconds', '') for item in wave_period]

    #extrapolate date and time from the table
    #saves values from the table

    li_texts = [ li.get_text(strip=True) for li in soup.find_all("li")]
    li_texts_date = [x for x in li_texts if x.startswith(('Mon ', 'Tue ', 'Wed ', 'Thu ', 'Fri ', 'Sat ', 'Sun '))]

    month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    day1=li_texts_date[0].split(" ")[1]
    month1=month_dict[li_texts_date[0].split(" ")[2][:3]]
    year1=datetime.date.today().year
    date1=f"{year1}-{month1}-{day1}"

    day2=li_texts_date[1].split(" ")[1]
    month2=month_dict[li_texts_date[1].split(" ")[2][:3]]
    year2=datetime.date.today().year
    date2=f"{year2}-{month2}-{day2}"

    day3=li_texts_date[2].split(" ")[1]
    month3=month_dict[li_texts_date[2].split(" ")[2][:3]]
    year3=datetime.date.today().year
    date3=f"{year3}-{month3}-{day3}"

    #print(date1, date2, date3)

    th_texts = [ th.get_text(strip=True) for th in soup.find_all("th")]
    th_texts_temp = [x for x in th_texts if x.startswith(('1','2','3','4','5','6','7','8','9','0'))]

    #print(th_texts_temp)
    #print(offset)

    for i in range(offset):
        th_texts_temp[i]=f"{date1} {th_texts_temp[i]}:00"
    offset1=offset+24
    for i in range(offset,offset1):
        th_texts_temp[i]=f"{date2} {th_texts_temp[i]}:00"
    offset2=offset1+24-offset
    for i in range(offset1,offset2):
        th_texts_temp[i]=f"{date3} {th_texts_temp[i]}:00"
    fecha=th_texts_temp.copy()

    print(fecha)

    #create disctionary for dataframe
    data_dict = {
        'Temperatura del mar (°C)': sea_temperature[-1],
        'Altura Signif. del Oleaje (m)': wave_height[-1],
        'Periodo Medio Tm02 (s)': wave_period[-1],
        'Fecha  (GMT)' : fecha[-1]
    }

    df = pd.DataFrame([data_dict])
    return df


def labouee_table_scraping(url):
    '''This function take an URL of the real time buoys webpage from the website https://labouee.app/en and extracts the real time data which wwill be plotted in an interactive map
    input -> URL, output -> pandas dataframe with the most recent buoy reading'''
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    driver.get(
        url
    )

    # wait up to 5 s, but return earlier if the table appears
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table")  # ideally a more specific selector
        )
    )

    html = driver.page_source
    driver.quit()

    #Tidy up the HTML code
    soup = BeautifulSoup(html, "html.parser")

    #saves values from the table
    td_texts = [td.get_text(strip=True) for td in soup.find_all("td")]
    # drop leading empty strings
    while td_texts and td_texts[0] == '':
        del td_texts[0]

    #we are interested in the fist 8 values
    
    #extract date and time values for last observation from the raw_extract 
    date_last_raw=td_texts[0].split(" ")
    month_dict = {"jan": 1, "feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
    month_last=month_dict[date_last_raw[0].lower()]
    year_last=datetime.date.today().year
    day_last=date_last_raw[1].replace(',','')
    hour, minute = date_last_raw[2].split(":")
    hour = int(hour)
    if date_last_raw[3].lower() == "pm" and hour != 12:
        hour += 12
    time_last=f"{hour:02d}:{minute}"
    #print(time_last)
    date_last=f"{year_last}-{month_last}-{day_last} {time_last}:00"
    #extract wave values and wave energy
    wave_sig_last=td_texts[1].replace('kJ','').split("m")[0]
    wave_energy=td_texts[1].replace('kJ','').split("m")[1]
    wave_max=td_texts[2].replace('m','')
    wave_period=td_texts[3].replace('s','')
    #extract sea temperature
    sea_temperature=td_texts[5].replace('°C','')

    df_dict={"Fecha  (GMT)":date_last,"Altura Signif. del Oleaje (m)":wave_sig_last,"Altura Máxima del Oleaje (m)":wave_max,"Energía del Oleaje (kJ)":wave_energy,"Periodo Medio Tm02 (s)":wave_period,"Temperatura del mar (°C)":sea_temperature}

    #convert disctionary in pd dataframe
    df = pd.DataFrame([df_dict])

    return df

