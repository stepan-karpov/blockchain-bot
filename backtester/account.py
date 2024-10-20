import src.logs.log as log
from common import SYMBOLS

class Account:
  def __init__(self):
    self.comission = 0.02 / 100
    self.state = {
      "USDT": 50,
    }
    for symbol in SYMBOLS:
      self.state[symbol] = 0

  def Buy(self, symbol_to_buy, quantity, price):
    log.info(f"{symbol_to_buy} / USDT = {price}")
    value = price * quantity
    self.state["USDT"] -= value * (1 + self.comission)
    if self.state["USDT"] < 0:
      raise Exception("BANKROT")
    self.state[symbol_to_buy] += quantity
    self.PrintState()
    

  def Sell(self, symbol_to_buy, quantity, price):
    log.info(f"{symbol_to_buy} / USDT = {price}")
    value = price * quantity 
    self.state["USDT"] += value * (1 - self.comission)
    self.state[symbol_to_buy] -= quantity
    self.PrintState()
  
  def PrintState(self):
    log.info(str(self.state))