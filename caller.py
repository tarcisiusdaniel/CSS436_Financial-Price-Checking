import numpy as np
import pandas as pd
import json
import requests
import yaml

def get_config():
    return yaml.safe_load(open("config.yaml"))

def fetch_latest_BTC_JSON(config_file):
    """Fetch the latest JSON data"""
    av_apikey = config_file['alpha_vantage_key']
    av_ticker = config_file['av_ticker']
    API_LINK = 'https://www.alphavantage.co/query?' + \
               'function=DIGITAL_CURRENCY_DAILY&' + \
               'symbol={}&market=USD&apikey={}'.format(av_ticker,av_apikey)
    page = requests.get(API_LINK).json()
    return page

def parse_alphaV_JSON(raw_data):
    # Remove meta data for now
    raw_data.pop('Meta Data',None)
    # Remove key name
    df = pd.DataFrame.from_dict(raw_data['Time Series (Digital Currency Daily)'],dtype=float)
    # Flip dates as columns into rows
    df = df.transpose()
    return df



def main():
    config = get_config()
    contents = fetch_latest_BTC_JSON(config_file=config)
    close_prices = fetch_close_prices(contents)
    print(np.average(close_prices))
    

if __name__ == '__main__':
    main()