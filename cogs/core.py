import discord

from discord import app_commands
from discord.ext import commands

class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.nickname = "Core"
        self.description = "Basic utility commands"

    @app_commands.command(name="whois", description="Get information on a user")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(user = "The user you wish to get information on")
    async def whois(self, interaction: discord.Interaction, user: discord.Member = None):
        if not user:
            user = interaction.user

        embed = discord.Embed(
            title = user.name,
            description = f"{user.mention}",
            colour = user.colour.value # if user.accent_colour else discord.Colour.blurple()
        )

        embed.add_field(name = "Created", value = user.created_at.strftime("%d/%m/%Y %H:%M:%S"))
        embed.set_thumbnail(url = user.avatar.url)

        if interaction.guild:
            embed.add_field(name = "Joined", value = user.joined_at.strftime("%d/%m/%Y %H:%M:%S"))
            embed.add_field(name = "Nickname", value = user.nick if user.nick else "None")
            # I would like to apologise, Copilot made this.
            roles = [role.mention for role in user.roles if role.name != "@everyone"]
            roles.reverse()

            embed.add_field(name = "Roles", value = " ".join(roles) if len(user.roles) > 1 else "None", inline = False)
            embed.add_field(name = "Permissions", value = ", ".join([perm.replace("_", " ").title() for perm, value in user.guild_permissions if value]) if len([perm for perm, value in user.guild_permissions if value]) > 0 else "None", inline = False)

        time_of_sent = interaction.created_at
        embed.set_footer(text = f"ID: {user.id}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roleinfo", description="Get the info about a role")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(role = "The role you wish to get the info of")
    async def roleinfo(self, interaction: discord.Interaction, role: str):
        await interaction.response.defer(thinking=True)

        role_by_id = None

        try:
            role_by_id = interaction.guild.get_role(int(role))
        except:
            pass

        if not role_by_id:        
            role = discord.utils.get(interaction.guild.roles, name=role)
        else:
            role = role_by_id
        

        if not role:
            raise app_commands.AppCommandError("Role not found")

        embed = discord.Embed(
            title = role.name,
            # description = f"ID: {role.id}",
            colour = role.colour.value,
        )

        embed.add_field(
            name = "ID",
            value = role.id,
        )

        embed.add_field(
            name = "Colour",
            # value = role.colour.value,
            value = f"#{role.colour.value:0>6x}".upper(),
        )

        embed.add_field(
            name = "Mentionable",
            value = role.mentionable,
        )

        embed.add_field(
            name = "Member Count",
            value = len(role.members),
        )

        if role.icon:
            embed.set_thumbnail(url = role.icon.url)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="listrolemembers", description="List the members of a role")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(role = "The role you wish to get the members from")
    async def listrolemembers(self, interaction: discord.Interaction, role: str):
        await interaction.response.defer(thinking=True)

        role_by_id = None

        try:
            role_by_id = interaction.guild.get_role(int(role))
        except:
            pass

        if not role_by_id:        
            role = discord.utils.get(interaction.guild.roles, name=role)
        else:
            role = role_by_id
        

        if not role:
            raise app_commands.AppCommandError("Role not found")

        embed = discord.Embed(
            title = role.name,
            # description = f"ID: {role.id}",
            colour = role.colour.value,
        )

        embed.add_field(
            name = "Members",
            value = "\n".join([f"{member.mention} ({member.id})" for member in role.members]),
        )

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CoreCog(bot))