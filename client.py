from telethon import TelegramClient, events
import asyncio
import os
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
- Only execute by/sell orders if it is +/- 10 pips from entry price or within range
- Add function to read move sl messages and close trade messages
- Add function to log trades and actions with date and time

"""

premium_members = 1001268664484
testing_group = 4255421846


async def manage_queue():
    while True:
        if action_queue:
            action, symbol, price_range, sl, tps = action_queue[0]
            if action == "BUY":
                if get_current_price(symbol, action) >= price_range[0] and get_current_price(symbol, action) <= price_range[1]:
                    place_buy(symbol, 0.1, sl, tps)
                    action_queue.pop(0)
                    await client.send_message('me', f"Action: {action}, Symbol: {symbol}, Entry Price: {get_current_price(symbol, action)}, SL: {sl}, TPs: {tps}, status: placed")
            elif action == "SELL":
                if get_current_price(symbol, action) >= price_range[0] and get_current_price(symbol, action) <= price_range[1]:
                    place_sell(symbol, 0.1, sl, tps)
                    action_queue.pop(0)
                    await client.send_message('me', f"Action: {action}, Symbol: {symbol}, Entry Price: {get_current_price(symbol, action)}, SL: {sl}, TPs: {tps}, status: placed")
        await asyncio.sleep(1)
       

async def main():
    # Start client
    await client.start()
    print("Client Started and Connected")
    initialise_mt5()

    # Start queue manager
    asyncio.create_task(manage_queue())

    # Event handler for new messages
    @client.on(events.NewMessage(chats=testing_group))
    async def handler(event):
        text = event.text.lower()
        # print(text)
        if 'buy' in text or 'sell' in text:
            action, symbol, price_range, sl, tps = process_trading_signal(text)
            if action and symbol and price_range and sl:
                print(f"Action: {action}, Symbol: {symbol}, Price Range: {price_range}, SL: {sl}, TPs: {tps}")
                action_queue.append((action, symbol, price_range, sl, tps))

        elif "stoploss" and "entry" in text or "sl" and "entry" in text:
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

