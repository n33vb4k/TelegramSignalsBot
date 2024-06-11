from telethon import TelegramClient, events
import asyncio
import os
from dotenv import load_dotenv
from trader import *

load_dotenv()

api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('copier', api_id, api_hash)

action_stack = []
action_history = []

"""
To Do:
- Add function to close trade messages
- Add function to log trades and actions with date and time

"""

premium_members = 1001268664484
testing_group = 4255421846
lots = 0.01 

# results.order = position.ticket

async def manage_stack():
    while True:
        if action_stack:
            action, symbol, price_range, sl, tps = action_stack[-1]
            if action == "BUY" or action == "SELL":
                if get_current_price(symbol, action) >= price_range[0] and get_current_price(symbol, action) <= price_range[1]:
                    action_history.append(place_buy(symbol, lots, sl, tps) if action == "BUY" else place_sell(symbol, lots, sl, tps))
                    action_stack.pop(-1)
                    await client.send_message('me', f"Action: {action}\nSymbol: {symbol}\nEntry Price: {get_current_price(symbol, action)}\nSL: {sl}\nTPs: {tps}\nStatus: PLACED")
    
        await asyncio.sleep(1)
       

async def main():
    # Start client
    await client.start()
    print("Client Started and Connected")
    initialise_mt5()

    # Start queue manager
    asyncio.create_task(manage_stack())

    # Event handler for new messages
    @client.on(events.NewMessage(chats=testing_group))
    async def handler(event):
        text = event.text.lower()
        
        if 'buy' in text or 'sell' in text:
            action, symbol, price_range, sl, tps = process_trading_signal(text)
            if action and symbol and price_range and sl:
                print(f"Action: {action}, Symbol: {symbol}, Price Range: {price_range}, SL: {sl}, TPs: {tps}, Status: QUEUED")
                action_stack.append((action, symbol, price_range, sl, tps))
        elif ("stoploss" and "entry" in text) or ("sl" and "entry" in text) or ("stoploss" and "breakeven" in text) or ("sl" and "breakeven" in text):
            #function to move sl to entry
            if action_history:
                tickets = action_history[-1]
                for ticket in tickets:
                    position = mt5.positions_get(ticket=ticket)
                    success = move_sl(position[0], position[0].price_open, ticket)
                    if success:
                        await client.send_message('me',  f"SL moved to entry for {position[0].symbol} {position[0].volume} lots at {position[0].price_open} tp: {position[0].tp}")
        else:
            simplified_text = message_simplify(text)
            if "close now" in simplified_text or "closing now" in simplified_text or "closed all" in simplified_text or "im out" in simplified_text:
                if action_history:
                    tickets = action_history[-1]
                    for ticket in tickets:
                        position = mt5.positions_get(ticket=ticket)[0]
                        success = close_trade(position, ticket)
                        if success:
                            await client.send_message('me', f"Trade closed for {position.symbol} {position.volume} lots at {position.price_open} with {position.profit} profit")
            

    await client.run_until_disconnected()

    
with client:
    client.loop.run_until_complete(main())

