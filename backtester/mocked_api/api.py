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
    current_price = self.get_curret_price(order_params["symbol"])
    self.account.Buy(order_params["symbol"], order_params["quantity"], current_price)

  def Sell(self, order_params: Dict[str, Any]):
    current_price = self.get_curret_price(order_params["symbol"])
    self.account.Sell(order_params["symbol"], order_params["quantity"], current_price)

  def GetAccountInfo(self) -> Dict[str, Any]:
    return {
      'makerCommission': None,
      'takerCommission': None,
      'buyerCommission': None,
      'sellerCommission': None,
      'canTrade': True,
      'canWithdraw': True,
      'canDeposit': True,
      'updateTime': None,
      'accountType': 'SPOT',
      'balances': [{'asset': symbol, 'free': str(value), 'locked': '0'} for symbol, value in self.account.state.items()],
      'permissions': ['SPOT']
    }
  
  # private
  def get_curret_price(self, symbol) -> float:
    return 1
