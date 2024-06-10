from telethon import TelegramClient, events
import MetaTrader5 as mt5
import os
import itertools
from dotenv import load_dotenv
from trader import *

load_dotenv()

api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('copier', api_id, api_hash)

testing_group = 4255421846

async def main():
    # Start client
    await client.start()
    print("Client Started and Connected")
    initialise_mt5()

    # Event handler for new messages
    @client.on(events.NewMessage(chats=testing_group))
    async def handler(event):
        text = event.text.lower()
        print(text)
        if 'buy' in text or 'sell' in text:
            action, symbol, entry_price, sl, tps = process_trading_signal(text)
            print(f"Action: {action}, Symbol: {symbol}, Entry Price: {entry_price}, SL: {sl}, TPs: {tps}")
            #just testing - change this to only execute if it is +/- 10 pips from entry price and add to queue
            if action == "BUY":
                place_buy(symbol, 0.1, sl, tps)
            elif action == "SELL":
                place_sell(symbol, 0.1, sl, tps)
            #function to place trades

    await client.run_until_disconnected()

    
with client:
    client.loop.run_until_complete(main())
