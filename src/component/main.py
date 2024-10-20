import time
from typing import List

from src.symbol.symbol import Symbol
from src.api.api import InternalAPIConnection
import src.logs.log as log 

from strategy_stupid1.main import StrategyStupid1 # import strategy

if __name__ == "__main__":
  symbol_names_to_poll = ["AITPROTOCOLUSDT"]
  symbols: List[Symbol] = []
  strategy = StrategyStupid1()
  connection = InternalAPIConnection()
  log.clear_logs()

  for symbol_name_to_poll in symbol_names_to_poll:
    current_symbol = Symbol(symbol_name_to_poll)
    log.info(f"{symbol_name_to_poll} added to list of symbols to poll")
    symbols.append(current_symbol)

  cnt = 0
  while True:
    cnt += 1
    for symbol in symbols:
      symbol.Actualize(connection)
      if symbol.bought_amount_usdt == 0:
        order_parameters = strategy.DecideIfBuy(symbol)
        if len(order_parameters) == 0:
          continue
        try:
          connection.Buy(order_parameters)
          symbol.bought_amount_usdt += order_parameters["quantity"]
        except Exception as e:
          log.error(str(e))
      else:
        order_parameters = strategy.DecideIfSell(symbol)
        if len(order_parameters) == 0:
          continue
        try:
          connection.Sell(order_parameters)
          symbol.bought_amount_usdt -= order_parameters["quantity"]
        except Exception as e:
          log.error(str(e))

    time.sleep(100)
    if cnt == 2:
      break

