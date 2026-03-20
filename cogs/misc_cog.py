import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from globals import FIX_BOT, EXTRA_ROLES, ACTIVE_RIGS, DETAILED_RIGS, RIG_COOLDOWNS, BUTTONS
from rated import DEFER, FOLLOWUP, INTERACTION, SEND
from quiz import FORCE_CLOSE_EVENT
from ladders import MG_RESET

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="reset", description="Reset Broken Drone")
    async def sub(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel

        if usr in FIX_BOT:
            await FOLLOWUP("Not again.", interaction, True)
            return
        
        await DEFER(interaction)

        try:
            FIX_BOT.append(usr)
            if len(FIX_BOT) == 1 and not EXTRA_ROLES['admin'] in usr.roles:
                await FOLLOWUP("One User wants me to reset. 2 more people are required for it to take effect.", interaction, False)
                # await SEND(ch, "One User wants me to reset. 2 more people are required for it to take effect.")
            elif len(FIX_BOT) == 2 and not EXTRA_ROLES['admin'] in usr.roles:
                # await SEND(ch, "Two Users want me to reset. 1 more person is required for it to take effect.")
                await FOLLOWUP("Two Users want me to reset. 1 more person is required for it to take effect.", interaction, False)
            else:
                # await SEND(ch, "All Games and Rigs (along with their Cooldowns) have been reset.")
                await FOLLOWUP("All Games and Rigs (along with their Cooldowns) have been reset.", interaction, False)
                FIX_BOT.clear()
                FORCE_CLOSE_EVENT()
                MG_RESET()

                for rig in ACTIVE_RIGS:
                    ACTIVE_RIGS[rig] = False 

                for rig in DETAILED_RIGS:
                    DETAILED_RIGS[rig][0] = None
                    DETAILED_RIGS[rig][1] = None

                for cooldown in RIG_COOLDOWNS:
                    RIG_COOLDOWNS[cooldown] = False

                BUTTONS["status"] = False
                BUTTONS["easterStatus"] = False
                BUTTONS["easterStaffStatus"] = False

            await asyncio.sleep(60)
            if len(FIX_BOT) != 0:
                await SEND(ch, "Games have not been reset due to lack of users asking to.")
                FIX_BOT.clear()
            return
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/reset`: {exc}", interaction)
            raise
