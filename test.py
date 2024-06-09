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


async def main():
    # Start client
    await client.start()
    print("Client Started and Connected")

    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    
with client:
    client.loop.run_until_complete(main())
