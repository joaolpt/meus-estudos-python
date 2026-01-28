import requests


def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)
    data = response.json()
    return data
