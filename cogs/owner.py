import contextlib
import discord
import io
import os
import subprocess

from discord import app_commands
from discord.ext import commands

def owner_only():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id in interaction.client.owners
    return app_commands.check(predicate)

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name = "Interpret as Python",
            callback=self.read_program
        )
        self.bot.tree.add_command(self.ctx_menu)

        self.nickname = "Owner"
        self.description = "Owner commands"
        self.hidden = True

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, self.ctx_menu.type)
        return await super().cog_unload()

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
    @app_commands.describe(code = "The code to evaluate.")
    @owner_only()
    async def eval_command(self, interaction: discord.Interaction, code: str):
        embed = discord.Embed(title="Eval", description=f"```py\n{code}\n```")
        
        result = ""
        output = ""

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = eval(code)
                output = stdout.getvalue()

        except Exception as e:
            embed.add_field(name="Error", value=f"```py\n{e}\n```")
            
        finally:
            if output:
                embed.add_field(name="Output", value=f"```py\n{output}\n```")
            if result:
                embed.add_field(name="Result", value=f"```py\n{result}\n```")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="exec", description="Executes code.")
    @app_commands.describe(code = "The code to execute.")
    @owner_only()
    async def exec_command(self, interaction: discord.Interaction, code: str):
        embed = discord.Embed(title="Exec", description=f"```py\n{code}\n```")
        
        result = ""
        output = ""

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = exec(code)
                output = stdout.getvalue()

        except Exception as e:
            embed.add_field(name="Error", value=f"```py\n{e}\n```")
            
        finally:
            if output:
                embed.add_field(name="Output", value=f"```py\n{output}\n```")
            if result:
                embed.add_field(name="Result", value=f"```py\n{result}\n```")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shell", description="Executes a through the shell.")
    @app_commands.describe(code = "The code to execute.")
    @owner_only()
    async def shell(self, interaction: discord.Interaction, code: str):
        embed = discord.Embed(title="Shell", description=f"```sh\n{code}\n```")
        
        result = ""
        output = ""

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = subprocess.check_output(code, shell=True).decode()
                output = stdout.getvalue()

        except Exception as e:
            embed.add_field(name="Error", value=f"```py\n{e}\n```")
            
        finally:
            if output:
                embed.add_field(name="Output", value=f"```\n{output}\n```")
            if result:
                embed.add_field(name="Result", value=f"```\n{result}\n```")

        await interaction.response.send_message(embed=embed)
    

    @staticmethod
    def get_code_block(content: str) -> str:
        # find the first instance of '```' and the next instance of '```'

        first = content.find("```")
        if first == -1:
            # No code block, interpret message as code
            return content
        first += 3

        second = content.find("```", first)
        if content[first:second].startswith("py"):
            # Remove 'py' from the start of the code block, if it exists
            first += 3
        
        return content[first:second]


    @owner_only()
    async def read_program(self, interaction: discord.Interaction, message: discord.Message):
        code = self.get_code_block(message.content)
        embed = discord.Embed(title="Read Program", description=f"```py\n{code}\n```")
        
        result = ""
        output = ""

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = exec(code)
                output = stdout.getvalue()

        except Exception as e:
            embed.add_field(name="Error", value=f"```py\n{e}\n```")
            
        finally:
            if output:
                embed.add_field(name="Output", value=f"```py\n{output}\n```")
            if result:
                embed.add_field(name="Result", value=f"```py\n{result}\n```")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="createthread", description="Creates a thread.")
    @app_commands.describe(name = "The name of the thread.", message = "The message to start the thread with.")
    @owner_only()
    async def create_thread(self, interaction: discord.Interaction, name: str, message: str):
        await interaction.response.defer()
        thread = await interaction.channel.create_thread(
            name = name,
            type = discord.ChannelType.public_thread
        )
        await thread.send(message)
        await interaction.followup.send("Created thread.")

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

    @app_commands.command(name="additem", description="Adds an item to the info command.")
    @app_commands.describe(name = "The name of the item.", description = "The description of the item.")
    @owner_only()
    async def add_item(self, interaction: discord.Interaction, name: str, description: str):
        await interaction.response.defer()
        
        for item in self.bot.items:
            if item["Name"].lower() == name.lower():
                await interaction.followup.send("Item already exists.")
                return

        self.bot.items.append({
            "Name": name,
            "Description": description
        })
        await interaction.followup.send("Added item.")

    @app_commands.command(name="removeitem", description="Removes an item from the info command.")
    @app_commands.describe(name = "The name of the item.")
    @owner_only()
    async def remove_item(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        for item in self.bot.items:
            if item["Name"].lower() == name.lower():
                self.bot.items.remove(item)
                await interaction.followup.send("Removed item.")
                return

        await interaction.followup.send("Item not found.")

    @app_commands.command(name="saveitems", description="Saves the items to the file.")
    @app_commands.describe(backup = "Whether to backup the file outside of the working directory before saving.")
    @owner_only()
    async def save_items(self, interaction: discord.Interaction, backup: bool = True):
        await interaction.response.defer()
        self.bot.save_items()
        if backup:
            self.bot.backup_items("..")
        await interaction.followup.send("Saved items.")

    @app_commands.command(name="syncitems", description="Syncs the items from the file.")
    @owner_only()
    async def sync_items(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.bot.sync_items()
        await interaction.followup.send("Synced items.")

    # load latest backup
    @app_commands.command(name="loadbackup", description="Loads the latest backup.")
    @owner_only()
    async def load_backup(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.bot.load_latest_backup("..")
        await interaction.followup.send("Loaded backup.")

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))