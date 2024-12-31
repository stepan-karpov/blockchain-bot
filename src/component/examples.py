from src.api.api import InternalAPIConnection

import src.logs.log as log

if __name__ == "__main__":
  log.clear_logs()
  
  connection = InternalAPIConnection()
  
  # ========= to get default symbols
  # print(connection.GetDefaultSymbols())

  # ========= to buy symbol
  # from src.symbol.symbol import Symbol
  # symbol = Symbol("AITPROTOCOLUSDT")
  # order_params = {
  #   "order_type": "MARKET",
  #   "quantity": 20,
  # }
  # symbol.Buy(connection, order_params)

