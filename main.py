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

class Bot(commands.Bot):
    def __init__(
        self,
        command_prefix = "r!",
        intents: discord.Intents = discord.Intents.default(),
        extensions: Iterable = config["default_cogs"],
        **options
    ):
        self.to_add = extensions
        self.owners = config["owners"]
        self.colours = config["colours"]
        super().__init__(command_prefix, intents=intents, **options)

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