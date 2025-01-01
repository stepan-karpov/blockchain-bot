from typing import Dict, Any
import random

from src.base_strategy import Strategy
from src.symbol.symbol import Symbol


class StrategyStupid(Strategy):
  def __init__(self):
    pass
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
    if random.random() > 0.9:
      return {}

    order_params = {
      "order_type": "MARKET",
      "quantity": self.DEFAULT_BUY_AMOUNT_USDT[symbol.name],
    }
    return order_params

  def DecideIfSell(self, symbol: Symbol) -> Dict[str, Any]:
    if random.random() > 0.9:
      return {}

    order_params = {
      "order_type": "MARKET",
      "quantity": self.DEFAULT_BUY_AMOUNT_USDT[symbol.name],
    }
    return order_params
