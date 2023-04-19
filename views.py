import time
import random

from globals import *
from database import *
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
            item.label = "It's just a button."
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, "I was right.", self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS["channel"], "Sleazel would have clicked it.")

        await self.on_timeout()

    @discord.ui.button(label="What's this?", style = discord.ButtonStyle.blurple)
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
            await INTERACTION(interaction.response, "Alright. That's enough clicking.", True)

        elif self.users[usr] == 6:
            await INTERACTION(interaction.response, "I am being serious. If you keep going I'll get rate limited.", True)

        elif self.users[usr] == 7:
            await INTERACTION(interaction.response, f"{usr.mention} has successfully clicked this button.", False)
            self.toolate = False
            BUTTONS["phase"] = 2

            if not str(usr.id) in list_decoded_entries("Persistent Clicker"):
                await add_entry_with_check("Persistent Clicker", usr)
            
            self.stop()


class SecondButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.label = "..."
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, "That's a wrap.", self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS["channel"], "So many buttons to press, I was torn as well.")

        await self.on_timeout()

    async def process_click(self, interaction, button, usr):
        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} clicked the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
            if not str(usr.id) in list_decoded_entries("Lucky Button"):
                await add_entry_with_check("Lucky Button", usr)
            BUTTONS["phase"] = 3
            self.stop()
        else:
            if self.pressed > len(BUTTONS["phase2labels"]) - 1:
                button.label = BUTTONS["phase2labels"][10]
                await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)
            else:
                button.label = BUTTONS["phase2labels"][self.pressed]
            button.style = discord.ButtonStyle.red
            button.disabled = True


            self.pressed += 1
            await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

    @discord.ui.button(label="Button", custom_id = "1",  style = discord.ButtonStyle.blurple)
    async def B1(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "2",  style = discord.ButtonStyle.blurple)
    async def B2(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "3",  style = discord.ButtonStyle.blurple)
    async def B3(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "4",  style = discord.ButtonStyle.blurple)
    async def B4(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "5",  style = discord.ButtonStyle.blurple)
    async def B5(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "6",  style = discord.ButtonStyle.blurple)
    async def B6(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "7",  style = discord.ButtonStyle.blurple)
    async def B7(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "8",  style = discord.ButtonStyle.blurple)
    async def B8(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "9",  style = discord.ButtonStyle.blurple)
    async def B9(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "10",  style = discord.ButtonStyle.blurple)
    async def B10(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "11",  style = discord.ButtonStyle.blurple)
    async def B11(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "12",  style = discord.ButtonStyle.blurple)
    async def B12(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "13",  style = discord.ButtonStyle.blurple)
    async def B13(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "14",  style = discord.ButtonStyle.blurple)
    async def B14(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "15",  style = discord.ButtonStyle.blurple)
    async def B15(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "16",  style = discord.ButtonStyle.blurple)
    async def B16(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "17",  style = discord.ButtonStyle.blurple)
    async def B17(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "18",  style = discord.ButtonStyle.blurple)
    async def B18(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "19",  style = discord.ButtonStyle.blurple)
    async def B19(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "20",  style = discord.ButtonStyle.blurple)
    async def B20(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "21",  style = discord.ButtonStyle.blurple)
    async def B21(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "22",  style = discord.ButtonStyle.blurple)
    async def B22(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "23",  style = discord.ButtonStyle.blurple)
    async def B23(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "24",  style = discord.ButtonStyle.blurple)
    async def B24(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Button", custom_id = "25",  style = discord.ButtonStyle.blurple)
    async def B25(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

class ThirdButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            if not len(self.users) <= 1:
                item.label = f"{self.winning.name} was here"
                await EDIT_VIEW_MESSAGE(self.message, "Not my button anymore.", self)
            else:
                item.label = "Still my button"
                item.style = discord.ButtonStyle.red
                await EDIT_VIEW_MESSAGE(self.message, "I get to keep my button.", self)

    async def too_late(self):
        if len(self.users) <= 1:
            await SEND(BUTTONS["channel"], "Thank you very much.")
        else:
            await SEND(BUTTONS["channel"], f"{self.winning.mention} stole my button after `{self.clicks}` interactions.")

            if not str(self.winning.id) in list_decoded_entries("Last One"):
                await add_entry_with_check("Last One", self.winning)
            BUTTONS["phase"] = 1

        await self.on_timeout()

    @discord.ui.button(label="Broken Drone button", style = discord.ButtonStyle.secondary)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if usr not in self.users:
            self.users.append(usr)

        if self.clicks >= 150:
            self.step = 2
            self.timeout = 5
            self.tm = 5
        elif self.clicks >= 100:
            self.step = 1
            self.timeout = 15
            self.tm = 15

        if usr == self.winning:
            await INTERACTION(interaction.response, "The button is yours.", True)
            await EDIT_VIEW_MESSAGE(self.message, BUTTONS["phase3again"][self.step].format(mention = usr.name, time = round(time.time() + self.tm)), self)
        else:
            button.label = f"{usr.name} button"
            button.style = discord.ButtonStyle.green
            self.winning = usr
            self.clicks += 1
            await EDIT_VIEW_MESSAGE(self.message, BUTTONS["phase3new"][self.step].format(mention = usr.name, time = round(time.time() + self.tm)), self)

class FourthButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            if item.style != discord.ButtonStyle.green:
                item.style = discord.ButtonStyle.red
                item.label = "Empty"

        await EDIT_VIEW_MESSAGE(self.message, "Help is not needed anymore.", self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS["channel"], "Where are the people when you need them?")
            await self.on_timeout()

    async def process_click(self, interaction, button, usr):
        if usr in self.users:
            await INTERACTION(interaction.response, "I need someone else now.", True)
            return
        elif str(usr.id) in self.roleowners:
            await INTERACTION(interaction.response, "You did help me in the past, there's no need now.", True)
            return

        self.users.append(usr)
        self.step += 1
        if self.step < 2:
            button.label = f"{usr.name}'s help"
            button.style = discord.ButtonStyle.green
            button.disabled = True
            await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)
        elif self.step == 2:
            self.toolate = False
            button.label = f"{usr.name}'s help"
            button.style = discord.ButtonStyle.green
            button.disabled = True
            await self.on_timeout()
            await asyncio.sleep(3)
            newview = FourthButtonFinal(timeout = 20)
            newview.users = self.users
            newview.clicked = []
            newview.message = await EDIT_VIEW_MESSAGE(self.message, "Thank you, take this button for your efforts.", newview)

            await newview.wait()
            await newview.too_late()
            newview.stop()

    @discord.ui.button(label="1", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="2", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="3", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="4", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="5", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

class FourthButtonFinal(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.label = "Exhausted"
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, "Well done.", self)

    async def too_late(self):
        if len(self.clicked) != len(self.users):
            await SEND(BUTTONS["channel"], "Someone didn't click it, but who cares.")

        await self.on_timeout()

    @discord.ui.button(label="Take", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if usr not in self.users:
            await INTERACTION(interaction.response, "You did not help.", True)
            return
        elif usr in self.clicked:
            await INTERACTION(interaction.response, "I do not have any more buttons for you.", True)
            return
        
        self.clicked.append(usr)
        await INTERACTION(interaction.response, "Here, take this button.", True)
        await add_entry_with_check("Broken Drone Helper", usr.id)

        if len(self.clicked) != len(self.users):
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