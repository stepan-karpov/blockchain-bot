from typing import Dict
import time
import datetime
import requests

import psycopg2
from psycopg2 import sql

from symbols import SYMBOLS

BASE_URL = "https://api.mexc.com"

def make_request(endpoint, params=None):
  response = requests.get(BASE_URL + endpoint, params=params)
  result = response.json()
  return result

def write_symbol_timerow(symbol, start_time, end_time, chunk_size, connection) -> None:
  seconds_number = (end_time - start_time) // 1000
  minutes_number = seconds_number // 60

  timerow = []

  last_start_time = start_time

  for _ in range(minutes_number // chunk_size + 1):
    current_start_time = last_start_time
    current_end_time = last_start_time + chunk_size * 60 * 1000

    # print(last_start_time, "====", current_end_time)
    last_start_time = current_end_time

    params = {"symbol": symbol, "interval": "1m", "startTime": current_start_time, "endTime": current_end_time, "limit": 500}
    try: # sometimes network flaps
      current_timerow = make_request("/api/v3/klines", params)
    except:
      current_timerow = make_request("/api/v3/klines", params)
    if (len(current_timerow) < 500):
      print("There are no data with such precision in MEXC API")
    timerow.extend(current_timerow)


  print(f"Symbol={symbol} was downloaded, {len(timerow)} records collected")
  timerow = [(symbol, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]) for value in  timerow]

  # print(timerow)
  cursor = connection.cursor()
  insert_query = "INSERT INTO testing.currencies_history (currency, open_time, value, high, low, close, volume, close_time, quote_asset_volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  cursor.executemany(insert_query, timerow)
  connection.commit()
  cursor.close()


def fill_mocked_data(connection, to_delete_old=False):
  now = datetime.datetime.now()
  N = 30
  d = 30
  start_time = int(time.mktime((now - datetime.timedelta(days=N)).timetuple()) * 1000)
  end_time = int(time.mktime((now - datetime.timedelta(days=N - d)).timetuple()) * 1000)
  chunk_size = 500
  if to_delete_old:
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE testing.currencies_history")
    connection.commit()
    cursor.close()

  for symbol in SYMBOLS:
    write_symbol_timerow(symbol, start_time, end_time, chunk_size, connection)

print("starting to download last 30 days data")
connection = psycopg2.connect(
    dbname="postgres",
    user="root",
    password="root",
    host="localhost",
    port="5432"
)
print("connection to postgres OK")
fill_mocked_data(connection, True)
connection.close()
print("finished to download last 30 days data")