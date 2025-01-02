import time

import src.logs.log as log

class Symbol:
  def __init__(self, name, connection):
    # public info
    self.name = name
    self.connection = connection


  def GetTimerow(self):
    klines = self.connection.GetSymbolTimerow(self.name)
    log.info(f"Actualizing symbol={self.name}. Timerow size={len(klines)}")
    return [{kline[0], kline[1]} for kline in klines]

  def GetCurrentBalance(self):
    account_info = self.connection.GetAccountInfo()
    for item in account_info["balances"]:
      if item["asset"] == self.name:
        return float(item["free"])
    log.error("No symbol found in account")
    return 0

  def GetAccountInfo(self):
    return self.connection.GetAccountInfo()

  def Buy(self, order_parameters):
    timestamp = int(time.time() * 1000)

    order_parameters["symbol"] = self.name
    order_parameters["side"] = "BUY"
    order_parameters["recvWindow"] = 5000
    order_parameters["timestamp_ms"] = timestamp

    self.connection.Buy(order_parameters)

  def Sell(self, order_parameters):
    timestamp = int(time.time() * 1000)

    order_parameters["symbol"] = self.name
    order_parameters["side"] = "SELL"
    order_parameters["recvWindow"] = 5000
    order_parameters["timestamp_ms"] = timestamp

    self.connection.Sell(order_parameters)