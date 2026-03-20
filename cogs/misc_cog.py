import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from globals import FIX_BOT, EXTRA_ROLES, ACTIVE_RIGS, DETAILED_RIGS, RIG_COOLDOWNS, BUTTONS
from rated import DEFER, FOLLOWUP, INTERACTION, SEND
from quiz import FORCE_CLOSE_EVENT
from ladders import MG_RESET
from views import ButtonGames_ThrowingStuff

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="reset", description="Reset Broken Drone")
    async def reset(self, interaction: discord.Interaction):
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
    
    @discord.app_commands.command(name="poll", description="Create a poll with buttons")
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None, option8: str = None, option9: str = None, option10: str = None, option11: str = None, option12: str = None, option13: str = None, option14: str = None, option15: str = None, option16: str = None, option17: str = None, option18: str = None, option19: str = None, option20: str = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel
        all_options = [
            option1, option2, option3, option4, option5, option6, 
            option7, option8, option9, option10, option11, option12, 
            option13, option14, option15, option16, option17, option18, 
            option19, option20
        ]
        active_options = [opt for opt in all_options if opt is not None]

        if BUTTONS["status"]:
            await INTERACTION(interaction, "A poll is already active.", True)
            return

        await DEFER(interaction)

        try:
            BUTTONS["status"] = True
            pollA = active_options
            pollQ = question

            if len(pollA) < 2:
                await FOLLOWUP('You need to provide at least 2 options to create a poll.', interaction, True)
                BUTTONS["status"] = False
                return

            for badword in self.bot.blacklist:
                for answer in pollA:
                    if (badword in answer.lower()) or (badword in pollQ.lower()):
                        await FOLLOWUP("Your poll contains inappropriate content.", interaction, True)
                        # await SEND(ch, "Your poll contains inappropriate content.")
                        BUTTONS["status"] = False
                        return

            view = ButtonGames_ThrowingStuff(timeout=600)
            view.choices = pollA
            view.customUser = usr

            for i in range(0, len(active_options)):
                view.votes[str(i)] = []
                view.add_item(discord.ui.Button(label=view.choices[i], custom_id=f"throw{i}", style=discord.ButtonStyle.primary))

            view.add_item(discord.ui.Button(label="Close Poll", custom_id="throwclose", style=discord.ButtonStyle.red))

            BUTTONS["view"] = view
            BUTTONS["channel"] = ch

            # view.message = await SEND_VIEW(BUTTONS["channel"], pollQ, view)
            view.message = await FOLLOWUP(pollQ, interaction, False, view=view)

            await view.wait()
            await view.too_late()
            BUTTONS["status"] = False
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/poll`: {exc}", interaction)
            raise