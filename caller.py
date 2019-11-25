import numpy as np
import pandas as pd
import json
import requests
import yaml

def get_config():
    return yaml.safe_load(open("config.yaml"))


def is_crypto(ticker):
    if(ticker == 'BTC' or ticker == 'LTC' or ticker == 'ETH' or \
        ticker == 'DOGE' or ticker == 'BCH'):
        return 'DIGITAL_CURRENCY_DAILY'
    return 'TIME_SERIES_DAILY'

def is_cryptocurrency(ticker):
    if(ticker == 'BTC' or ticker == 'LTC' or ticker == 'ETH' or \
        ticker == 'DOGE' or ticker == 'BCH'):
        return True
    elif(ticker == 'BTCUSD' or ticker == 'LTCUSD' or ticker == 'ETHUSD' or \
        ticker == 'DOGEUSD' or ticker == 'BCHUSD'):
        return True
    return False


def fetch_latest_BTC_JSON(config_file,ticker,interval):
    """Fetch the latest JSON data
    """
    av_apikey = config_file['alpha_vantage_key']
    API_LINK = 'https://www.alphavantage.co/query?' + \
               'function={}&symbol={}&market=USD&apikey={}'.format(interval,ticker,av_apikey)
    print('FINAL LINK = ', API_LINK)
    page = requests.get(API_LINK).json()
    return page

def parse_alphaV_JSON(raw_data,interval):
    # Remove meta data for now
    raw_data.pop('Meta Data',None)
    # Remove key name
    df = None
    if(interval == 'DIGITAL_CURRENCY_DAILY'):
        df = pd.DataFrame.from_dict(raw_data['Time Series (Digital Currency Daily)'],dtype=float)
    elif(interval == 'TIME_SERIES_DAILY'):
        df = pd.DataFrame.from_dict(raw_data['Time Series (Daily)'],dtype=float)
    # Flip dates as columns into rows
    df = df.transpose()
    return df

def get_index(ticker):
    exchange_name = ''
    if(is_cryptocurrency(ticker)):
        if(ticker == 'DOGEUSD'):
            exchange_name == 'BITTREX'
        else:
            exchange_name = 'COINBASE'
    else:
        api_key = 'Tpk_a71985faa6ab4c84b8e2cfdb7b021731'
        info_link = 'https://sandbox.iexapis.com/stable/stock/{}/company?token={}'.format(ticker,api_key)
        data = requests.get(info_link).json()
        exchange_name = data['exchange']
        if(sorted(exchange_name) == sorted("NASDAQ")):
            exchange_name = "NASDAQ"
        elif(sorted(exchange_name) == sorted("New York Stock Exchange")):
            exchange_name = "New York Stock Exchange"
    return exchange_name
    

def main():
    config = get_config()
    contents = fetch_latest_BTC_JSON(config_file=config)
    close_prices = fetch_close_prices(contents)
    print(np.average(close_prices))
    

if __name__ == '__main__':
    main()