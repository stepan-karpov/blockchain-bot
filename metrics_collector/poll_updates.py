from typing import Dict
import time
import datetime
import requests

import psycopg2
from psycopg2 import sql

BASE_URL = "https://api.mexc.com"

from symbols import SYMBOLS

def make_request(endpoint, params=None):
  response = requests.get(BASE_URL + endpoint, params=params)
  result = response.json()
  return result

def write_symbol_timerow(symbol, start_time, end_time, connection) -> None:
  timerow = []

  params = {"symbol": symbol, "interval": "1m", "startTime": start_time, "endTime": end_time, "limit": 500}
  try: # sometimes network flaps
    current_timerow = make_request("/api/v3/klines", params)
  except:
    current_timerow = make_request("/api/v3/klines", params)
  timerow.extend(current_timerow)

  min_start_time = min([value[0] for value in timerow])

  print(f"Symbol={symbol} was downloaded, {len(timerow)} records collected")

  cursor = connection.cursor()

  query = """
  SELECT * FROM testing.currencies_history 
  WHERE currency = %s AND open_time >= %s
  """
  cursor.execute(query, (symbol, min_start_time))
  rows = cursor.fetchall()
  cursor.close()

  timestamps_to_skip = [(row[1], row[7]) for row in rows]

  new_timestamps = []
  for kline in timerow:
    if not (kline[0], kline[6]) in timestamps_to_skip:
      new_timestamps.append(kline)
  new_timestamps = [(symbol, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]) for value in  new_timestamps]

  print(f"Inserting {len(new_timestamps)} new values for symbol={symbol}")

  cursor = connection.cursor()
  insert_query = "INSERT INTO testing.currencies_history (currency, open_time, value, high, low, close, volume, close_time, quote_asset_volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  cursor.executemany(insert_query, new_timestamps)
  connection.commit()
  cursor.close()

def fill_mocked_data(connection, to_delete_old=False):
  now = datetime.datetime.now()
  start_time = int(time.mktime((now - datetime.timedelta(hours=4)).timetuple()) * 1000) # remember about timezone
  end_time = int(time.mktime((now - datetime.timedelta(seconds=0)).timetuple()) * 1000)
  
  for symbol in SYMBOLS:
    write_symbol_timerow(symbol, start_time, end_time, connection)

while True:
  print("starting update")
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
  print("update OK")
  time.sleep(30)