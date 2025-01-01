import time
from typing import List

from src.symbol.symbol import Symbol
from src.api.api import InternalAPIConnection
import src.logs.log as log 

class SimplePoller:
  def __init__(self, connection, strategy, symbol_names_to_poll):
    self.connection = connection
    self.strategy = strategy
    self.symbols: List[Symbol] = []

    for symbol_name_to_poll in symbol_names_to_poll:
      current_symbol = Symbol(symbol_name_to_poll)
      log.info(f"{symbol_name_to_poll} added to list of symbols to poll")
      self.symbols.append(current_symbol)
  
  def Run(self, SleepFunction, EndFunction):
    while True:
      for symbol in self.symbols:
        symbol.Actualize(self.connection)

        order_parameters = self.strategy.DecideIfBuy(symbol)
        if len(order_parameters) == 0:
          continue
        symbol.Buy(self.connection, order_parameters)
        
        order_parameters = self.strategy.DecideIfSell(symbol)
        if len(order_parameters) == 0:
          continue
        symbol.Sell(self.connection, order_parameters)


      SleepFunction()
      if EndFunction():
        return
