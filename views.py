import time

from globals import *
from rated import *
from roles import *
from globals import *
from discord.ext import commands

class SplicerView(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        disableSplicer()

        await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

    async def too_late(self):
        if self.toolate:
            await SEND(self.message.channel, "Too little, too late.")

        await self.on_timeout()

    @discord.ui.button(label="Refuse", custom_id = "SpliceNameNo", style = discord.ButtonStyle.red)
    async def declined(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        if usr == SPLICER_RIG["user"] and SPLICER_RIG["active"]:
            disableSplicer()
            
            await INTERACTION(interaction.response, "Splice request declined. That's too bad.", False)
            self.toolate = False
            self.stop()
        else:
            await INTERACTION(interaction.response, "Do not force your opinion on others.", True)

    @discord.ui.button(label="Accept your fate", custom_id = "SpliceNameYes", style = discord.ButtonStyle.green)
    async def accepted(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        if usr == SPLICER_RIG["user"] and SPLICER_RIG["active"]:
            await EDIT_NICK(usr, SPLICER_RIG["user-name"])
            await asyncio.sleep(1)
            await EDIT_NICK(RIG_DATA['rigCaster'], SPLICER_RIG['rigcaster-name'])

            disableSplicer()

            await INTERACTION(interaction.response, "Splice request accepted. Enjoy your new display names.", False)
            self.toolate = False
            self.stop()
        else:
            await INTERACTION(interaction.response, "Do not force your opinion on others.", True)

class FirstButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

    async def too_late(self) -> None:
        await self.on_timeout()
        await SEND(BUTTONS["channel"], "I usually press a button when I see one.")

    @discord.ui.button(label="What's this?", style = discord.ButtonStyle.secondary)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if usr not in self.users.keys():
            self.users[usr] = 0
        else:
            self.users[usr] += 1

        if self.users[usr] == 0:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 1:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 2:
            await INTERACTION(interaction.response, "This interaction will not fail on my watch.", True)

        elif self.users[usr] == 3:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 4:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 5:
            await INTERACTION(interaction.response, "Alright. That's enough pressing.", True)

        elif self.users[usr] == 6:
            await INTERACTION(interaction.response, "I am being serious. If you keep going I'll get rate limited.", True)

        elif self.users[usr] == 7:
            await INTERACTION(interaction.response, f"{usr.mention} has successfully pressed this button.", False)
            self.stop()

# class CastAgain(discord.ui.View):
#     async def on_timeout(self):
#         for item in self.children:
#             item.disabled = True

#         RIG_DATA["rigType"] = None
#         RIG_DATA["rigChannel"] = None
#         RIG_DATA["message"] = None

#         await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

#     async def too_late(self) -> None:
#         await self.on_timeout()

#     @discord.ui.button(label="Cast again!", custom_id = "Recast", style = discord.ButtonStyle.primary)
#     async def casting(self, interaction: discord.Interaction, button: discord.ui.Button):
#         usr = interaction.user
#         if usr == RIG_DATA["rigCaster"] and self.message == RIG_DATA["message"]:
            
#             await Rig(RIG_DATA["rigType"], RIG_DATA["rigChannel"], RIG_DATA["rigCaster"])
#             self.stop()
#         else:
#             await INTERACTION(interaction.response, "You did not cast this rig.", True)