import asyncio
import discord
import json
import openai
import os

from collections.abc import Iterable
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

with open("config.json") as f:
    config = json.load(f)

if os.path.exists("assets/iteminfo.json"):
    with open("assets/iteminfo.json") as f:
        iteminfo = json.load(f)
else:
    iteminfo = []

class Bot(commands.Bot):
    def __init__(
        self,
        command_prefix = "r!",
        intents: discord.Intents = discord.Intents.default(),
        extensions: Iterable = config["default_cogs"],
        **options
    ):
        self.to_add = extensions

        # This is used for when I'm hosting the bot on my own machine
        # Love you MC, but I don't want anyone having unrestricted shell access to my machine
        if os.getenv("TRUE_OWNER"):
            self.owners = [int(os.getenv("TRUE_OWNER"))]
        else:
            self.owners = config["owners"]

        self.colours = config["colours"]
        self.items = iteminfo.copy()
        super().__init__(command_prefix, intents=intents, **options)

    def save_items(self):
        with open("assets/iteminfo.json", "w") as f:
            json.dump(iteminfo, f, indent=4)

    def sync_items(self):
        self.items = iteminfo.copy()

    async def setup_hook(self) -> None:
        for extension in self.to_add:
            await self.load_extension(extension)

        await self.tree.sync()
        return await super().setup_hook()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

async def main():
    load_dotenv("private.env")

    intents = discord.Intents.default()
    intents.members = True

    openai.api_key = os.getenv("OPENAI_TOKEN")
    bot = Bot(command_prefix="!", intents=intents)
    
    async with bot:
        await bot.start(os.getenv("BOT_TOKEN"))

asyncio.run(main())