from re import sub

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

    _raw_roles = list(PING_ROLES.keys()) + SECRET_PING_ROLES
    _sorted_roles = sorted(_raw_roles)
    role_choices = [app_commands.Choice(name="All Roles", value="all")] + [
        app_commands.Choice(name=role, value=role) 
        for role in _sorted_roles
    ]

    @discord.app_commands.command(name="sub", description="Subscribe to a role")
    @discord.app_commands.choices(role=role_choices)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
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
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
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

    @sub.error
    @unsub.error
    async def role_error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            seconds = round(error.retry_after, 1)
            await INTERACTION(interaction.response, f"Chill. You can use this command again in **{seconds}s**.", True)
        else:
            raise error