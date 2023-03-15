import contextlib
import discord
import io
import os

from discord import app_commands
from discord.ext import commands

def owner_only():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id in interaction.client.owners
    return app_commands.check(predicate)

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="load", description="Loads a cog.")
    @app_commands.describe(cog = "The cog to load.")
    @owner_only()
    async def load(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
        else:
            await interaction.response.send_message(f"Loaded {cog}.")

    @app_commands.command(name="unload", description="Unloads a cog.")
    @app_commands.describe(cog = "The cog to unload.")
    @owner_only()
    async def unload(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
        else:
            await interaction.response.send_message(f"Unloaded {cog}.")

    @app_commands.command(name="reload", description="Reloads a cog.")
    @app_commands.describe(cog = "The cog to reload.")
    @owner_only()
    async def reload(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
        else:
            await interaction.response.send_message(f"Reloaded {cog}.")

    @app_commands.command(name="eval", description="Evaluates code.")
    @owner_only()
    async def eval_command(self, interaction: discord.Interaction, code: str):
        embed = discord.Embed(title="Eval", description=f"```py\n{code}\n```")
        
        result = ""
        stdout = ""

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = eval(code)
                stdout = stdout.getvalue()

        except Exception as e:
            embed.add_field(name="Error", value=f"```py\n{e}\n```")
            
        finally:
            if stdout:
                embed.add_field(name="Output", value=f"```py\n{stdout}\n```")
            if result:
                embed.add_field(name="Result", value=f"```py\n{result}\n```")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="exec", description="Executes code.")
    @owner_only()
    async def exec_command(self, interaction: discord.Interaction, code: str):
        embed = discord.Embed(title="Exec", description=f"```py\n{code}\n```")
        
        result = ""
        stdout = ""

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = exec(code)
                stdout = stdout.getvalue()

        except Exception as e:
            embed.add_field(name="Error", value=f"```py\n{e}\n```")
            
        finally:
            if stdout:
                embed.add_field(name="Output", value=f"```py\n{stdout}\n```")
            if result:
                embed.add_field(name="Result", value=f"```py\n{result}\n```")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shutdown", description="Shuts down the bot.")
    @owner_only()
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.send_message("Shutting down...")
        await self.bot.close()

    @app_commands.command(name="sync", description="Syncs the bot.")
    @owner_only()
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.bot.tree.sync()
        await interaction.followup.send("Synced.")


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))