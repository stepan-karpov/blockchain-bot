from typing import Dict, Any
import datetime
import requests
import json

from src.common import BASE_URL
from backtester.mocked_api.consts import MOCKED_DATA_DIR
from src.api.api import InternalAPIConnection
from common import SYMBOLS



def make_request(endpoint, params=None):
  response = requests.get(BASE_URL + endpoint, params=params)
  result = response.json()
  return result

def GetSymbolTimerow(symbol, human_readable: bool = False) -> Dict[str, str]:
  params = {"symbol": symbol, "interval": "1m"}
  price_items = make_request("/api/v3/klines", params)
  time_to_price = {}
  for price_item in price_items:
    current_time = (price_item[0] + price_item[6]) // 2
    current_price = (float(price_item[1]) + float(price_item[4])) / 2
    current_time_human_readable = datetime.datetime.fromtimestamp(current_time // 1000).isoformat()
    time_to_price[current_time_human_readable] = current_price

  return time_to_price




def fill_mocked_data():
  connection = InternalAPIConnection()

  for symbol in SYMBOLS:
    data = {}
    data["timerow"] = connection.GetSymbolTimerow(symbol, False)

    with open(MOCKED_DATA_DIR + str(symbol) + ".json", 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
  fill_mocked_data()