import discord
from discord.ext import commands

from rigs import CastRig

class RigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="cast", description="Cast a rig (former 'cast X rig')")
    async def cast(self, interaction: discord.Interaction, rig: str):
        if interaction.guild is None or interaction.channel is None:
            await interaction.response.send_message("This command must be used in a guild channel.", ephemeral=True)
            return

        rig_lower = rig.strip().lower()
        await interaction.response.defer(ephemeral=True)
        await CastRig(rig_lower, interaction.channel, interaction.user)


async def setup(bot: commands.Bot):
    await bot.add_cog(RigCog(bot))
