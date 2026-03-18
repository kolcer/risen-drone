import discord
from discord import app_commands
from roles import SubTo, UnsubFrom
from discord.ext import commands

from utility import send_followup
from globals import HYPNO_SWAPS, EXTRA_ROLES, PING_ROLES, SECRET_PING_ROLES
from rated import DEFER, FOLLOWUP, INTERACTION

class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    role_choices = [
        app_commands.Choice(name=role, value=role) 
        for role in list(PING_ROLES.keys()) + SECRET_PING_ROLES
    ]

    @discord.app_commands.command(name="sub", description="Subscribe to a role")
    @discord.app_commands.choices(role=role_choices)
    async def sub(self, interaction: discord.Interaction, role: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        role_name = role.title()
        await DEFER(interaction)

        try:
            if EXTRA_ROLES['hypno'] in interaction.user.roles:
                await send_followup(interaction.channel, await UnsubFrom(interaction.user, role_name), interaction)
            else:
                await send_followup(interaction.channel, await SubTo(interaction.user, role_name), interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/sub {role}`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="unsub", description="Unsubscribe from a role")
    @discord.app_commands.choices(role=role_choices)
    async def unsub(self, interaction: discord.Interaction, role: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        role_name = role.title()
        await DEFER(interaction)

        try:
            if EXTRA_ROLES['hypno'] in interaction.user.roles:
                await send_followup(interaction.channel, await SubTo(interaction.user, role_name), interaction)
            else:
                await send_followup(interaction.channel, await UnsubFrom(interaction.user, role_name), interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/unsub {role}`: {exc}", interaction)
            raise