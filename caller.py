import numpy as np
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

def fetch_close_prices(content):
    prices = []
    for key,value in content['Time Series (Digital Currency Daily)'].items():
        prices.append(float(value['4a. close (USD)']))
    return np.array(prices)
    


def main():
    config = get_config()
    contents = fetch_latest_BTC_JSON(config_file=config)
    close_prices = fetch_close_prices(contents)
    print(np.average(close_prices))
    

if __name__ == '__main__':
    main()