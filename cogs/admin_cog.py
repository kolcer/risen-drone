import asyncio
import time

from database import add_egg_with_check, add_entry, check_key, delete_entry, delete_key, get_value, list_decoded_entries
import discord
from discord import app_commands
from discord.ext import commands
from utility import command_check
from globals import BOT_BLACKLIST, CHANNELS, I_SPY, WISDOM, FUN_ROLES
from rated import DEFER, DELETE, EDIT_MESSAGE, FOLLOWUP, INTERACTION, SEND, SEND_VIEW
from views import ButtonEgg_Throw

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

    @discord.app_commands.command(name="delete_key", description="Delete a key from the database.")
    async def delete_key(self, interaction: discord.Interaction, key: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            delete_key(key)
            await FOLLOWUP(f"Key '{key}' deleted successfully.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/delete_key`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="assign", description="Assign a role to a user.")
    async def assign(self, interaction: discord.Interaction, user: discord.Member, role: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            if not any(role in category_data for category_data in FUN_ROLES.values()):
                await FOLLOWUP("You cannot assign this role through my commands.", interaction)
                return

            if user.id in list_decoded_entries(role):
                await asyncio.sleep(1)
                await FOLLOWUP("They already own this role, duh.", interaction)
                return

            if role in (FUN_ROLES["Easter"] + FUN_ROLES["Easter26"] + FUN_ROLES["Easter27"]):
                await add_egg_with_check(role, user)
            else:
                add_entry(role, user.id)

            await asyncio.sleep(1)
            await FOLLOWUP(f"I gave the role to {user.mention}.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/assign`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="unassign", description="Remove a role from a user.")
    async def unassign(self, interaction: discord.Interaction, user: discord.Member, role: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            if not any(role in category_data for category_data in FUN_ROLES.values()):
                await FOLLOWUP("You cannot unassign this role through my commands.", interaction)
                return

            entries = list_decoded_entries(role)

            if not user.id in entries:
                await asyncio.sleep(1)
                await FOLLOWUP("They do not own the role. Are you ok?", interaction)
                return

            index = entries.index(user.id)
            delete_entry(role, index)

            await asyncio.sleep(1)
            await FOLLOWUP(f"Took the role away from {user.mention}.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/unassign`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="enlist", description="Add an user to the blacklist, or remove them if they are already blacklisted.")
    @discord.app_commands.choices(list=[
        discord.app_commands.Choice(name='Blacklist', value='blacklist'),
        discord.app_commands.Choice(name='Whitelist', value='whitelist')
    ])
    async def enlist(self, interaction: discord.Interaction, list: str, target: discord.Member):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            finalMsg = ""
            if list == 'blacklist':
                if str(target.id) not in BOT_BLACKLIST:
                    BOT_BLACKLIST.append(str(target.id))
                    finalMsg = f"{target.mention} has been blacklisted."
                else:
                    finalMsg = f"{target.mention} is already blacklisted."
            elif list == 'whitelist':
                if str(target.id) in BOT_BLACKLIST:
                    BOT_BLACKLIST.remove(str(target.id))
                    finalMsg = f"{target.mention} has been whitelisted."
                else:
                    finalMsg = f"{target.mention} is not in the blacklist."

            await FOLLOWUP(finalMsg, interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/delete_key`: {exc}", interaction)
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

    @discord.app_commands.command(name="architect", description="Drop Architect Egg.")
    @discord.app_commands.choices(channel=channel_choices)
    async def architect(self, interaction: discord.Interaction, channel: str, countdown: int):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            await FOLLOWUP(f"Launching Architect Egg in {channel}...", interaction)
            await asyncio.sleep(1)

            arcMsg = await SEND(CHANNELS[channel], f"The Architect Egg is falling at terminal velocity in this channel! Take cover <t:{round(time.time() + countdown)}:R>.")
            await asyncio.sleep(countdown)

            view = ButtonEgg_Throw(timeout=30)
            view.thrower = None
            view.disabled = False

            view.type = "Architect"

            view.channel = CHANNELS[channel]
            view.toolate = True
            view.message = await SEND_VIEW(CHANNELS[channel], "The Architect Egg fell from the sky!", view)
            await asyncio.sleep(1)
            await EDIT_MESSAGE(arcMsg, "The Architect Egg landed gracefully.")

            await view.wait()
            await view.too_late()
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/architect`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="makesay", description="Have the drone speak your words.")
    @discord.app_commands.choices(channel=channel_choices)
    async def makesay(self, interaction: discord.Interaction, channel: str, txt: str):
        stopMsg = command_check(interaction, True)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        await DEFER(interaction)

        try:
            await FOLLOWUP(f"I'm clearing my voice...", interaction)
            await asyncio.sleep(1)
            await SEND(CHANNELS[channel], txt)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/makesay`: {exc}", interaction)
            raise