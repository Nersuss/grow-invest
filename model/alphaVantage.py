import logging

import requests
api_key = 'ETYJF8AVBD4G6WO2'
# api_key = 'FBHPMXR7LC2AVHK0' 'ZEBSZMBM169YX5Z7'

def get_prices_by_symbol_and_period(symbol, period):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{period}&symbol={symbol}&apikey={api_key}&datatype=json'
    response = requests.get(url)
    data = response.json()
    logging.warning(data)
    return data

def get_symbols_by_chars(chars):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={chars}&apikey={api_key}&datatype=json'
    response = requests.get(url)
    data = response.json()
    logging.warning(data)
    return data

# def getDatasAndCloses(symbol, period):
#     api_key = 'ETYJF8AVBD4G6WO2'
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&datatype=json'
#     response = requests.get(url)
#     data = response.json()
#     result = []
#     closes = []
#     dates = []
#     for date, values in data['Time Series (Daily)'].items():
#        open_price = values['1. open']
#        result.append({'Date': date, 'Open': open_price})
#        dates.append(date)
#        closes.append(open_price)
#     return data