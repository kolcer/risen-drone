import asyncio
import random
import re
import discord
from discord.ext import commands

from globals import BUTTONS, HYPNO_SWAPS, QUIZ, LADDERS, EXTRA_ROLES
from rated import DEFER, FOLLOWUP, INTERACTION, SEND_VIEW
from quiz import StartQuiz
from ladders import PlayLucidLadders
from views import Minigames_Hangman, Minigames_TicTacToe

class MinigamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="play", description="Start game: Quiz, Lucid Ladders, or Tic Tac Toe")
    @discord.app_commands.choices(game=[
        discord.app_commands.Choice(name="Quiz", value="quiz"),
        discord.app_commands.Choice(name="Lucid Ladders", value="lucid_ladders"),
        discord.app_commands.Choice(name="Tic Tac Toe", value="ttt")
    ])
    @discord.app_commands.describe(
        game="How can I entertain you?",
        duelist="Optional: Challenge a friend to play with you."
    )
    async def start_game(self, interaction: discord.Interaction, game: str, duelist: discord.Member = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return
        
        newGame = game

        if EXTRA_ROLES['hypno'] in interaction.user.roles:
            newGame = HYPNO_SWAPS.get(game, game)
        
        duelists = [duelist, interaction.user] if duelist and duelist != interaction.user else None

        await DEFER(interaction)

        if (QUIZ["active"] or QUIZ["second-player"]) or (LADDERS['status'] != "off"):
            await FOLLOWUP(f"Another game is in progress.", interaction, True)

        if newGame == "quiz":
            try:
                await StartQuiz(interaction.user, interaction.channel, interaction, duelists)
            except Exception as exc:
                await FOLLOWUP(f"Something went wrong with `/play quiz`: {exc}", interaction)
                raise
        elif newGame == "lucid_ladders":
            try:
                await PlayLucidLadders(interaction.user, interaction.channel, interaction, duelists)
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
                        msg += f"\n{duelist.mention}, you have been challenged by {interaction.user.mention}!"

                    view.message = await FOLLOWUP(msg, interaction, False, view)

                    await view.wait()
                    await view.too_late()
                except Exception as exc:
                    await FOLLOWUP(f"Something went wrong with `/play ttt`: {exc}", interaction)
                    raise
                finally:
                    BUTTONS["status"] = False
            else:
                await FOLLOWUP(f"Another game is in progress.", interaction, True)

    @discord.app_commands.command(name="hangman", description="Play a game of hangman")
    @discord.app_commands.describe(
        word="Optional: Provide a custom word to guess (leave empty for a random word)",
        alone="Optional: Set to true if you want to play alone (default: false)",
        duelist="Optional: Challenge a friend to play with you."
    )
    async def hangman(self, interaction: discord.Interaction, word: str = None, alone: bool = False, duelist: discord.Member = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the server!", True)
            return

        duelists = [duelist, interaction.user] if duelist and duelist != interaction.user else None
        await DEFER(interaction, True)

        if BUTTONS["status"]:
            await FOLLOWUP("Another game is in progress.", interaction, True)
            return

        if word and alone:
            await FOLLOWUP("You want me to play along like that?", interaction, True)
            return
        
        if duelist and alone:
            await FOLLOWUP("Make a decision... To play alone, or to challenge someone!", interaction, True)
            return
        
        if duelist and word:
            await FOLLOWUP("They were right in saying Hangman is rigged!", interaction, True)
            return
        
        try:
            target_word = word.lower() if word else None
            view = Minigames_Hangman(timeout=120)
            view.alone = alone
            BUTTONS["status"] = True
            BUTTONS["channel"] = interaction.channel

            if word:
                if not re.match("^[a-zA-Z ]*$", target_word):
                    await FOLLOWUP("Your word contains invalid characters.", interaction, True)
                    BUTTONS["status"] = False
                    return
                
                if "q" in target_word:
                    await FOLLOWUP("Your word contains the letter Q. Since the button limit is 25, one letter of the alphabet had to go. Pick another word.", interaction, True)
                    BUTTONS["status"] = False
                    return
                
                if len(target_word) >= 32:
                    await FOLLOWUP("Your word is too long.", interaction, True)
                    BUTTONS["status"] = False
                    return

                for badword in self.bot.blacklist:
                    if badword in target_word:
                        await FOLLOWUP("Your word is inappropriate.", interaction, True)
                        BUTTONS["status"] = False
                        return

                view.myword = target_word
                view.picker = interaction.user
            else:
                random_word = random.choice(self.bot.word_list).lower()
                while "q" in random_word:
                    random_word = random.choice(self.bot.word_list).lower()
                view.myword = random_word

            view.current = "".join([" " if i == " " else "-" for i in view.myword])
            
            view.status = ""
            for i in range(view.lifes):
                view.status += "🟩"
            view.status += "<:csStairbonk:812813052822421555>"

            if view.alone:
                view.cp = interaction.user

            msg = f"Can you guess the word {view.picker.mention if view.picker else 'I am'} thinking?\n\n`{view.current}`\n\n{view.status}"
            
            await FOLLOWUP("Setting up the poor Hangman...", interaction, True)

            await asyncio.sleep(1)

            if duelist:
                view.duelists = duelists
                msg += f"\n{duelist.mention}, you have been challenged by {interaction.user.mention}!"

            view.message = await SEND_VIEW(BUTTONS["channel"], msg, view)

            await view.wait()
            await view.too_late()
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/hangman`: {exc}", interaction)
            raise
        finally:
            BUTTONS["status"] = False

