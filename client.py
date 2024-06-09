from telethon import TelegramClient, events
import MetaTrader5 as mt5
import os
import itertools
from dotenv import load_dotenv

load_dotenv()

api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('copier', api_id, api_hash)

action_queue = []

"""
To Do:
- Add function to place trades
- Add function to move stop loss
- Add function to close trades
- Add these to a queue to be executed in order
- intergrate NLP model to understand messages better
- Add function to log trades and actions with date and time

"""

async def main():
    await client.start()
    print("Client Started and Connected")

    @client.on(events.NewMessage(chats=1001268664484))
    async def handler(event):
        text = event.text.lower()
        print(text)
        if 'buy' in text or 'sell' in text:
            #function to place trades
            await client.send_message('me', event.text)
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

def message_simplify(text):
    return ''.join(
        ch for ch, _ in itertools.groupby(text)
    )