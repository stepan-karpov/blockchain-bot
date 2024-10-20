import requests
import datetime
import os
import json
import time
import subprocess
from typing import Dict, Any

from src.common import BASE_URL
import src.logs.log as log

from backtester.mocked_api.consts import MOCKED_DATA_DIR
import backtester.time
from backtester.account import Account

class MockInternalAPIConnection:
  # public: 
  def __init__(self, account: Account):
    log.info("Internal API init")
    self.api_key = None
    self.secret_key = None
    self.account = account


  def Buy(self, order_params: Dict[str, Any]):
    log.transaction(f"BUY={order_params["symbol"]} parameters={order_params}")
    
    current_price = self.get_curret_price(order_params["symbol"])
    self.account.Buy(order_params["symbol"], order_params["quantity"], current_price)
    
    response = {}
    log.transaction(f"Answer from MEXC={response}")
    if response != {}:
      raise Exception("Buy trancation fail. " + str(response))

  def Sell(self, order_params: Dict[str, Any]):
    log.transaction(f"SELL={order_params["symbol"]} parameters={order_params}")
    
    current_price = self.get_curret_price(order_params["symbol"])
    self.account.Sell(order_params["symbol"], order_params["quantity"], current_price)
    
    response = {}
    log.transaction(f"Answer from MEXC={response}")
    if response != {}:
      raise Exception("Sell trancation fail. " + str(response))

  def GetSymbolTimerow(self, symbol) -> Dict[str, str]:
    params = {"symbol": symbol}
    data = {}
    with open(MOCKED_DATA_DIR + params["symbol"] + ".json", 'r') as file:
        data = json.load(file)
    to_return = {}
    for timestamp, value in data["timerow"].items():
      if int(timestamp) <= backtester.time.current_time:
        to_return[int(timestamp)] = value
    return to_return
  
  # private
  def get_curret_price(self, symbol) -> float:
    timerow = self.GetSymbolTimerow(symbol)
    last_value, last_timestamp = -1, -1

    for timestamp, value in timerow.items():
      if int(timestamp) > last_timestamp:
        last_timestamp = timestamp
        last_value = value

    return last_value
