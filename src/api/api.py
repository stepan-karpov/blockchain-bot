import requests
import datetime
import os
import json
import subprocess
import time
from typing import Dict, Any, List

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
    log.transaction(f"BUY={data['symbol']} parameters={data}")
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

    log.transaction(f"SELL={data['symbol']} parameters={data}")
    data["signature"] = self.get_signature(data)
    response = self.send_order(data)
    log.transaction(f"Answer from MEXC={response}")

  def GetSymbolTimerow(self, symbol) -> List[Any]:
    params = {"symbol": symbol, "interval": "1m", "limit": 1000}
    return self.make_request("/api/v3/klines", params)


  def GetAvgPrice(self, symbol) -> Dict[str, Any]:
    params = {"symbol": symbol}
    return self.make_request("/api/v3/avgPrice", params)

  def GetDefaultSymbols(self) -> Dict[str, Any]:
    return self.make_request("/api/v3/defaultSymbols")

  def GetAccountInfo(self) -> Dict[str, Any]:
    headers = {
        "X-MEXC-APIKEY": self.api_key,
        "Content-Type": "application/json"
    }
    timestamp = int(time.time() * 1000)
    parameters = {
      "timestamp": timestamp,
      "recvWindow": 5000,
      "signature": self.get_signature({"timestamp": timestamp, "recvWindow": 5000})
    }
    return self.make_request("/api/v3/account", headers=headers, parameters=parameters)

  # private: 
  def make_request(self, endpoint, parameters=None, headers=None, data=None):
    response = requests.get(BASE_URL + endpoint, params=parameters, headers=headers, data=data)
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
    response = requests.post(BASE_URL + "/api/v3/order/test", headers=headers, data=data)
    log.debug(str(response.json))
    return response.json()
