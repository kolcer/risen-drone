import discord
from discord.ext import commands

from globals import QUIZ, QUIZZERS
from rated import DEFER, FOLLOWUP, INTERACTION
from quiz import StartQuiz, JoinQuiz

class MinigamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="quiz_start", description="Start a Crazy Stairs knowledge quiz (former 'start quiz')")
    async def start_quiz(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return
        
        await DEFER(interaction)
        if not QUIZ["active"] and not QUIZ["second-player"]:
            try:
                await StartQuiz(interaction.user, interaction.channel, interaction)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/start_quiz`: {exc}", interaction)
                raise
        else:
            await FOLLOWUP("A quiz is already in progress! Type 'join quiz' to participate.", interaction)

    @discord.app_commands.command(name="quiz_join", description="Join an in-progress Crazy Stairs knowledge quiz (former 'join quiz')")
    async def join_quiz(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        await DEFER(interaction)
        if QUIZ["second-player"] and interaction.user not in QUIZZERS:
            try:
                await JoinQuiz(interaction.user, interaction.channel)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/join_quiz`: {exc}", interaction)
                raise
        else:
            await FOLLOWUP("No quiz is currently looking for participants, or you have already joined!", interaction)