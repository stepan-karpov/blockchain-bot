import src.logs.log as log

class Account:
  def __init__(self, symbols):
    self.comission = 0.02 / 100
    self.transactions_number = 0
    self.state = {
      "USDT": 500,
    }
    for symbol in symbols:
      self.state[symbol] = 0


  def Buy(self, symbol_to_buy, quantity, price):
    self.transactions_number += 1
    value = price * quantity
    self.state["USDT"] -= value * (1 + self.comission)
    if self.state["USDT"] < 0:
      assert False
    self.state[symbol_to_buy] = self.state.get(symbol_to_buy, 0) + quantity
    

  def Sell(self, symbol_to_sell, quantity, price):
    self.transactions_number += 1
    value = price * quantity 
    self.state["USDT"] += value * (1 - self.comission)
    self.state[symbol_to_sell] = self.state.get(symbol_to_sell, 0) - quantity
    if self.state[symbol_to_sell] < 0:
      assert False
