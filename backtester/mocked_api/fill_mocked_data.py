from typing import Dict, Any
import time
import datetime
import requests
import json

from src.common import BASE_URL
from backtester.mocked_api.consts import MOCKED_DATA_DIR
from src.api.api import InternalAPIConnection

def make_request(endpoint, params=None):
  response = requests.get(BASE_URL + endpoint, params=params)
  result = response.json()
  return result

def GetSymbolTimerow(symbol, start_time, end_time, chunk_size) -> Dict[str, str]:
  seconds_number = (end_time - start_time) // 1000
  minutes_number = seconds_number // 60

  timerow = []

  last_start_time = start_time

  for _ in range(minutes_number // chunk_size + 1):
    current_start_time = last_start_time
    current_end_time = last_start_time + chunk_size * 60 * 1000

    print(last_start_time, "====", current_end_time)
    last_start_time = current_end_time

    params = {"symbol": symbol, "interval": "1m", "startTime": current_start_time, "endTime": current_end_time, "limit": 500}
    try: # sometimes network flaps
      current_timerow = make_request("/api/v3/klines", params)
    except:
      current_timerow = make_request("/api/v3/klines", params)
    if (len(current_timerow) < 500):
      print("There are no data with such precision in MEXC API")
    timerow.extend(current_timerow)
  print(f"Symbol={symbol} was downloaded")
  return timerow



def fill_mocked_data():
  now = datetime.datetime.now()
  N = 30
  d = 30
  start_time = int(time.mktime((now - datetime.timedelta(days=N)).timetuple()) * 1000)
  end_time = int(time.mktime((now - datetime.timedelta(days=N - d)).timetuple()) * 1000)
  chunk_size = 500

  for symbol in ["ETHUSDT", "PEPEUSDT", "JUPUSDT", "WIFUSDT", "GNSUSDT"]:
    data = {}
    data["timerow"] = GetSymbolTimerow(symbol, start_time, end_time, chunk_size)

    with open(MOCKED_DATA_DIR + str(symbol) + ".json", 'w') as file:
      json.dump(data, file)

if __name__ == "__main__":
  fill_mocked_data()