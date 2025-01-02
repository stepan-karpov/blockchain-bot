from backtester.mocked_api.api import MockInternalAPIConnection
from backtester.account import Account
import backtester.time as backtester_time

from src.components.simple_polling import SimplePoller # executor
from strategy_stupid.main import StrategyStupid # import strategy

import psycopg2

import src.logs.log as log

if __name__ == "__main__":
  SYMBOLS = ["AITPROTOCOLUSDT", "ETHUSDT", "PEPEUSDT", "JUPUSDT", "WIFUSDT", "GNSUSDT", "ZEREBROUSDT", "MEMESAIUSDT", "SOLUSDT", "BTCUSDT"]
  log.clear_logs()
  pg_connection = psycopg2.connect(
      dbname="postgres",
      user="root",
      password="root",
      host="localhost",
      port="5432"
  )

  cursor = pg_connection.cursor()
  truncate_table = "TRUNCATE TABLE testing.currencies_values;"
  cursor.execute(truncate_table)
  pg_connection.commit()
  cursor.close()

  testing_account = Account(SYMBOLS)

  connection = MockInternalAPIConnection(testing_account)
  strategy = StrategyStupid()
  simple_poller = SimplePoller(connection, strategy, SYMBOLS)

  def SaveState():
    account_info = connection.GetAccountInfo()
    currencies = []
    total = 0
    for item in account_info["balances"]:
      currencies.append((item["asset"], backtester_time.current_time, item["free"]))
      total += float(item["free"])
    currencies.append(("TOTAL", backtester_time.current_time, total))

    cursor = pg_connection.cursor()
    insert_query = "INSERT INTO testing.currencies_values (currency, timestamp, value) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, currencies)
    pg_connection.commit()
    cursor.close()

    log.all("2 minutes passed")

  def SleepFunction():
    SaveState()
    backtester_time.current_time += 2 * backtester_time.MINUTE # 2 min

  def EndFunction() -> bool:
    return backtester_time.current_time > backtester_time.END_TIME

  try:
    simple_poller.Run(SleepFunction, EndFunction)
  except Exception as e:
    pg_connection.close()
    raise e

