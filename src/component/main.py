import time

from src.api.api import InternalAPIConnection
from src.component.simple_polling import SimplePoller # executor
from strategy_stupid1.main import StrategyStupid1 # import strategy

import src.logs.log as log
from common import SYMBOLS

if __name__ == "__main__":
  log.clear_logs()
  
  connection = InternalAPIConnection()

  strategy = StrategyStupid1()
  symbol_names_to_poll = SYMBOLS
  
  simple_poller = SimplePoller(connection, strategy, symbol_names_to_poll)


  def SleepFunction():
    time.sleep(120)

  def EndFunction():
    return False

  simple_poller.Run(SleepFunction, EndFunction)

  