import time
import random

from globals import *
from database import *
from rated import *
from roles import *
from globals import *
from discord.ext import commands

class ShowProfile(discord.ui.View):
    cp  = 0
    sep = 2
    titles = ["{user}'s secret roles",
              "{user}'s locked roles",
              "{user}'s stats"]
    sidecolor = ["FFA500",
                 "FF0000",
                 "FFC0CB"]  
    embed = None
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await self.message.edit(embed=self.embed, view=self)

    async def send(self, ch):
        self.message = await ch.send(view=self)
        await self.update_message()

    def create_embed(self):
        embed = discord.Embed()
        embed.title = self.titles[self.cp].format(user=self.target.display_name)
        embed.description = self.data[self.cp]
        embed.set_footer(text=self.footers[self.cp].format(usr=self.target.display_name, stotal=self.totsroles, ltotal=self.totlroles, scurrent=self.sroles, lcurrent=self.lroles))

        if self.sroles != self.totsroles:
            embed.color = discord.Colour(int(self.sidecolor[self.cp], 16)) 
        else:
            embed.color = discord.Colour(int("FFD700", 16)) 


        self.embed = embed
        return embed

    async def update_message(self):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(), view=self)

    def update_buttons(self):
        if self.cp == 0:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.cp == 2:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    async def check_requester(self, interaction):
            if interaction.user != self.requester:
                await INTERACTION(interaction.response, "Keep your hands to yourself.", True)
                return

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction)
        await interaction.response.defer()
        self.cp = 0

        await self.update_message()

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction)
        await interaction.response.defer()
        self.cp -= 1
        await self.update_message()

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction)
        await interaction.response.defer()
        self.cp += 1
        await self.update_message()

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction)
        await interaction.response.defer()
        self.cp = 2
        await self.update_message()

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

            # if not str(usr.id) in list_decoded_entries("Persistent Clicker"): 3 roles for 3 games are enough. next ones will not grant roles either.
            #     await add_entry_with_check("Persistent Clicker", usr)
            
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
            await interaction.response.defer()
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
            BUTTONS["phase"] = 4

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
            await interaction.response.defer()

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
            await SEND(BUTTONS["channel"], "Where is the support when you need it?")
            await self.on_timeout()

    async def process_click(self, interaction, button, usr):
        if usr in self.users:
            await INTERACTION(interaction.response, "I need someone else now.", True)
            return
        elif str(usr.id) in self.roleowners:
            await INTERACTION(interaction.response, "You have been helpful to me in the past, but I don't require your assistance at the moment.", True)
            return

        self.users.append(usr)
        self.step += 1
        if self.step < 4:
            await interaction.response.defer()
            button.label = f"{usr.name}"
            button.style = discord.ButtonStyle.green
            button.disabled = True
            await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)
        elif self.step == 4:
            self.toolate = False
            BUTTONS["phase"] = 1
            button.label = f"{usr.name}"
            button.style = discord.ButtonStyle.green
            button.disabled = True
            await self.on_timeout()
            await asyncio.sleep(10)
            newview = FourthButtonFinal(timeout = 60)
            newview.users = self.users
            newview.clicked = []
            newview.message = self.message
            await EDIT_VIEW_MESSAGE(self.message, "Thank you, take this button for your efforts.", newview)

            await newview.wait()
            await newview.too_late()
            self.stop()

    @discord.ui.button(label="Broken Drone", custom_id = "1", style = discord.ButtonStyle.green, disabled = True)
    async def B1(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="2", custom_id = "2", style = discord.ButtonStyle.blurple)
    async def B2(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="3", custom_id = "3", style = discord.ButtonStyle.blurple)
    async def B3(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="4", custom_id = "4", style = discord.ButtonStyle.blurple)
    async def B4(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="5", custom_id = "5", style = discord.ButtonStyle.blurple)
    async def B5(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

class FourthButtonFinal(discord.ui.View):
    async def on_closed(self):
        for item in self.children:
            item.disabled = True
            item.label = "Exhausted"

        await EDIT_VIEW_MESSAGE(self.message, "Good work.", self)

    async def too_late(self):
        if len(self.clicked) != len(self.users):
            await SEND(BUTTONS["channel"], "Someone didn't take my gift, but who cares.")

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
        await add_entry_with_check("Broken Drone Helper", usr)

        if len(self.clicked) == len(self.users):
            await self.on_closed()

class FifthButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, f"The hangman's fate is sealed.\n\n`{self.current}`\n\n{self.status}", self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS["channel"], f"How sad. I was thinking about: {str(self.myword)}.")

        await self.on_timeout()

    async def update_revealed(self, interaction, button):
        self.current = ""
        for i in self.myword:
            if str(i).lower() in self.revealed:
                self.current += str(i).upper()
            else:
                if str(i) != " ":
                    self.current += "_"
                else:
                    self.current += " "

        await EDIT_VIEW_MESSAGE(self.message, f"Keep it going!\n\n`{self.current}`\n\n{self.status}\n\nWrong letters used so far: {self.wrong}\n\nLast move: {self.cp.mention} guessed {self.cl}", self)

        if "_" not in self.current:
            # best_user = max(self.players, key=lambda user: len(self.players[user]))
            max_length = max(len(guesses) for guesses in self.players.values())
            best_users = [user.mention for user, letters in self.players.items() if len(letters) == max_length]

            for plr in self.players.keys():
                self.result += f"{plr.display_name}'s correct guesses: {len(self.players[plr])}\n"
            await INTERACTION(interaction.response, f"The users with the most correct guesses are: {', '.join(best_users)}", False)
            self.toolate = False
            self.stop()
        else:
            await interaction.response.defer()

    async def update_mistake(self, interaction, button):
        self.status = "<:csSleazel:786328102392954921>"

        for i in range(self.lifes):
            if self.lifes == 1:
                self.status += "🟥"
            elif 2 <= self.lifes <= 3:
                self.status += "🟧"
            else:
                self.status += "🟩"

        if self.lifes > 0:
            self.status += "<:csStairbonk:812813052822421555>" 
        else:
            self.status = "<:csPranked:786317086066343936><:csThegun:786629172101513216><:csStairbonk:812813052822421555>" 

        await EDIT_VIEW_MESSAGE(self.message, f"How reckless.\n\n`{self.current}`\n\n{self.status}\n\nWrong letters used so far: {self.wrong}\n\nLast move: {self.cp.mention} guessed {self.cl}", self) 

        if self.lifes <= 0:
            await INTERACTION(interaction.response, f"{interaction.user.mention} should be ashamed of themselves. I was thinking about: {self.myword}", False)
            self.toolate = False
            self.stop()
        else:
            await interaction.response.defer()

    async def process_click(self, interaction, button, usr):

        if self.alone:
            if usr != self.cp:
                await INTERACTION(interaction.response, "This user is playing solo.", True)
        else:
            if usr == self.cp:
                await INTERACTION(interaction.response, "It's someone else's turn now.", True)
                return
            else:
                self.cp = usr

        if self.wrong == "":
            self.wrong = "None"

        self.cl = str(button.custom_id).upper()

        if str(button.custom_id).lower() in self.myword:
            button.style = discord.ButtonStyle.green
            button.disabled = True
            self.revealed.append(str(button.custom_id).lower())

            self.players[usr].append(str(button.custom_id).upper())

            await self.update_revealed(interaction, button)
        else:
            self.lifes -= 1

            if str(button.custom_id).upper() not in self.wrong:
                self.wrong += str(button.custom_id).upper() + " "

            await self.update_mistake(interaction, button)


    @discord.ui.button(label="A", custom_id = "a",  style = discord.ButtonStyle.blurple)
    async def B1(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="B", custom_id = "b",  style = discord.ButtonStyle.blurple)
    async def B2(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="C", custom_id = "c",  style = discord.ButtonStyle.blurple)
    async def B3(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="D", custom_id = "d",  style = discord.ButtonStyle.blurple)
    async def B4(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="E", custom_id = "e",  style = discord.ButtonStyle.blurple)
    async def B5(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="F", custom_id = "f",  style = discord.ButtonStyle.blurple)
    async def B6(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="G", custom_id = "g",  style = discord.ButtonStyle.blurple)
    async def B7(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="H", custom_id = "h",  style = discord.ButtonStyle.blurple)
    async def B8(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="I", custom_id = "i",  style = discord.ButtonStyle.blurple)
    async def B9(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="J", custom_id = "j",  style = discord.ButtonStyle.blurple)
    async def B10(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="K", custom_id = "k",  style = discord.ButtonStyle.blurple)
    async def B11(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="L", custom_id = "l",  style = discord.ButtonStyle.blurple)
    async def B12(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="M", custom_id = "m",  style = discord.ButtonStyle.blurple)
    async def B13(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="N", custom_id = "n",  style = discord.ButtonStyle.blurple)
    async def B14(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="O", custom_id = "o",  style = discord.ButtonStyle.blurple)
    async def B15(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="P", custom_id = "p",  style = discord.ButtonStyle.blurple)
    async def B16(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="R", custom_id = "r",  style = discord.ButtonStyle.blurple)
    async def B18(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="S", custom_id = "s",  style = discord.ButtonStyle.blurple)
    async def B19(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="T", custom_id = "t",  style = discord.ButtonStyle.blurple)
    async def B20(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="U", custom_id = "u",  style = discord.ButtonStyle.blurple)
    async def B21(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="V", custom_id = "v",  style = discord.ButtonStyle.blurple)
    async def B22(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="W", custom_id = "w",  style = discord.ButtonStyle.blurple)
    async def B23(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="X", custom_id = "x",  style = discord.ButtonStyle.blurple)
    async def B24(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Y", custom_id = "y",  style = discord.ButtonStyle.blurple)
    async def B25(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="Z", custom_id = "z",  style = discord.ButtonStyle.blurple)
    async def B17(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user

        await self.process_click(interaction, button, usr)

class BurgerButton(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, 'The burger is dead D:', self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS['channel'], 'burger over')

        await self.on_timeout()

    @discord.ui.button(label="🍔", style = discord.ButtonStyle.blurple)
    async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await INTERACTION(interaction.response, "🍔", True)




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