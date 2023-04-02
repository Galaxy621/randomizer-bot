import discord

from discord import app_commands
from discord.ext import commands

class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Get information on a user")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(user = "The user you wish to get information on")
    async def whois(self, interaction: discord.Interaction, user: discord.Member = None):
        if not user:
            user = interaction.user

        embed = discord.Embed(
            title = user.name,
            description = f"ID: {user.id}",
            colour = user.colour.value # if user.accent_colour else discord.Colour.blurple()
        )

        embed.set_thumbnail(url = user.avatar.url)

        embed.add_field(name = "Joined", value = user.joined_at.strftime("%d/%m/%Y %H:%M:%S"))
        embed.add_field(name = "Created", value = user.created_at.strftime("%d/%m/%Y %H:%M:%S"))

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CoreCog(bot))