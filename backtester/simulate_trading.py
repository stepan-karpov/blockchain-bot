import time
from typing import List

from backtester.mocked_api.api import MockInternalAPIConnection
from backtester.account import Account
import backtester.time as backtester_time
import src.logs.log as log
from common import SYMBOLS

from src.component.simple_polling import SimplePoller # executor
from strategy_stupid1.main import StrategyStupid1 # import strategy

if __name__ == "__main__":
  testing_account = Account()

  log.clear_logs()

  connection = MockInternalAPIConnection(testing_account)
  strategy = StrategyStupid1()
  
  simple_poller = SimplePoller(connection, strategy, SYMBOLS)

  def SleepFunction():
    backtester_time.current_time += 2 * backtester_time.MINUTE # 1 min
    # time.sleep(0.1)

  def EndFunction() -> bool:
    return backtester_time.current_time > backtester_time.END_TIME

  simple_poller.Run(SleepFunction, EndFunction)

  

  log.info("=" * 10 + "\n\n")
  testing_account.PrintState()
