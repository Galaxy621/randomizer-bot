import discord
import openai

from discord import app_commands
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = [
            app_commands.ContextMenu(
                name = "Check Filter",
                callback=self.checkfilter
            )
        ]

        self.nickname = "Moderation"
        self.description = "Moderation commands"

        for command in self.ctx_menu: self.bot.tree.add_command(command)

    async def cog_unload(self) -> None:
        for command in self.ctx_menu: self.bot.tree.remove_command(command.name, command.type)
        return await super().cog_unload()


    # @app_commands.command(name="checkfilter", description="See if OpenAI considers your message against their usage policies")
    # @app_commands.describe(message = "The message you wish to check")

    @app_commands.checks.cooldown(1, 5)
    async def checkfilter(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(thinking = True)
        
        response = openai.Moderation.create(input = message.content)
        embeds = []

        for result in response["results"]:
            embed = discord.Embed(
                title = "OpenAI Moderation",
                description = f"Message:\n```\n{message.content}```",
                color = 0xFF0000 if result["flagged"] else 0x00FF00
            )

            if result["flagged"]:
                reasons = []
                for category, isTrue in result["categories"].items():
                    if isTrue: reasons.append(category)

                embed.add_field(name = "Reasons", value = ", ".join(reasons), inline = False)
            else:
                embed.add_field(name = "Reasons", value = "None", inline = False)

            embeds.append(embed)

        await interaction.followup.send(embeds = embeds)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))