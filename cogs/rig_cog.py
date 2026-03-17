import discord
from discord.ext import commands

from globals import RIG_LIST
from rated import DEFER, FOLLOWUP, INTERACTION
from rigs import CastRig

class RigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Cast Rig Command
    @discord.app_commands.command(name="cast", description="Cast a rig (former 'cast X rig')")
    @discord.app_commands.choices(rig=[discord.app_commands.Choice(name=rig.capitalize(), value=rig) for rig in RIG_LIST])
    async def cast(self, interaction: discord.Interaction, rig: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        rig_lower = rig.strip().lower()
        await DEFER(interaction)

        try:
            await CastRig(rig_lower, interaction.channel, interaction.user, interaction=interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/cast {rig_lower}`: {exc}", interaction)
            raise


async def setup(bot: commands.Bot):
    await bot.add_cog(RigCog(bot))
