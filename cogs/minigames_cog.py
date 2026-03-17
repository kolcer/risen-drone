import discord
from discord.ext import commands

from globals import BUTTONS, CHANNELS, QUIZ, QUIZZERS, LADDERS, MG_PLAYERS, MG_QUEUE
from rated import DEFER, FOLLOWUP, INTERACTION, SEND_VIEW
from quiz import StartQuiz
from ladders import PlayLucidLadders
from views import Minigames_TicTacToe

class MinigamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="play", description="Start game: quiz or lucid ladders")
    @discord.app_commands.choices(game=[
        discord.app_commands.Choice(name="Quiz", value="quiz"),
        discord.app_commands.Choice(name="Lucid Ladders", value="lucid_ladders"),
        discord.app_commands.Choice(name="Tic Tac Toe", value="ttt")
    ])
    async def start_game(self, interaction: discord.Interaction, game: str, duelist: discord.Member = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return
        
        duelists = [duelist, interaction.user] if duelist else None

        await DEFER(interaction)

        if (QUIZ["active"] or QUIZ["second-player"]) or (LADDERS['status'] != "off"):
            await FOLLOWUP(f"Another game is in progress.", interaction, True)

        if game == "quiz":
            try:
                await StartQuiz(interaction.user, interaction.channel, interaction, duelists)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/play quiz`: {exc}", interaction)
                raise
        elif game == "lucid_ladders":
            try:
                await PlayLucidLadders(interaction.user, interaction.channel, interaction)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/play lucid_ladders`: {exc}", interaction)
                raise
        else:
            if not BUTTONS["status"]:
                try:
                    BUTTONS["status"] = True
                    view = Minigames_TicTacToe(timeout=60)

                    msg = f"Let's play a game."
                    if duelist:
                        view.duelists = duelists
                        msg = f"{duelist.mention}, you have been challenged by {interaction.user.mention}!"

                    view.message = await FOLLOWUP(msg, interaction, False, view)

                    await view.wait()
                    await view.too_late()
                    BUTTONS["status"] = False
                except Exception as exc:
                    await FOLLOWUP(f"Something went wrong with `/play ttt`: {exc}", interaction)
                    raise

