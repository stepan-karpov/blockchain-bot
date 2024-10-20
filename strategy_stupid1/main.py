from typing import Dict, Any
import time

from src.base_strategy import Strategy
from src.symbol.symbol import Symbol

DEFAULT_BUY_AMOUNT_USDT = {
  "AITPROTOCOLUSDT": 10
}
DEFAULT_SELL_AMOUNT_USDT = DEFAULT_BUY_AMOUNT_USDT

class StrategyStupid1(Strategy):
  def DecideIfBuy(self, symbol: Symbol) -> Dict[str, Any]:
    if symbol.bought_amount_usdt > 0:
      return {}

    order_params = {
      "symbol": "AITPROTOCOLUSDT",
      "side": "BUY",
      "order_type": "MARKET",
      "quantity": DEFAULT_BUY_AMOUNT_USDT[symbol.name],
      "recvWindow": 50000,
      "timestamp_ms": int(time.time() * 1000)
    }
    return order_params

  def DecideIfSell(self, symbol: Symbol) -> Dict[str, Any]:
    if symbol.bought_amount_usdt == 0:
      return {}

    order_params = {
      "symbol": "AITPROTOCOLUSDT",
      "side": "SELL",
      "order_type": "MARKET",
      "quantity": DEFAULT_BUY_AMOUNT_USDT[symbol.name],
      "recvWindow": 50000,
      "timestamp_ms": int(time.time() * 1000)
    }
    return order_params