from typing import Tuple
from abc import ABC, abstractmethod

from src.symbol.symbol import Symbol

class Strategy(ABC):
  @abstractmethod
  def DecideIfBuy(self, symbol: Symbol) -> Tuple[bool, float]:
    pass

  @abstractmethod
  def DecideIfSell(self, symbol: Symbol) -> Tuple[bool, float]:
    pass
