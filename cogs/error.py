import discord

from discord import app_commands
from discord.ext import commands

class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        self.bot.tree.on_error = self._old_tree_error
        self._old_tree_error = None

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        return await interaction.response.send_message(f"Error: {error}")

async def setup(bot):
    await bot.add_cog(ErrorCog(bot))