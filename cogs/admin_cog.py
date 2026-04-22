import asyncio

from database import add_entry, check_key, get_value, list_decoded_entries
import discord
from discord import app_commands
from discord.ext import commands
from utility import command_check
from globals import CHANNELS, I_SPY, WISDOM
from rated import DEFER, FOLLOWUP, INTERACTION, SEND

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    channel_choices = [
        discord.app_commands.Choice(name=ch.title(), value=ch) 
        for ch in sorted(CHANNELS.keys())
    ]

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

    @discord.app_commands.command(name="wisdoms", description="Show the number of wisdoms")
    async def wisdoms(self, interaction: discord.Interaction):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            await FOLLOWUP(f"I have {len(WISDOM)} wisdoms.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/wisdoms`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="nr", description="Add a new secret role.")
    async def nr(self, interaction: discord.Interaction, name: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            add_entry(name, "dummy")
            await FOLLOWUP("Role created successfully.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/nr`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="check_key", description="Check if a key exists in the database.")
    async def check_key(self, interaction: discord.Interaction, key: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            responses = []

            if check_key(key):
                value = list_decoded_entries(key)

                if not value:
                    value = get_value(key)
                
                responses.append(f"Key `{key}` found! Value: {value}")

            if responses:
                await FOLLOWUP("\n".join(responses), interaction)
            else:
                await FOLLOWUP(f"No key found for '{key}'.", interaction)
                
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/check_key`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="ispy", description="Begin a game of ispy.")
    @discord.app_commands.choices(channel=channel_choices)
    async def ispy(self, interaction: discord.Interaction, channel: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            await FOLLOWUP(f"Starting ispy game in {channel}...", interaction)

            I_SPY['channel'] = CHANNELS[channel]
            I_SPY['status'] = 0

            await SEND(I_SPY['channel'], I_SPY['questions'][0])

            await asyncio.sleep(I_SPY['maxwait'])

            if I_SPY['status'] == 0:
                I_SPY['status'] = None
                await SEND(I_SPY['channel'],'Whatever.')
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/ispy`: {exc}", interaction)
            raise