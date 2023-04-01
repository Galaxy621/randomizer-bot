import discord
import openai
import random

from discord import app_commands
from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colours = {}

        with open("assets/rgb.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            try:
                colour = line.strip().split("\t")
                self.colours[colour[0].lower()] = colour[1]
            except:
                pass

        self.names = {v: k for k, v in self.colours.items()}

    @app_commands.command(name="mods", description="Umm... mods?")
    @app_commands.checks.cooldown(1, 5)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://tenor.com/view/heyzzy-mods-cry-to-mods-annoying-bitch-stfu-gif-25951942")

        # print(response)

    @app_commands.command(name="colour", description="Get information on a colour")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(name = "Name of a colour")
    @app_commands.describe(colour = "The hex value of the colour")
    async def colour(self, interaction: discord.Interaction, name: str = None, colour: str = None):
        await interaction.response.defer(thinking=True)
        got_random = False

        # Get a colour using a name
        # If this doesn't work, the command will throw an error
        if name and not colour:
            colour = self.colours.get(name.lower())

        # Get a name using colour
        # The command should respond even if the name doesn't exist
        elif colour and not name:
            colour = "#" + colour[-6:].lower()
            name = self.names.get(colour)

        # The user has either provided nothing, or both a name and colour
        # Create a random colour name pair
        else:
            name, colour = name, colour = random.choice(list(self.colours.items()))
            got_random = True

        if not colour:
            raise app_commands.AppCommandError(f"Invalid colour name: `{name}`")

        try:
            hex_value =int(colour[1:], base = 16)
        except:
            raise app_commands.AppCommandError(f"Invalid hex value: `{colour}`")

        title = f"{'Random ' if got_random else ''}Colour"
        description = f"{f'{name.title()} | ' if name else ''}{colour.upper()}"
        url = f"https://singlecolorimage.com/get/{colour[1:]}/256x256"

        embed = discord.Embed(
            title = title,
            description = description,
            colour = hex_value
        )

        embed.set_image(url = url)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="sticker", description="Place a sticker in chat")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(sticker = "Name of the sticker you wish to post")
    async def sticker(self, interaction: discord.Interaction, sticker: str):
        id = 0

        for s in interaction.guild.stickers:
            if s.name == sticker:
                id = s.id
                break

        if id != 0:
            await interaction.response.send_message(f"https://media.discordapp.net/stickers/{id}.webp")
        else:
            await interaction.response.send_message(f"A sticker of the name {sticker} does not exist!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCog(bot))