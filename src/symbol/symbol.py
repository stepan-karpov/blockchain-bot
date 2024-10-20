import time

from src.api.api import InternalAPIConnection
import src.logs.log as log

class Symbol:
  def __init__(self, name):
    # public info
    self.name = name
    self.timerow = None
    self.depth = None

    # private info
    self.bought_amount_usdt = 0
    self.last_buy_at = None
    self.last_sell_at = None

  def Actualize(self, connection: InternalAPIConnection):
    log.info(f"Actualizing symbol={self.name}")
    self.timerow = connection.GetSymbolTimerow(self.name)
    self.depth = connection.GetSymbolDepth(self.name)
    log.debug(f"Actualizing symbol={self.name}")
    log.debug(f"Timerow={self.timerow}, depth={self.depth}\n\n\n")

  def Buy(self, connection, order_parameters):
    timestamp_ms = int(time.time() * 1000)

    order_parameters["symbol"] = self.name
    order_parameters["side"] = "BUY"
    order_parameters["recvWindow"] = 5000
    order_parameters["timestamp_ms"] = timestamp_ms

    try:
      connection.Buy(order_parameters)
      self.bought_amount_usdt += order_parameters["quantity"]
      self.last_buy_at = timestamp_ms
    except Exception as e:
          log.error(str(e))

  def Sell(self, connection, order_parameters):
    timestamp_ms = int(time.time() * 1000)

    order_parameters["symbol"] = self.name
    order_parameters["side"] = "SELL"
    order_parameters["recvWindow"] = 5000
    order_parameters["timestamp_ms"] = timestamp_ms

    try:
      connection.Sell(order_parameters)
      self.bought_amount_usdt += order_parameters["quantity"]
      self.last_buy_at = timestamp_ms
    except Exception as e:
          log.error(str(e))