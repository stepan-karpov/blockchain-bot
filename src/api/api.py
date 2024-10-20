import requests
import datetime
import os
import json
import time
import subprocess
from typing import Dict, Any

from src.common import BASE_URL, SECRETS_FILE
import src.logs.log as log

class InternalAPIConnection:
  # public: 
  def __init__(self):
    log.info("Internal API init")

    self.api_key = None
    self.secret_key = None

    with open(SECRETS_FILE, 'r') as file:
      data = json.load(file)
      self.api_key = data["api_key"]
      self.secret_key = data["secret_key"]

  def Buy(self, order_params: Dict[str, Any]):
    log.transaction(f"BUY={order_params["symbol"]} parameters={order_params}")
    response = self.send_order(order_params, self.get_signature(order_params))
    log.transaction(f"Answer from MEXC={response}")
    if response != {}:
      raise Exception("Buy trancation fail. " + str(response))

  def Sell(self, order_params: Dict[str, Any]):
    log.transaction(f"SELL={order_params["symbol"]} parameters={order_params}")
    response = self.send_order(order_params, self.get_signature(order_params))
    log.transaction(f"Answer from MEXC={response}")
    if response != {}:
      raise Exception("Sell trancation fail. " + str(response))

  def GetSymbolTimerow(self, symbol) -> Dict[str, str]:
    params = {"symbol": symbol}
    price_items = self.make_request("/api/v3/aggTrades", params)
    time_to_price = {}
    for price_item in price_items:
      time = datetime.datetime.fromtimestamp(price_item["T"] // 1000)
      time_to_price[time] = price_item["p"]
    return time_to_price

  def GetSymbolDepth(self, symbol) -> Dict[str, Any]:
    params = {"symbol": symbol}
    return self.make_request("/api/v3/depth", params)


  # private: 
  def make_request(self, endpoint, params=None):
    response = requests.get(BASE_URL + endpoint, params=params)
    result = response.json()
    return result

  def get_signature(self, order_params) -> str:
    symbol = order_params["symbol"]
    side = order_params["side"]
    order_type = order_params["order_type"]
    quantity = order_params["quantity"]
    recvWindow = order_params["recvWindow"]
    timestamp_ms = order_params["timestamp_ms"]
    TEMPFILE_NAME = 'temp.sh'

    query = f"symbol={symbol}&side={side}&type={order_type}&quantity={quantity}&recvWindow={recvWindow}&timestamp={timestamp_ms}"
    first_cmd = "echo -n \"" + query + "\" | openssl dgst -sha256 -hmac \"" + self.secret_key + "\""

    with open(TEMPFILE_NAME, 'w') as f:
        f.write(first_cmd)

    result = subprocess.run([f'bash "{TEMPFILE_NAME}"'], stdout=subprocess.PIPE, shell=True)
    signature = result.stdout.decode("utf-8")
    signature = signature[signature.find("(stdin)") + 9:-1]

    os.remove(TEMPFILE_NAME)
    return signature


  def send_order(self, order_params: Dict, signature: str) -> None:
    headers = {
        "X-MEXC-APIKEY": self.api_key,
        "Content-Type": "application/json"
    }
    data = {
        "symbol": order_params["symbol"],
        "side": order_params["side"],
        "type": order_params["order_type"],
        "quantity": order_params["quantity"],
        "recvWindow": order_params["recvWindow"],
        "timestamp": order_params["timestamp_ms"],
        "signature": signature
    }

    log.info(f"Sending order={order_params} to MEXC")
    response = requests.post(BASE_URL + "/api/v3/order", headers=headers, data=data)
    log.debug(str(response.json))
    return response.json()
