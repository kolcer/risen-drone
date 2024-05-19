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

class ShowCommands(discord.ui.View):    
    data = [
        '''
        Please use these commands only in <#750060041289072771>

**morph to** *[alignment]*
➡️ Get chosen alignment role in this server (Remember to always read the server rules)

**demorph from** *[alignment]*
➡️ Remove chosen alignment role

**sub to** *[ping role]*
➡️ Subscribe to chosen ping role

**unsub from** *[ping role]*
➡️ Unsubscribe from chosen ping role

**general tip**
➡️ Show a general tip

*[alignment]* **tip**
➡️ Show chosen alignment tip

**general trivia**
➡️ Show a general trivia

*[alignment]* **trivia**
➡️ Show chosen alignment trivia


**Available aligments**: Patron, Joker, Wicked, Spectre, Muggle, Chameleon, Keeper, Hacker, Thief, Archon, Drifter, Heretic.
**Extra alignments** *(cannot be morphed into)*: Possessed, None, Architect.
**Available ping roles**: Updates, Announcements, Events, Polls, Minigames, Sleazel-in-game (sub if you want Prank The Creator badge)
        ''',

        '''
        With the exception of Revive Chat, use these commands in <#750060041289072771>

**bd show profile**
➡️ Admire your roles collection and some of your statistics

**cast** *[alignment]* **rig**
➡️ Your favorite Alignment's rig, but on Discord

**drone of wisdom**
➡️ Receive wisdom directly from myself that will change how you perceive the world

**create poll|[question]|[answer 1]|[answer 2]|[answer 3]|[answer 4]...** (2 to 19 answers)
➡️ Create a poll with a question and its possible answers, votes will be revealed when it's closed 

**revive chat**
➡️ How could you

**reset bot**
➡️ Use this command if I become unresponsive (which I won't) (3 users required)



** USER COMMANDS **

*Attention! The bot no longer checks for user discriminator as Discord should have forced every user to remove them.*


**bd scold** *[username]*
➡️ They should not have done that

**give mana to** *[username]*
➡️ Remove the Possessed role from the user (does not apply to users muted by moderators)


**Available aligments**: Patron, Joker, Wicked, Spectre, Muggle, Chameleon, Keeper, Hacker, Thief, Archon, Drifter, Heretic, Splicer, Necromancer.
        ''',

        '''
        I hope you did not forget, but use these commands in <#750060041289072771>

**play lucid ladders**
➡️ Start Lucid Ladders minigame (requires at least 2 players)

**start quiz**
➡️ Start Crazy Stairs knowledge quiz (2 players required, 20 questions, timed)

**play hangman** *?*
➡️ Play hangman with the other members or by yourself
*[? = alone, to play alone | ? = CUSTOMWORD, to make your own hangman | leave empty for a random word]*
        ''',

        '''
        I hope you showed these commands in <#813882658156838923> 

**|ispy** *[channel-name]*
➡️ Start an "ispy" mini-game in the specified channel

**|quiz** *[action] [?]*
➡️ New: Creates a new quiz question with the format "Question|Correct answer|Option 1|Option 2|Option 3|[Automatic user mention +] Good response|Bad response".
Count: Displays the number of currently existing quiz questions.
Print: Prints a specified quiz question with its answer, options, and responses. Specify the question index in the [?] section.
List: Lists all current quiz questions.
Delete: Deletes the specified quiz question by index.

**|makesay** *[channel-name] [message]*
➡️ Have the bot repeat what you say

**|ckr to/from** *[username]*
➡️ Give/remove the Chat Killer role

**|nr** *[name]*
➡️ Create new custom role :bangbang:

**|un/assign** *[!!USER ID!!] [role-name]*
➡️ Remove/assign custom roles :bangbang:

**|purge role** *[role-name]*
➡️ Delete a custom role :bangbang:

**|buttons** *[num] [channel]*
➡️ Start button minigame
1: Fake Interaction
2: So Many Buttons
3: Help Broken Drone
4: Tic Tac Toe
5: Poll


:bangbang: Must be in the FUN_ROLES list in globals.py
        ''',
    ]

    cp  = 0
    titles = [
        "Basic Commands",
        "Fun Commands",
        "Minigames Commands",
        "Drone Master Commands"
    ]

    footers = [
        "Morph to your favorite Alignments and subscribe to various pings to be notified of stuff.", 
        "Use my commands and have some fun. !!Discriminator no longer has to be included for the command to work!!", 
        "Play some of the minigames currently available. They require participation from more people.",
        "What are you up to??"
    ]
    
    sidecolor = [
        "FFA500",
        "FF0000",
        "FFC0CB",
        "FFC0CB"
    ]

    data_original = data.copy()
    footers_original = footers.copy()
    titles_original = titles.copy()
    
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
        embed.title = self.titles[self.cp]
        embed.description = self.data[self.cp]
        embed.set_footer(text=self.footers[self.cp])

        embed.color = discord.Colour(int(self.sidecolor[self.cp], 16)) 
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

        if self.cp == 2 or self.cp == 3:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

        if self.cp == 3:
            self.admin_button.disabled = True
            self.admin_button.style = discord.ButtonStyle.gray
        else:
            self.admin_button.disabled = False
            self.admin_button.style = discord.ButtonStyle.red

        if not EXTRA_ROLES['admin'] in self.requester.roles:
            self.admin_button.disabled = True


    async def check_requester(self, interaction, button):
            if interaction.user != self.requester:
                await INTERACTION(interaction.response, "You did not ask for help, did you?", True)
                return
            
            if button.custom_id == 'admin':
                if not EXTRA_ROLES['admin'] in interaction.user.roles:
                    await INTERACTION(interaction.response, "You somehow clicked the button, however, its content is far from your reach.", True)
                    return
                
    async def check_channel(self):
            if self.channel.id != 813882658156838923:
                self.data[3] = "🛡️"
                self.titles[3] = "Shield Simulator"
                self.footers[3] = "Shiny!"
            else:
                self.data[3] = self.data_original[3]
                self.titles[3] = self.titles_original[3]
                self.footers[3] = self.footers_original[3]
            

    @discord.ui.button(label="|<", custom_id='0', style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction, button)
        await interaction.response.defer()
        self.cp = 0

        await self.update_message()

    @discord.ui.button(label="<", custom_id='1', style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction, button)
        await interaction.response.defer()
        self.cp -= 1
        await self.update_message()

    @discord.ui.button(label=">", custom_id='2', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction, button)
        await interaction.response.defer()
        self.cp += 1
        await self.update_message()

    @discord.ui.button(label=">|", custom_id='3', style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction, button)
        await interaction.response.defer()
        self.cp = 2
        await self.update_message()

    @discord.ui.button(label="🛡️", custom_id='admin', row=2, style=discord.ButtonStyle.red)
    async def admin_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.check_requester(interaction, button)
        await self.check_channel()
        await interaction.response.defer()
        self.cp = 3
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

class ButtonGames_FakeInteractionFailed(discord.ui.View):

    FAKE_FAIL = [
        ["This interaction will not fail on my watch.", "Alright. That's enough clicking.", "I am being serious. If you keep going I'll get rate limited."],
        ["This interaction WILL fail on my watch.", "You got me.", "Yes, I was being funny."],
        ["You are not one to give up that easily.", "Persistent much?", "I heard that if you click the button enough times, Sleazel will give you a gift."],
        ["Still here?", "I'd figured you would just think this thing was broken and stop trying", "I was proved wrong."],
        ["Sleazel?!?", "Made you turn around.", "Made you think I made you turn around."],
        ["I am quite impressed, you found me out. Take this little secret role.", "I hope I did not make you feel that bad.", "Fun Fact: This button used to give a role."],
        ["Keep clicking for 100000 Robux.", "That click just now costed you 100000 Robux.", "Profit."],
        ["You know, I used to climb the stairs a while ago.", "It was pretty fun actually.", "But seeing people think they can stand on me is even more fun."],
        ["CON####GR###S##", "Y###U#####MA#######D######I####T#####J", "Do not worry. I am fine."],
        ["Once upon a time.", "There was a little drone that did not know what to do.", "But that was not me, because I am a genius."],
        ["Can you guess my favorite game?", "You have one more attempt.", "Why do you keep clicking the button? I asked a question."],
        ["This is the holy button.", "If you click it again you'll be cancelled.", "Blocked and reported."],
    ]

    lineOfQuestioning = -1
    
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

            # Generate a random index within the bounds of the list size
            self.lineOfQuestioning = random.randint(0, len(self.FAKE_FAIL) - 1)
        else:
            self.users[usr] += 1

        if self.users[usr] == 0:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 1:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 2:
            await INTERACTION(interaction.response, self.FAKE_FAIL[self.lineOfQuestioning][0], True)

        elif self.users[usr] == 3:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 4:
            self.users[usr] = self.users[usr]

        elif self.users[usr] == 5:
            await INTERACTION(interaction.response, self.FAKE_FAIL[self.lineOfQuestioning][1], True)

        elif self.users[usr] == 6:
            await INTERACTION(interaction.response, self.FAKE_FAIL[self.lineOfQuestioning][2], True)

        elif self.users[usr] == 7:
            await INTERACTION(interaction.response, f"{usr.mention} has successfully clicked this button.", False)
            self.toolate = False

            # if not str(usr.id) in list_decoded_entries("Persistent Clicker"): 3 roles for 3 games are enough. next ones will not grant roles either.
            #     await add_entry_with_check("Persistent Clicker", usr)
            
            self.stop()

class ButtonGames_SoManyButtons(discord.ui.View):
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
            await interaction.response.defer()

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

class ButtonGames_HelpBrokenDrone(discord.ui.View):
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
            button.label = f"{usr.name}"
            button.style = discord.ButtonStyle.green
            button.disabled = True
            await self.on_timeout()
            await asyncio.sleep(10)
            newview = ButtonGames_HelpBrokenDroneFinal(timeout = 60)
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

class ButtonGames_HelpBrokenDroneFinal(discord.ui.View):
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

class ButtonGames_TicTacToe(discord.ui.View):
    button_mapping = {
        "1": (0, 0),
        "2": (0, 1),
        "3": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "7": (2, 0),
        "8": (2, 1),
        "9": (2, 2),
    }

    row = None
    col = None
    letter = None

    pick_messages = [
        "I saw that incoming.",
        "That's cheating.",
        "You can do better.",
        "Little do you know...",
        "Your opponent must be shaking after that move.",
        "Not that one...",
        "How predictable.",
        "Even I could have come up with a better move.",
        "How ironic.",
        "You are two steps ahead, I see.",
        "TOP RIGHT.",
        "Oh no! Anyway.",
        "🤓.",
        "There is no way out of that.",
        "Between you and me, I favor you.",
        "You cannot cheese this game.",
        "I'm watching your every move."
    ]

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, "Game over.", self)

    async def too_late(self):
        if self.toolate:
            if len(self.players) < 2:
                await SEND(BUTTONS["channel"], "I was waiting.")
                return
            else:
                await SEND(BUTTONS["channel"], f"{self.lastplayer.mention} won due to the other player forfeiting.")

            await self.on_timeout()

    async def update_board(self, interaction, button):
        self.row, self.col = self.button_mapping.get(button.custom_id)
        self.board[self.row][self.col] = self.letter

        await self.check_content(interaction)

        # match button.custom_id:
        #     case "1":
        #         self.board[0][0] = letter
        #     case "2":
        #         self.board[0][1] = letter
        #     case "3":
        #         self.board[0][2] = letter

    async def check_content(self, interaction):
        # for item in self.children:
        #     if item.disabled == True:
        await EDIT_VIEW_MESSAGE(self.message, random.choice(self.pick_messages), self)
        await asyncio.sleep(1)

        if (
            # Check rows
            (self.board[0][0] == self.board[0][1] == self.board[0][2] == self.assignments[interaction.user]) or
            (self.board[1][0] == self.board[1][1] == self.board[1][2] == self.assignments[interaction.user]) or
            (self.board[2][0] == self.board[2][1] == self.board[2][2] == self.assignments[interaction.user]) or
            # Check columns
            (self.board[0][0] == self.board[1][0] == self.board[2][0] == self.assignments[interaction.user]) or
            (self.board[0][1] == self.board[1][1] == self.board[2][1] == self.assignments[interaction.user]) or
            (self.board[0][2] == self.board[1][2] == self.board[2][2] == self.assignments[interaction.user]) or
            # Check diagonals
            (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.assignments[interaction.user]) or
            (self.board[0][2] == self.board[1][1] == self.board[2][0] == self.assignments[interaction.user])
        ):
            # await EDIT_VIEW_MESSAGE(self.message, 'Nicely done.', self)
            await INTERACTION(interaction.response, f"{interaction.user.mention} won the match.", False)
            self.toolate = False
            await self.on_timeout()
        elif (self.turns == 9):
            await INTERACTION(interaction.response, f"A draw! Lame.", False)
            await asyncio.sleep(1)
            await SEND(BUTTONS["channel"], "We'll settle this next time.")
            self.toolate = False
            await self.on_timeout()
        else:
            await interaction.response.defer()

    async def process_click(self, interaction, button, usr):
        if usr not in self.players:
            if len(self.players) == 2:
                await INTERACTION(interaction.response, "You are too late :bangbang:", True)
                return
            else:
                if len(self.players) == 0:
                    self.assignments[usr] = "X"
                else:
                    self.assignments[usr] = "O"

                self.players.append(usr)
        
        if usr == self.lastplayer:
            await INTERACTION(interaction.response, "You have already played this turn :interrobang:", True)
            return

        self.lastplayer = usr
        self.turns += 1
        self.letter = self.assignments[usr]

        if self.letter == "X":
            button.style = discord.ButtonStyle.blurple
        else:
            button.style = discord.ButtonStyle.green

        button.label = self.letter
        button.disabled = True

        await self.update_board(interaction, button)


    @discord.ui.button(label="?", row=0, custom_id = "1", style = discord.ButtonStyle.secondary)
    async def B1(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=0, custom_id = "2", style = discord.ButtonStyle.secondary)
    async def B2(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=0, custom_id = "3", style = discord.ButtonStyle.secondary)
    async def B3(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=1, custom_id = "4", style = discord.ButtonStyle.secondary)
    async def B4(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=1, custom_id = "5", style = discord.ButtonStyle.secondary)
    async def B5(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=1, custom_id = "6", style = discord.ButtonStyle.secondary)
    async def B6(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=2, custom_id = "7", style = discord.ButtonStyle.secondary)
    async def B7(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=2, custom_id = "8", style = discord.ButtonStyle.secondary)
    async def B8(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

    @discord.ui.button(label="?", row=2, custom_id = "9", style = discord.ButtonStyle.secondary)
    async def B9(self, interaction: discord.Interaction, button: discord.ui.Button):
        usr = interaction.user
        await self.process_click(interaction, button, usr)

class ButtonGames_ThrowingStuff(discord.ui.View):
    embed = None

    async def on_timeout(self):
        self.results = ""
        for key in self.votes.keys():
            for user in self.votes[key]:
                if len(self.users) > 1:
                    self.results += '\n'

                if not self.custom:
                    self.results += f"**{user.display_name}** would {self.choices[int(key)]}".replace("yourself", "themselves").replace("your", "their").replace("Don't", "not").lower()
                else:
                    self.results += f"**{user.display_name}** voted for \"{self.choices[int(key)]}\"".replace("yourself", "themselves").replace("your", "their").replace("Don't", "not").lower()

        await self.update_message()

        for item in self.children:
            item.disabled = True


        self.closed = True
        await EDIT_VIEW_MESSAGE(self.message, f"{self.message.content}\nPoll is closed. Look at the results.", self)
        await self.stop()

    async def too_late(self):
        if self.closed == True:
            return

        if len(self.users) < 1:
            await REPLY(self.message, "No participation whatsoever.")
        elif len(self.users) == 1:
            await REPLY(self.message, "You spoke for everyone else.")
        else:
            await REPLY(self.message, "Very interesting choices.")

        await self.on_timeout()

    def create_embed(self):
        embed = discord.Embed()
        embed.title = "Poll results"
        embed.description = self.results
        embed.color = discord.Colour(int("FFD700", 16))

        self.embed = embed
        return embed
    
    async def update_message(self):
        await self.message.edit(embed=self.create_embed(), view=self)

    async def process_click(self, interaction, buttonId, usr):
        if (buttonId == "close"):
            if (usr == self.customUser):
                await interaction.response.defer()
                await self.too_late()
                return
            else:
                await INTERACTION(interaction.response, "Only the person who created the poll may close it.", True)
                return

        if (usr in self.users):
            await INTERACTION(interaction.response, "One vote only.", True)
            return
        
        self.users.append(usr)
        self.votes[buttonId].append(usr)
        self.results = ""

        for key in self.votes.keys():
            for user in self.votes[key]:
                if len(self.users) > 1:
                    self.results += '\n'
                self.results += f"Someone would..."

        if self.custom:
            self.results = self.results.replace("would", "voted for")

        await self.update_message()
        await interaction.response.defer()

    # async def createButtons(self):
    #     @discord.ui.button(label=self.choice1, custom_id = "0", style = discord.ButtonStyle.secondary)
    #     async def B1(self, interaction: discord.Interaction, button: discord.ui.Button):
    #         usr = interaction.user
    #         await self.process_click(interaction, button, usr)

    #     @discord.ui.button(label=self.choice2, custom_id = "1", style = discord.ButtonStyle.secondary)
    #     async def B2(self, interaction: discord.Interaction, button: discord.ui.Button):
    #         usr = interaction.user
    #         await self.process_click(interaction, button, usr)

    #     @discord.ui.button(label=self.choice3, custom_id = "2", style = discord.ButtonStyle.secondary)
    #     async def B3(self, interaction: discord.Interaction, button: discord.ui.Button):
    #         usr = interaction.user
    #         await self.process_click(interaction, button, usr)

    #     @discord.ui.button(label=self.choice4, custom_id = "3", style = discord.ButtonStyle.secondary)
    #     async def B4(self, interaction: discord.Interaction, button: discord.ui.Button):
    #         usr = interaction.user
    #         await self.process_click(interaction, button, usr)
        
    #     await self.createButtons()

class Minigames_Hangman(discord.ui.View):
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await EDIT_VIEW_MESSAGE(self.message, f"The hangman's fate is sealed.\n\n`{self.current}`\n\n{self.status}", self)

    async def too_late(self):
        if self.toolate:
            await SEND(BUTTONS["channel"], f"Time's up, the answer was: `{str(self.myword)}`.")

        await self.on_timeout()

    async def update_revealed(self, interaction, button):
        self.current = ""
        for i in self.myword:
            if str(i).lower() in self.revealed:
                self.current += str(i).upper()
            else:
                if str(i) != " ":
                    self.current += "-"
                else:
                    self.current += " "

        await EDIT_VIEW_MESSAGE(self.message, f"Keep it going!\n\n`{self.current}`\n\n{self.status}\n\nWrong letters used so far: `{self.wrong}`\n\nLast move: {self.cp.mention} guessed `{self.cl}`", self)

        if "-" not in self.current:
            # best_user = max(self.players, key=lambda user: len(self.players[user]))
            max_length = max(len(guesses) for guesses in self.players.values())
            best_users = [user.mention for user, letters in self.players.items() if len(letters) == max_length]
            best_users_ids = [user.id for user, letters in self.players.items() if len(letters) == max_length]

            for plr in self.players.keys():
                self.results += f"`{plr.display_name}`: {len(self.players[plr])}\n"

            await INTERACTION(interaction.response, f"Special thanks to: {', '.join(best_users)}\n\n{self.results}", False)

            if len(self.myword) >= 5 and self.lifes == 5 and self.alone:
                # for usrId in best_users_ids:
                if not str(self.cp.id) in list_decoded_entries("Sleazel Saviour"):
                    await add_entry_with_check("Sleazel Saviour", self.cp)

                await asyncio.sleep(1)
                await SEND(BUTTONS["channel"], "It looks like no mistakes were made this round, I'm sure Sleazel can sleep peacefully at night with you around.")

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

        await EDIT_VIEW_MESSAGE(self.message, f"How reckless.\n\n`{self.current}`\n\n{self.status}\n\nWrong letters used so far: `{self.wrong}`\n\nLast move: {self.cp.mention} guessed `{self.cl}`", self) 

        if self.lifes <= 0:
            await INTERACTION(interaction.response, f"{interaction.user.mention} is wrong. The correct word was: `{self.myword}`", False)
            self.toolate = False
            self.stop()
        else:
            await interaction.response.defer()

    async def process_click(self, interaction, button, usr):

        if self.alone:
            if usr != self.cp:
                await INTERACTION(interaction.response, "This user is playing solo.", True)
                return
        else:
            if usr == self.cp:
                await INTERACTION(interaction.response, "It's someone else's turn now.", True)
                return
            elif self.picker != None and usr == self.picker:
                await INTERACTION(interaction.response, "You do not deserve this victory.", True)
                return
            else:
                self.cp = usr

        self.cl = str(button.custom_id).upper()

        if usr not in self.players.keys():
            self.players[usr] = []

        if str(button.custom_id).lower() in self.myword:
            button.style = discord.ButtonStyle.green
            button.disabled = True
            self.revealed.append(str(button.custom_id).lower())

            self.players[usr].append(str(button.custom_id).upper())

            await self.update_revealed(interaction, button)
        else:
            self.lifes -= 1

            button.style = discord.ButtonStyle.secondary

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

# class BurgerButton(discord.ui.View):
#     async def on_timeout(self):
#         for item in self.children:
#             item.disabled = True

#         await EDIT_VIEW_MESSAGE(self.message, 'The burger is dead D:', self)

#     async def too_late(self):
#         if self.toolate:
#             await SEND(BUTTONS['channel'], 'burger over')

#         await self.on_timeout()

#     @discord.ui.button(label="🍔", style = discord.ButtonStyle.blurple)
#     async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await INTERACTION(interaction.response, "🍔", True)

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

# class ThirdButton(discord.ui.View):
#     async def on_timeout(self):
#         for item in self.children:
#             item.disabled = True
#             if not len(self.users) <= 1:
#                 item.label = f"{self.winning.name} was here"
#                 await EDIT_VIEW_MESSAGE(self.message, "Not my button anymore.", self)
#             else:
#                 item.label = "Still my button"
#                 item.style = discord.ButtonStyle.red
#                 await EDIT_VIEW_MESSAGE(self.message, "I get to keep my button.", self)

#     async def too_late(self):
#         if len(self.users) <= 1:
#             await SEND(BUTTONS["channel"], "Thank you very much.")
#         else:
#             await SEND(BUTTONS["channel"], f"{self.winning.mention} stole my button after `{self.clicks}` interactions.")

#             if not str(self.winning.id) in list_decoded_entries("Last One"):
#                 await add_entry_with_check("Last One", self.winning)

#         await self.on_timeout()

#     @discord.ui.button(label="Broken Drone button", style = discord.ButtonStyle.secondary)
#     async def pressed(self, interaction: discord.Interaction, button: discord.ui.Button):
#         usr = interaction.user

#         if usr not in self.users:
#             self.users.append(usr)

#         if self.clicks >= 150:
#             self.step = 2
#             self.timeout = 5
#             self.tm = 5
#         elif self.clicks >= 100:
#             self.step = 1
#             self.timeout = 15
#             self.tm = 15

#         if usr == self.winning:
#             await INTERACTION(interaction.response, "The button is yours.", True)
#             await EDIT_VIEW_MESSAGE(self.message, BUTTONS["phase3again"][self.step].format(mention = usr.name, time = round(time.time() + self.tm)), self)
#         else:
#             button.label = f"{usr.name} button"
#             button.style = discord.ButtonStyle.green
#             self.winning = usr
#             self.clicks += 1
#             await EDIT_VIEW_MESSAGE(self.message, BUTTONS["phase3new"][self.step].format(mention = usr.name, time = round(time.time() + self.tm)), self)
#             await interaction.response.defer()