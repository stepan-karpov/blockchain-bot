from src.api.api import InternalAPIConnection
import src.logs.log as log

class Symbol:
  def __init__(self, name):
    # public info
    self.name = name
    self.timerow = None
    self.depth = None

    # private info
    self.bought_amount_usdt = 0
    self.last_bought_at = None


  def Actualize(self, connection: InternalAPIConnection):
    log.info(f"Actualizing symbol={self.name}")
    self.timerow = connection.GetSymbolTimerow(self.name)
    self.depth = connection.GetSymbolDepth(self.name)
    log.debug(f"Actualizing symbol={self.name}")
    log.debug(f"Timerow={self.timerow}, depth={self.depth}\n\n\n")