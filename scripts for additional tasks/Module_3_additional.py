import requests
from datetime import datetime

# Constants
API_KEY = 'fca_live_RyexoUQsFee3F3tBjdy03LsFEm6HqKhpesdByVBd'
URL_LATEST = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}'
URL_HISTORICAL = f'https://api.freecurrencyapi.com/v1/historical?apikey={API_KEY}'
URL_CURRENCY_INFO = f'https://api.freecurrencyapi.com/v1/currencies?apikey={API_KEY}'
CURRENCIES = ('USD', 'EUR', 'JPY', 'CAD', 'CHF', 'NZD')


# Function to get the latest currency exchange rates
def getLatestResults(currency_base):
    currencies = ','.join(CURRENCIES)
    url = f'{URL_LATEST}&base_currency={currency_base}&currencies={currencies}'
    result = requests.get(url).json()['data']
    if currency_base in result: del result[currency_base]
    return result


# Function to get the historical currency exchange rates
def getHistoricalResults(currency_base, date):
    currencies = ','.join(CURRENCIES)
    url = f'{URL_HISTORICAL}&date={date}&base_currency={currency_base}&currencies={currencies}'
    result = requests.get(url).json()['data'][date]
    if currency_base in result: del result[currency_base]
    return result


def getCurrencyAdditionalInfo():
    currencies = ','.join(CURRENCIES)
    url = f'{URL_CURRENCY_INFO}&currencies={currencies}'
    result = requests.get(url).json()['data']
    return result


def printCurrencies(dictionary_of_currencies):
    additional_info = getCurrencyAdditionalInfo()
    for carrency_name, value in dictionary_of_currencies.items():
        print(
            f"{carrency_name}: {value: .4f}, {additional_info[carrency_name]['symbol']}, {additional_info[carrency_name]['name']}")


if __name__ == '__main__':
    while True:
        currency_base = input(
            "What currency do you want to change? (press 'q' to quit): ").upper()  # Currency for exchange

        if currency_base == 'Q':
            exit()
        else:
            date = input('In what date are you interested in? (yyyy-mm-dd): ')  # Date of exchange

            # Try/except block for handling errors
            try:
                # if date is TODAY, then get the latest results of exchange rates
                if date == datetime.today().strftime('%Y-%m-%d'):
                    latest_results = getLatestResults(currency_base)
                    print("Here's your TODAY data:")
                    printCurrencies(latest_results)
                # if date is NOT TODAY, then get the historical results of exchange rates
                else:
                    historical_results = getHistoricalResults(currency_base, date)
                    print("Here's your HISTORICAL data:")
                    printCurrencies(historical_results)
            # If any error occurs, ask a user to try again and start the program from the beginning
            except:
                print("I can't load you any data with provided parameters. Try again!")
                continue
