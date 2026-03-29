import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import datetime
from roles import DemorphFrom, MorphTo, MorphTo, SubTo, UnsubFrom
from utility import send_followup, command_check
from globals import EVENTS, EXTRA_ROLES, PING_ROLES, RIG_LIST, SECRET_PING_ROLES, MORPHABLE_ROLES, SPECIAL_ROLES, EX_CLIMBERS, MAX_EGGS, BOT_BLACKLIST
from rated import DEFER, FOLLOWUP, INTERACTION, SEND, REMOVE_ROLES, ADD_ROLES
from database import list_decoded_entries, add_entry_with_check

class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    _raw_roles = list(PING_ROLES.keys()) + SECRET_PING_ROLES
    _sorted_roles = sorted(_raw_roles)
    role_choices = [app_commands.Choice(name="All Roles", value="all")] + [
        discord.app_commands.Choice(name=role, value=role) 
        for role in _sorted_roles
    ]

    # !!! max 25 choices allowed and sorted_alignments rn is exactly 25.
    sorted_alignments = [app_commands.Choice(name="All Alignments", value="all")] + [
        discord.app_commands.Choice(name=ali.capitalize(), value=ali.lower()) 
        for ali in sorted(MORPHABLE_ROLES.keys()) + sorted(SPECIAL_ROLES.keys())
    ]

    @discord.app_commands.command(name="sub", description="Subscribe to a role")
    @discord.app_commands.choices(role=role_choices)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def sub(self, interaction: discord.Interaction, role: str):
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
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
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
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

    @discord.app_commands.command(name="morph", description="Morph into an Alignment")
    @discord.app_commands.choices(role=sorted_alignments)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def morph(self, interaction: discord.Interaction, role: str):
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)
        user = interaction.user
        today = datetime.date.today()
        
        morph_target = "Joker" if (today.day == 1 and today.month == 4) else role.title()
        alignment_roles_count = len([r for r in user.roles if r.name.title() in MAX_EGGS])

        if EVENTS.get("Easter", False):
            if morph_target != "Janitor" and (alignment_roles_count >= 1 or role == "all"):
                msg = ("I'm afraid I can't let you do that.\n"
                    "For the duration of the Easter Event, you may only have 1 alignment role.\n"
                    "Eating eggs of any alignment will morph you instead.")
                await FOLLOWUP(msg, interaction, True)
                return

        try:
            if EXTRA_ROLES['hypno'] in interaction.user.roles:
                await FOLLOWUP(await DemorphFrom(user, morph_target), interaction, True)
            else:
                await FOLLOWUP(await MorphTo(user, morph_target), interaction, True)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/morph {role}`: {exc}", interaction)
            raise

        reaver_role = MORPHABLE_ROLES.get("Reaver", [None])[0]

        if alignment_roles_count == (len(RIG_LIST) - 2) and reaver_role not in user.roles:
            await SEND(interaction.channel, "What did poor Reaver do to you? They are not an illusion.")
            
            if str(user.id) not in list_decoded_entries("Alien"):
                await add_entry_with_check("Alien", user)

    @discord.app_commands.command(name="demorph", description="Demorph from an Alignment")
    @discord.app_commands.choices(role=sorted_alignments)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def demorph(self, interaction: discord.Interaction, role: str):
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)
        user = interaction.user
        today = datetime.date.today()

        if today.day == 1 and today.month == 4:
            await FOLLOWUP("Unfortunately, this command is out of service.", interaction, True)
            return

        demorph_target = role.title()

        if EVENTS.get("Easter", False) and demorph_target != "Janitor":
            alignment_roles_count = len([r for r in user.roles if r.name.title() in MAX_EGGS])
            
            if alignment_roles_count == 1:
                msg = ("I'm afraid you're stuck with that alignment for now.\n"
                       "During the Easter Event, you can side with any alignment but there are no take-backsies... unless you eat an egg.")
                await FOLLOWUP(msg, interaction, True)
                return

        if EXTRA_ROLES['hypno'] in interaction.user.roles:
            await FOLLOWUP(await MorphTo(user, demorph_target), interaction)
        else:
            await FOLLOWUP(await DemorphFrom(user, demorph_target), interaction)

        climber_role_obj = SPECIAL_ROLES.get("Climber", [None])[0]
        
        if demorph_target == "Climber" and climber_role_obj in user.roles:
            EX_CLIMBERS.append(user)
            await REMOVE_ROLES(user, climber_role_obj)
            
            await asyncio.sleep(10)
            await ADD_ROLES(user, climber_role_obj)
            
            if user in EX_CLIMBERS:
                EX_CLIMBERS.remove(user)
                
            await asyncio.sleep(1)
            await SEND(interaction.channel, "Just kidding.")

    @sub.error
    @morph.error
    @unsub.error
    @demorph.error
    async def role_error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            seconds = round(error.retry_after, 1)
            await INTERACTION(interaction.response, f"Chill. You can use this command again in **{seconds}s**.", True)
        else:
            raise error