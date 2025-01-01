import time

from src.api.api import InternalAPIConnection
import src.logs.log as log

class Symbol:
  def __init__(self, name, connection):
    # public info
    self.name = name
    self.connection: InternalAPIConnection = connection


  def GetTimerow(self):
    klines = self.connection.GetSymbolTimerow(self.name)
    log.info(f"Actualizing symbol={self.name}. Timerow size={len(klines)}")
    return [{kline[0], kline[1]} for kline in klines]

  def Buy(self, order_parameters):
    timestamp = int(time.time() * 1000)

    order_parameters["symbol"] = self.name
    order_parameters["side"] = "BUY"
    order_parameters["recvWindow"] = 5000
    order_parameters["timestamp_ms"] = timestamp

    try:
      self.connection.Buy(order_parameters)
    except Exception as e:
      log.error(str(e))

  def Sell(self, order_parameters):
    timestamp = int(time.time() * 1000)

    order_parameters["symbol"] = self.name
    order_parameters["side"] = "SELL"
    order_parameters["recvWindow"] = 5000
    order_parameters["timestamp_ms"] = timestamp

    try:
      self.connection.Sell(order_parameters)
    except Exception as e:
      log.error(str(e))