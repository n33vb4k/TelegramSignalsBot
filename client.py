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

action_queue = []

"""
To Do:
- Add orders to a queue to be executed in order
- Only execute by/sell orders if it is +/- 10 pips from entry price
- Add function to read move sl messages and close trade messages
- Add function to log trades and actions with date and time

"""

premium_members = 1001268664484
testing_group = 4255421846

async def main():
    # Start client
    await client.start()
    print("Client Started and Connected")

    # Initialize MT5
    if not mt5.initialize():
        print("Failed to initialize")
        return
    print("MT5 Initialized")

    # Login to MT5
    if not mt5.login(int(os.getenv("mt5_login")), os.getenv("mt5_password"), server="MetaQuotes-Demo"):
        print("Failed to login")
        return
    print("Logged in to MT5")

    # Event handler for new messages
    @client.on(events.NewMessage(chats=testing_group))
    async def handler(event):
        text = event.text.lower()
        print(text)
        if 'buy' in text or 'sell' in text:
            action, symbol, entry_price, sl, tps = process_trading_signal(text)
            #function to place trades
            await client.send_message('me', f"Action: {action}, Symbol: {symbol}, Entry Price: {entry_price}, SL: {sl}, TPs: {tps}")

        elif "stoploss" and "entry" in text:
            #function to move sl to entry
            await client.send_message('me', event.text)
        else:
            simplified_text = message_simplify(text)
            if "close" in simplified_text or "closing" in simplified_text or "closed" in simplified_text:
                #function to close trade
                await client.send_message('me', event.text)
    

    await client.run_until_disconnected()

    
with client:
    client.loop.run_until_complete(main())

