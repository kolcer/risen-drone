import discord
from discord.ext import commands

from globals import RIG_LIST
from rigs import CastRig

class RigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="cast", description="Cast a rig (former 'cast X rig')")
    @discord.app_commands.choices(rig=[discord.app_commands.Choice(name=rig, value=rig) for rig in RIG_LIST])
    async def cast(self, interaction: discord.Interaction, rig: str):
        if interaction.guild is None or interaction.channel is None:
            await interaction.response.send_message(
                "Use this command in the Crazy Stairs server!", 
                ephemeral=True
            )
            return

        rig_lower = rig.strip().lower()
        await interaction.response.defer(ephemeral=True)

        try:
            await CastRig(rig_lower, interaction.channel, interaction.user, interaction=interaction)
        except Exception as exc:
            await interaction.followup.send(
                f"Something went wrong when casting `{rig_lower}` rig: {exc}",
                ephemeral=False
            )
            raise


async def setup(bot: commands.Bot):
    await bot.add_cog(RigCog(bot))
