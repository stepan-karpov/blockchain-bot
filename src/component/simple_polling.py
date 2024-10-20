import time
from typing import List

from src.symbol.symbol import Symbol
from src.api.api import InternalAPIConnection
import src.logs.log as log 

from strategy_stupid1.main import StrategyStupid1 # import strategy

class SimplePoller:
  def __init__(self, connection, strategy, symbol_names_to_poll):
    self.connection = connection
    self.strategy = strategy
    self.symbol_names_to_poll = symbol_names_to_poll
    self.symbols: List[Symbol] = []

    for symbol_name_to_poll in self.symbol_names_to_poll:
      current_symbol = Symbol(symbol_name_to_poll)
      log.info(f"{symbol_name_to_poll} added to list of symbols to poll")
      self.symbols.append(current_symbol)
  
  def Run(self, SleepFunction, EndFunction):
    while True:
      for symbol in self.symbols:
        symbol.Actualize(self.connection)

        if symbol.bought_amount_usdt == 0:
          order_parameters = self.strategy.DecideIfBuy(symbol)
          if len(order_parameters) == 0:
            continue
          symbol.Buy(self.connection, order_parameters)
        else:
          order_parameters = self.strategy.DecideIfSell(symbol)
          if len(order_parameters) == 0:
            continue
          symbol.Sell(self.connection, order_parameters)


      SleepFunction()
      if EndFunction():
        return
