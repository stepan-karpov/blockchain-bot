import time

from src.api.api import InternalAPIConnection
from src.components.simple_polling import SimplePoller # executor
from strategy_stupid.main import StrategyStupid # import strategy

import src.logs.log as log

if __name__ == "__main__":
  log.clear_logs()
  
  connection = InternalAPIConnection()

  strategy = StrategyStupid()
  symbol_names_to_poll = ['AITPROTOCOLUSDT']  
  simple_poller = SimplePoller(connection, strategy, symbol_names_to_poll)

  def SleepFunction():
    time.sleep(120)

  def EndFunction():
    return False

  simple_poller.Run(SleepFunction, EndFunction)

  