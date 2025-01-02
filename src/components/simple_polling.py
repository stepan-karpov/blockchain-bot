from typing import List

from src.symbol.symbol import Symbol
import src.logs.log as log 

class SimplePoller:
  def __init__(self, connection, strategy, symbol_names_to_poll):
    self.connection = connection
    self.strategy = strategy
    self.symbols: List[Symbol] = []

    for symbol_name_to_poll in symbol_names_to_poll:
      current_symbol = Symbol(symbol_name_to_poll, connection)
      log.info(f"{symbol_name_to_poll} added to list of symbols to poll")
      self.symbols.append(current_symbol)
  
  def Run(self, sleep_function, end_function):
    while True:
      for symbol in self.symbols:
        order_parameters_buy = self.strategy.DecideIfBuy(symbol)
        order_parameters_sell = self.strategy.DecideIfSell(symbol)
        
        if (order_parameters_buy != {}):
          symbol.Buy(order_parameters_buy)
        elif (order_parameters_sell != {}):
          symbol.Sell(order_parameters_sell)


      sleep_function()
      if end_function():
        return
