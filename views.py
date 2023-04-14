import time

from globals import *
from rated import *
from roles import *
from globals import *
from discord.ext import commands

class SplicerView(discord.ui.View):
    async def tooLate(self):
        for item in self.children:
            item.disabled = True

        disableSplicer()

        await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

    async def on_timeout(self) -> None:
        await self.tooLate()
        await SEND(self.message.channel, "Too little, too late.")

    @discord.ui.button(label="Refuse", custom_id = "SpliceNameNo", style = discord.ButtonStyle.red)
    async def declined(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        if usr == SPLICER_RIG["user"] and SPLICER_RIG["active"] and self.message == SPLICER_RIG["reactionmessage"]:
            disableSplicer()
            
            await INTERACTION(interaction.response, "Splice request declined. That's too bad.", False)
            self.stop()
        else:
            await INTERACTION(interaction.response, "Do not force your opinion on others.", True)

    @discord.ui.button(label="Accept your fate", custom_id = "SpliceNameYes", style = discord.ButtonStyle.green)
    async def accepted(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        if usr == SPLICER_RIG["user"] and SPLICER_RIG["active"] and self.message == SPLICER_RIG["reactionmessage"]:
            await EDIT_NICK(usr, SPLICER_RIG["user-name"])
            await asyncio.sleep(1)
            await EDIT_NICK(RIG_DATA['rigCaster'], SPLICER_RIG['rigcaster-name'])

            disableSplicer()

            await INTERACTION(interaction.response, "Splice request accepted. Enjoy your new display names.", False)
            self.stop()
        else:
            await INTERACTION(interaction.response, "Do not force your opinion on others.", True)

class CastAgain(discord.ui.View):
    async def tooLate(self):
        for item in self.children:
            item.disabled = True

        RIG_DATA["rigType"] = None
        RIG_DATA["rigChannel"] = None
        RIG_DATA["message"] = None

        await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

    async def on_timeout(self) -> None:
        await self.tooLate()

    @discord.ui.button(label="Cast again!", custom_id = "Recast", style = discord.ButtonStyle.primary)
    async def casting(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        if usr == RIG_DATA["rigCaster"] and self.message == RIG_DATA["message"]:
            
            await Rig(RIG_DATA["rigType"], RIG_DATA["rigChannel"], RIG_DATA["rigCaster"])
            self.stop()
        else:
            await INTERACTION(interaction.response, "You did not cast this rig.", True)