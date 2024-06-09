import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# load_dotenv()

# login    = os.getenv("mt5_login")
# password = os.getenv("mt5_password")

# print(login, password)

# print(mt5.initialize())
# print(mt5.login(int(login), password ,server="MetaQuotes-Demo"))


def place_buy(symbol, volume, sl, *tps):
    for tp in tps:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        result = mt5.order_send(request)
        print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order send failed")
            print(result.comment)
            return False
    return True


def place_sell(symbol, volume, sl, *tps):
    for tp in tps:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        result = mt5.order_send(request)
        print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order send failed")
            print(result.comment)
            return False
    return True

def move_sl(new_sl, ticket):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": mt5.positions_get(ticket).symbol,
        "sl": new_sl,
        "tp": mt5.positions_get(ticket).tp,
        "position": ticket,
    }
    result = mt5.order_send(request)
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order send failed")
        print(result.comment)
        return False
    return True
    

def close_trade(ticket):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": mt5.positions_get(ticket).symbol,
        "volume": mt5.positions_get(ticket).volume,
        "type": mt5.ORDER_TYPE_CLOSE_BY,
        "position": ticket,
    }
    result = mt5.order_send(request)
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order send failed")
        print(result.comment)
        return False
    return True
    

