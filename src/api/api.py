import requests
import datetime
import os
import json
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
    data = {
      "symbol": order_params["symbol"],
      "side": order_params["side"],
      "type": order_params["order_type"],
      "quantity": order_params["quantity"],
      "recvWindow": order_params["recvWindow"],
      "timestamp": order_params["timestamp_ms"],
    }
    log.transaction(f"BUY={data["symbol"]} parameters={data}")
    data["signature"] = self.get_signature(data)
    response = self.send_order(data)
    log.transaction(f"Answer from MEXC={response}")

  def Sell(self, order_params: Dict[str, Any]):
    data = {
      "symbol": order_params["symbol"],
      "side": order_params["side"],
      "type": order_params["order_type"],
      "quantity": order_params["quantity"],
      "recvWindow": order_params["recvWindow"],
      "timestamp": order_params["timestamp_ms"],
    }

    log.transaction(f"SELL={data["symbol"]} parameters={data}")
    data["signature"] = self.get_signature(data)
    response = self.send_order(data)
    log.transaction(f"Answer from MEXC={response}")

  def GetSymbolTimerow(self, symbol, human_readable: bool = False) -> Dict[str, str]:
    params = {"symbol": symbol, "interval": "1d"}
    price_items = self.make_request("/api/v3/klines", params)
    time_to_price = {}
    for price_item in price_items:
      current_time = (price_item[0] + price_item[6]) // 2
      current_price = (float(price_item[1]) + float(price_item[4])) / 2
      if human_readable:
        current_time = datetime.datetime.fromtimestamp(current_time // 1000).isoformat()

      time_to_price[current_time] = current_price
    return time_to_price

  def GetAvgPrice(self, symbol) -> Dict[str, Any]:
    params = {"symbol": symbol}
    return self.make_request("/api/v3/avgPrice", params)

  def GetDefaultSymbols(self) -> Dict[str, Any]:
    return self.make_request("/api/v3/defaultSymbols")

  # private: 
  def make_request(self, endpoint, params=None, headers=None):
    response = requests.get(BASE_URL + endpoint, params=params, headers=headers)
    result = response.json()
    return result

  def get_signature(self, order_params) -> str:
    query = ""
    for parameter_name, parameter_value in order_params.items():
      query += parameter_name + "=" + str(parameter_value) + "&"
    query = query[:-1]

    TEMPFILE_NAME = 'temp.sh'
    first_cmd = "echo -n \"" + query + "\" | openssl dgst -sha256 -hmac \"" + self.secret_key + "\""

    with open(TEMPFILE_NAME, 'w') as f:
        f.write(first_cmd)

    result = subprocess.run([f'bash "{TEMPFILE_NAME}"'], stdout=subprocess.PIPE, shell=True)
    signature = result.stdout.decode("utf-8")
    signature = signature[signature.find("(stdin)") + 9:-1]

    os.remove(TEMPFILE_NAME)
    return signature


  def send_order(self, data: Dict) -> None:
    headers = {
        "X-MEXC-APIKEY": self.api_key,
        "Content-Type": "application/json"
    }
    log.info(f"Sending order={data} to MEXC")
    response = requests.post(BASE_URL + "/api/v3/order", headers=headers, data=data)
    log.debug(str(response.json))
    return response.json()
