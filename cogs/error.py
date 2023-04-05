import discord

from discord import app_commands
from discord.ext import commands

class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.nickname = "Error"
        self.hidden = True
        self.description = "Error handling"

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        self.bot.tree.on_error = self._old_tree_error
        self._old_tree_error = None

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        isdone = interaction.response.is_done()
        callback = interaction.response.send_message if not isdone else interaction.followup.send
        
        embed = discord.Embed(
            title = "Error",
            description = f":no_entry_sign: {error}",
            colour = int(self.bot.colours["negative"], base=16)
        )

        return await callback(embed=embed)

async def setup(bot):
    await bot.add_cog(ErrorCog(bot))