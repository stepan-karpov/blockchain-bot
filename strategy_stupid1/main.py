from typing import Dict, Any
import random

from src.base_strategy import Strategy
from src.symbol.symbol import Symbol
import src.logs.log as logs
from common import SYMBOLS



class StrategyStupid1(Strategy):
  def __init__(self):
    self.DEFAULT_BUY_AMOUNT_USDT = {
      "KDAUSDT": 3.29,
      "ELGUSDT": 3.22,
      "SYNUSDT": 3.11,
      "ERGUSDT": 2.98,
      "BNXUSDT": 2.92,
      "BAIUSDT": 2.82,
      "XIDOUSDT": 2.72,
      "W3SUSDT": 2.56,
      "HTMUSDT": 2.04,
      "FDUSDUSDT": 2.00,
      "EWTUSDT": 1.74,
      "SAKAIUSDT": 1.48,
      "TUBESUSDT": 1.48,
      "TBCUSDT": 1.45,
    }

    self.DEFAULT_SELL_AMOUNT_USDT = self.DEFAULT_BUY_AMOUNT_USDT

  def DecideIfBuy(self, symbol: Symbol) -> Dict[str, Any]:
    if symbol.bought_amount_usdt > 0:
      return {}
    
    if not (len(symbol.prices) >= 4 and symbol.prices[-4] < symbol.prices[-2] < symbol.prices[-1]):
      return {}

    if random.random() > 0.1:
      return {}

    order_params = {
      "order_type": "MARKET",
      "quantity": self.DEFAULT_BUY_AMOUNT_USDT[symbol.name],
    }
    return order_params

  def DecideIfSell(self, symbol: Symbol) -> Dict[str, Any]:
    if symbol.bought_amount_usdt == 0:
      return {}
    
    if not (len(symbol.prices) >= 4 and symbol.prices[-4] > symbol.prices[-2] > symbol.prices[-1]):
      return {}

    if random.random() > 0.1:
      return {}

    order_params = {
      "order_type": "MARKET",
      "quantity": self.DEFAULT_BUY_AMOUNT_USDT[symbol.name],
    }
    return order_params
