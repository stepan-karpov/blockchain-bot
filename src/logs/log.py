import sys
import datetime

ALL_LOGS = "logs/all.txt"
DEBUG_FILE = "logs/debug.txt"
ERROR_FILE = "logs/error.txt"
INFO_FILE = "logs/info.txt"
TRANSACTIONS_INFO = "logs/transactions_info.txt"

def clear_logs():
  with open(ALL_LOGS, "w") as file:
    file.write("")
  with open(DEBUG_FILE, "w") as file:
    file.write("")
  with open(ERROR_FILE, "w") as file:
    file.write("")
  with open(INFO_FILE, "w") as file:
    file.write("")
  with open(TRANSACTIONS_INFO, "w") as file:
    file.write("")

def get_file_name():
    return sys.argv[0]

def get_current_time():
  if sys.argv[0].find("backtester") != -1:
    from backtester.time import current_time
    datetime_obj = datetime.datetime.fromtimestamp(current_time // 1000)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S' + "." + str(current_time % 1000))
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def all(string):
  with open(ALL_LOGS, "a+") as file:
    
    file.write(get_current_time() + " " + string + "\n")
    file.close()

def debug(string):
  # all(string)
  with open(DEBUG_FILE, "a+") as file:
    file.write(get_current_time() + " " + string + "\n")
    file.close()

def error(string):
  all("[ ERROR ] " + string)
  with open(ERROR_FILE, "a+") as file:
    file.write(get_current_time() + " " + string + "\n")
    file.close()

def info(string):
  all("[ INFO ] " + string)
  with open(INFO_FILE, "a+") as file:
    file.write(get_current_time() + " " + string + "\n")
    file.close()

def transaction(string):
  all("[ TRANSACTION ] " + string)
  with open(TRANSACTIONS_INFO, "a+") as file:
    file.write(get_current_time() + " " + string + "\n")
    file.close()