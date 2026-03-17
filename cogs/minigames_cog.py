import discord
from discord import app_commands
from discord.ext import commands

from globals import QUIZ, QUIZZERS, LADDERS, MG_PLAYERS, MG_QUEUE
from rated import DEFER, FOLLOWUP, INTERACTION
from quiz import StartQuiz
from ladders import PlayLucidLadders
from views import LucidLadders

class MinigamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    start_group = app_commands.Group(name="start", description="Commands to start things")
    @start_group.command(name="game", description="Start game: quiz or lucid ladders")
    @discord.app_commands.choices(mode=[
        discord.app_commands.Choice(name="Quiz", value="quiz"),
        discord.app_commands.Choice(name="Lucid Ladders", value="lucid_ladders")
    ])
    async def start_game(self, interaction: discord.Interaction, mode: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        await DEFER(interaction)

        if (QUIZ["active"] or QUIZ["second-player"]) or (LADDERS['status'] != "off"):
            await FOLLOWUP(f"Another game is in progress.", interaction, True)

        if mode == "quiz":
            try:
                await StartQuiz(interaction.user, interaction.channel, interaction)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/start_game quiz`: {exc}", interaction)
                raise
        else:
            try:
                await PlayLucidLadders(interaction.user, interaction.channel, interaction)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/start_game lucid_ladders`: {exc}", interaction)
                raise
