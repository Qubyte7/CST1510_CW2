import requests as rq
import pandas as pd
from pathlib import Path


URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
PARAMS = {"format":"geojson","minmagnitude":2.5,"limit":500}

# Filter and renaming columns
RENAME = {
        "properties_mag":"mag",
        "properties_time":"time",
        "properties_place":"location",
        "properties_alert":"alert",
        "properties_tsunami":"tsunami",
        "properties_sig":"sig",
        "properties_nst":"nst",
        "properties_magType":"magtype",
    
        }

KEEP = ["id","mag","time","location","alert","tsunami","sig","nst","magtype","geometry_coordinates"]
MUST_HAVE = ["id","location","geometry_coordinates","time"]
RECORDS_KEY = "features"
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"


def get_data(url, params):
    """ Fetches data from a url and returns JSON data or None if something is wrong"""
    try:
        response = rq.get(url,params=params,timeout=15)

        # let us check response status
        print(f"Status {response.status_code}")

        data = response.json()
        return data
    except rq.RequestException as error:
        print(f"An error occured {error}")
        return None
    
def make_table(data,records_key):
    """Turn JSON into normalized table dataframe"""
    records = data[records_key] if records_key else data
    table = pd.json_normalize(records,sep="_")
    print(table.shape)
    return table


def tidy_data(df):
    """ Rename,keep and drop na values so that we can remain with the one that wants"""
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df =  df.dropna(subset=MUST_HAVE)

    print(df.head())
    return df

def save_data(df,path):
    """Save table as a CSV"""
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    data = get_data(URL,PARAMS)
    if data is not None:
        table = make_table(data,RECORDS_KEY)
        table = tidy_data(table)
        save_data(table,RAW_FILE)








