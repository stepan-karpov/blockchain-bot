from typing import Dict, Any
import random

from src.base_strategy import Strategy
from src.symbol.symbol import Symbol


class StrategyStupid(Strategy):
  def __init__(self):
    self.DEFAULT_BUY_AMOUNT_USDT = {
      "AITPROTOCOLUSDT": 1,
      "ETHUSDT": 1,
      "PEPEUSDT": 1,
      "JUPUSDT": 1,
      "WIFUSDT": 1,
      "GNSUSDT": 1,
      "ZEREBROUSDT": 1,
      "MEMESAIUSDT": 1,
      "SOLUSDT": 1,
      "BTCUSDT": 1
    }
    self.DEFAULT_SELL_AMOUNT_USDT = self.DEFAULT_BUY_AMOUNT_USDT

  def DecideIfBuy(self, symbol: Symbol) -> Dict[str, Any]:
    if random.random() > 0.1:
      return {}
  
    account_info = symbol.GetAccountInfo()
    usdt_balance = 0
    for item in account_info["balances"]:
      if (item["asset"] == "USDT"):
        usdt_balance = float(item["free"])
        break

    if (self.DEFAULT_BUY_AMOUNT_USDT[symbol.name] > usdt_balance):
      return {}

    order_params = {
      "order_type": "MARKET",
      "quantity": self.DEFAULT_BUY_AMOUNT_USDT[symbol.name],
    }
    return order_params

  def DecideIfSell(self, symbol: Symbol) -> Dict[str, Any]:
    if random.random() > 0.1:
      return {}

    if (symbol.GetCurrentBalance() < self.DEFAULT_BUY_AMOUNT_USDT[symbol.name]):
      return {}

    order_params = {
      "order_type": "MARKET",
      "quantity": self.DEFAULT_BUY_AMOUNT_USDT[symbol.name],
    }
    return order_params
