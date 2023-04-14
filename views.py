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
            
            await interaction.response.send_message("Splice request declined. That's too bad.")
            self.stop()

    @discord.ui.button(label="Accept your fate", custom_id = "SpliceNameYes", style = discord.ButtonStyle.green)
    async def accepted(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        if usr == SPLICER_RIG["user"] and SPLICER_RIG["active"] and self.message == SPLICER_RIG["reactionmessage"]:
            await EDIT_NICK(usr, SPLICER_RIG["user-name"])
            await asyncio.sleep(1)
            await EDIT_NICK(RIG_DATA['rigCaster'], SPLICER_RIG['rigcaster-name'])

            disableSplicer()

            await interaction.response.send_message("Splice request accepted. Enjoy your new display names.")
            self.stop()