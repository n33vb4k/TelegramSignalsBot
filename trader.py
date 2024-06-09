import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

login    = os.getenv("mt5_login")
password = os.getenv("mt5_password")

print(login, password)

print(mt5.initialize())
print(mt5.login(int(login), password ,server="MetaQuotes-Demo"))


def place_trade():
    pass

def move_sl():
    pass

def close_trade():
    pass

