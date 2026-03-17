import discord
from discord.ext import commands

from globals import QUIZ, QUIZZERS, LADDERS, MG_PLAYERS, MG_QUEUE
from rated import DEFER, FOLLOWUP, INTERACTION
from quiz import StartQuiz
from ladders import PlayLucidLadders
from views import LucidLadders

class MinigamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="start_game", description="Start game: quiz or lucid ladders")
    @discord.app_commands.choices(mode=[
        discord.app_commands.Choice(name="quiz", value="quiz"),
        discord.app_commands.Choice(name="lucid_ladders", value="lucid_ladders")
    ])
    async def start_game(self, interaction: discord.Interaction, mode: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        await DEFER(interaction)

        if mode == "quiz":
            if not QUIZ["active"] and not QUIZ["second-player"]:
                try:
                    await StartQuiz(interaction.user, interaction.channel, interaction)
                except Exception as exc:
                    await FOLLOWUP(f"Something went wrong with `/start_game quiz`: {exc}", interaction)
                    raise
            else:
                await FOLLOWUP("A quiz is already in progress!", interaction)
            return
        else:
            try:
                await PlayLucidLadders(interaction.user, interaction.channel, interaction)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/start_game lucid_ladders`: {exc}", interaction)
                raise
