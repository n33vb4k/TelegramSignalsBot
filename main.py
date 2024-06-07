from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from funcs import *

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('copier', api_id, api_hash)


async def main():
    await client.start()
    print("Client Started and Connected")

    @client.on(events.NewMessage(chats='@Premium members'))
    async def handler(event):
        text = event.text.lower()
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
            

    
with client:
    client.loop.run_until_complete(main())
