from src.api.api import InternalAPIConnection
from common import SYMBOLS

def GetCurrentPrices(symbols):
  connection = InternalAPIConnection()
  for symbol in symbols:
    try:
      price = connection.GetAvgPrice(symbol)['price']
      print(f"symbol={symbol}, price={2 / float(price)}")
    except:
      pass

def AnalyzePossibleSymbols():
  symbols = []
  with open("/Users/stepan-karpov/Desktop/blockchain-bot/analytics/possible_symbols.txt", mode='r') as file:
    for line in file.readlines():
      if line.strip() == "":
        continue
      symbols.append(line.strip()[:-5] + "USDT")
    
  GetCurrentPrices(symbols)

def AnalyzeSnapshot():
  symbols = []
  with open("/Users/stepan-karpov/Desktop/blockchain-bot/analytics/snapshot.txt", mode='r') as file:
    for line in file.readlines():
      symbol = line[7:line.find(" ") - 1]
      price = float(line[line.find("price=") + 6:-1])

      if 0.6 < price < 1.5:
        symbols.append((price, symbol))

  symbols = sorted(symbols)
  print(symbols)
  print(len(symbols))

if __name__ == "__main__":
  # AnalyzeSnapshot()
  # AnalyzePossibleSymbols()
  GetCurrentPrices(SYMBOLS)
