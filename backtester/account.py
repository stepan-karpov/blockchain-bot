import src.logs.log as log
from common import SYMBOLS

class Account:
  def __init__(self):
    self.comission = 0.02 / 100
    self.transactions_number = 0
    self.state = {
      "USDT": 50,
    }
    for symbol in SYMBOLS:
      self.state[symbol] = 0

    # not valid, for visualization only!!
    self.last_price = {}

  def Buy(self, symbol_to_buy, quantity, price):
    self.last_price[symbol_to_buy] = price

    log.info(f"{symbol_to_buy} / USDT = {price}")
    self.transactions_number += 1
    value = price * quantity
    self.state["USDT"] -= value * (1 + self.comission)
    if self.state["USDT"] < 0:
      assert False
    self.state[symbol_to_buy] += quantity
    self.PrintState()
    

  def Sell(self, symbol_to_sell, quantity, price):
    self.last_price[symbol_to_sell] = price

    log.info(f"{symbol_to_sell} / USDT = {price}")
    self.transactions_number += 1
    value = price * quantity 
    self.state["USDT"] += value * (1 - self.comission)
    self.state[symbol_to_sell] -= quantity
    if self.state[symbol_to_sell] < 0:
      assert False
    self.PrintState()
  
  def PrintState(self):
    log.info(str(self.state))
    usdt_value = self.state["USDT"]
    for symb_name, symb_value in self.state.items():
      if symb_name == "USDT":
        continue
      try:
        usdt_value += self.last_price[symb_name] * symb_value
      except:
        pass

    log.info(f"USDT ~ {usdt_value}, transactions_number = {self.transactions_number}")