import os
import asyncio
from dotenv import load_dotenv
from roblox import Client
from roblox.utilities.exceptions import *
load_dotenv()
RoClient = Client(os.getenv("ROBLOXTOKEN"))


async def main():
    group = await RoClient.get_group(16965138)
    users = await group.get_members().flatten(10)
    for user in users:
        print(f"{user.name} ({user.id})")
        
asyncio.run(main())