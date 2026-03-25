import discord
from discord.ext import commands

from globals import HYPNO_SWAPS, RIG_LIST, EXTRA_ROLES
from rated import DEFER, FOLLOWUP, INTERACTION
from rigs import CastRig
from utility import command_check

class RigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    sorted_choices = [
        discord.app_commands.Choice(name=rig.capitalize(), value=rig) 
        for rig in sorted(RIG_LIST)
    ]

    # Cast Rig Command
    @discord.app_commands.command(name="cast", description="Cast a rig (former 'cast X rig')")
    @discord.app_commands.choices(rig=sorted_choices)
    async def cast(self, interaction: discord.Interaction, rig: str):
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return
        
        usr = interaction.user
        rigLower = rig.strip().lower()
        newRig = rigLower

        if EXTRA_ROLES['hypno'] in usr.roles:
            newRig = HYPNO_SWAPS.get(rigLower, rigLower)

        await DEFER(interaction)

        try:
            await CastRig(newRig, interaction.channel, usr, interaction=interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/cast {newRig}`: {exc}", interaction)
            raise
