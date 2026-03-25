import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from utility import command_check
from globals import CHANNELS, BOT_BLACKLIST
from rated import DEFER, FOLLOWUP, INTERACTION

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="invite", description="Give access to Drone Masters chat")
    async def invite(self, interaction: discord.Interaction, target: discord.Member):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            await CHANNELS["drone-masters"].set_permissions(target, view_channel=True, send_messages=True)
            await asyncio.sleep(1)
            await FOLLOWUP(f"Permissions granted. {target.mention} has been ushered into the Drone Master chambers.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/invite`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="bid_farewell", description="Remove access from Drone Masters chat")
    async def bid_farewell(self, interaction: discord.Interaction, target: discord.Member):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            await CHANNELS["drone-masters"].set_permissions(target, view_channel=False, send_messages=False)
            await FOLLOWUP(f"Farewell, {target.display_name}. Their access to the Drone Master channel has been dissolved.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/bid_farewell`: {exc}", interaction)
            raise