from backtester.mocked_api.api import MockInternalAPIConnection
from backtester.account import Account
import backtester.time as backtester_time

from src.components.simple_polling import SimplePoller # executor
from strategy_stupid.main import StrategyStupid # import strategy

import src.logs.log as log

if __name__ == "__main__":
  log.clear_logs()

  testing_account = Account()

  connection = MockInternalAPIConnection(testing_account)
  strategy = StrategyStupid()
  simple_poller = SimplePoller(connection, strategy, ['AITPROTOCOLUSDT'])

  def SleepFunction():
    backtester_time.current_time += 2 * backtester_time.MINUTE # 2 min

  def EndFunction() -> bool:
    return backtester_time.current_time > backtester_time.END_TIME

  simple_poller.Run(SleepFunction, EndFunction)


  log.info("=" * 10 + "\n\n")
  testing_account.PrintState()
