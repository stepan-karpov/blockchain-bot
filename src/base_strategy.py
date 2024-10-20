from abc import ABC, abstractmethod

from src.symbol.symbol import Symbol

class Strategy(ABC):
  @abstractmethod
  def DecideIfBuy(self, symbol: Symbol) -> tuple[bool, float]:
    pass

  @abstractmethod
  def DecideIfSell(self, symbol: Symbol) -> tuple[bool, float]:
    pass
