import time
import random

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
            item.label = "It's just a button."
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, "I was right.", self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS["channel"], "I usually press a button when I see one.")

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
            await INTERACTION(interaction.response, "Alright. That's enough pressing.", True)

        elif self.users[usr] == 6:
            await INTERACTION(interaction.response, "I am being serious. If you keep going I'll get rate limited.", True)

        elif self.users[usr] == 7:
            await INTERACTION(interaction.response, f"{usr.mention} has successfully pressed this button.", False)
            self.toolate = False
            BUTTONS["phase"] = 2
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

    @discord.ui.button(label="Button", custom_id = "1",  style = discord.ButtonStyle.blurple)
    async def B1(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "2",  style = discord.ButtonStyle.blurple)
    async def B2(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "3",  style = discord.ButtonStyle.blurple)
    async def B3(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "4",  style = discord.ButtonStyle.blurple)
    async def B4(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "5",  style = discord.ButtonStyle.blurple)
    async def B5(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "6",  style = discord.ButtonStyle.blurple)
    async def B6(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "7",  style = discord.ButtonStyle.blurple)
    async def B7(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "8",  style = discord.ButtonStyle.blurple)
    async def B8(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "9",  style = discord.ButtonStyle.blurple)
    async def B9(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "10",  style = discord.ButtonStyle.blurple)
    async def B10(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "11",  style = discord.ButtonStyle.blurple)
    async def B11(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "12",  style = discord.ButtonStyle.blurple)
    async def B12(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "13",  style = discord.ButtonStyle.blurple)
    async def B13(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "14",  style = discord.ButtonStyle.blurple)
    async def B14(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "15",  style = discord.ButtonStyle.blurple)
    async def B15(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "16",  style = discord.ButtonStyle.blurple)
    async def B16(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "17",  style = discord.ButtonStyle.blurple)
    async def B17(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "18",  style = discord.ButtonStyle.blurple)
    async def B18(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "19",  style = discord.ButtonStyle.blurple)
    async def B19(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "20",  style = discord.ButtonStyle.blurple)
    async def B20(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "21",  style = discord.ButtonStyle.blurple)
    async def B21(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "22",  style = discord.ButtonStyle.blurple)
    async def B22(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "23",  style = discord.ButtonStyle.blurple)
    async def B23(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "24",  style = discord.ButtonStyle.blurple)
    async def B24(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

    @discord.ui.button(label="Button", custom_id = "25",  style = discord.ButtonStyle.blurple)
    async def B25(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if button.custom_id == self.correct_button:
            await INTERACTION(interaction.response, f"{usr.mention} pressed the correct button.", False)
            button.style = discord.ButtonStyle.green
            self.toolate = False
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

class ThirdButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            if not len(self.users) <= 1:
                item.label = f"{self.winning.name} was here."
                await EDIT_VIEW_MESSAGE(self.message, "Not my button anymore.", self)
            else:
                item.label = "Still my button."
                await EDIT_VIEW_MESSAGE(self.message, "I get to keep my button.", self)

    async def too_late(self):
        if len(self.users) <= 1:
            await SEND(BUTTONS["channel"], "Thank you very much.")
        else:
            await SEND(BUTTONS["channel"], f"{self.winning.mention} now owns my former button.")

        await self.on_timeout()

    @discord.ui.button(label="Broken Drone button", style = discord.ButtonStyle.secondary)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        if usr not in self.users:
            self.users.append(usr)

        if usr == self.winning:
            await INTERACTION(interaction.response, "The button is yours.", True)
        else:
            button.label = f"{usr.name} button"
            button.style = discord.ButtonStyle.green
            self.winning = usr
            await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

            


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