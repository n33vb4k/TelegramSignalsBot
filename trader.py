import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import itertools
import os

def initialise_mt5():
    if not mt5.initialize():
        print("Failed to initialize")
        return
    print("MT5 Initialized")

    if not mt5.login(int(os.getenv("mt5_login")), os.getenv("mt5_password"), server="MetaQuotes-Demo"):
        print("Failed to login")
        return
    print("Logged in to MT5")


def place_buy(symbol, volume, sl, tps):
    for tp in tps:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234000,
            "comment": "python script", 
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        print("api returned:",result)

        if result is None:
            print(mt5.last_error())
            return False
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order send failed")
            print(result.comment)
            return False
        
        print(f"{symbol} {volume} lots at {mt5.symbol_info_tick(symbol).ask} placed")

    return True


def place_sell(symbol, volume, sl, tps):
    for tp in tps:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234000,
            "comment": "python script", 
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        print("api returned:",result)

        if result is None:
            print(mt5.last_error())
            return False
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order send failed")
            print(result.comment)
            return False
        
        print(f"{symbol} {volume} lots at {mt5.symbol_info_tick(symbol).bid} placed")
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
    

def message_simplify(text):
    return ''.join(
        ch for ch, _ in itertools.groupby(text)
    )


def process_trading_signal(message_text):
    lines = message_text.split('\n')
    action = None
    symbol = None
    entry_price = None
    sl = None
    tps = []

    for line in lines:
        if 'sell' in line or 'buy' in line:
            parts = line.split()
            if len(parts) >= 3:
                symbol = parts[0].upper()
                action = parts[1].upper()
                entry_price_range = parts[2].split('-')
                if len(entry_price_range) == 2:
                    entry_price = (float(entry_price_range[0]) + float(entry_price_range[1])) / 2
                else:
                    entry_price = float(entry_price_range[0])
        elif 'sl' in line:
            parts = line.split()
            sl = float(parts[1])
        elif 'tp' in line:
            parts = line.split()
            try:
                tps.append(float(parts[1]))
            except ValueError:
                continue

    return action, symbol, entry_price, sl, tps