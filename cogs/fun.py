import discord

from discord import app_commands
from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mods")
    @app_commands.checks.cooldown(1, 5)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://tenor.com/view/heyzzy-mods-cry-to-mods-annoying-bitch-stfu-gif-25951942")

    @app_commands.command(name="sticker", description="Place a sticker in chat")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(sticker = "Name of the sticker you wish to post")
    async def sticker(self, interaction: discord.Interaction, sticker: str):
        win = False
        id = 0
        for s in interaction.guild.stickers:
            if s.name == sticker:
                win = True
                id = s.id
                break
        if win:
            await interaction.response.send_message(f"https://media.discordapp.net/stickers/{id}.webp")
        else:
            await interaction.response.send_message(f"A sticker of the name {sticker} does not exist!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCog(bot))