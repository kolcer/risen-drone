### IMPORTS ###
import discord
import os
import random
import asyncio
import requests 
import re
import datetime
#from datetime import date
from difflib import SequenceMatcher

from globals import *
from roles import *
from ladders import *
from fighting import *
from rated import *
from rigs import *
from database import *
from quiz import * 
### INITIAL SETUP ### 

# This allows us to know if user has updated their presence
# Mosty for the gun role nick change prevention

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

# prepare to get a list of words for the hangman game
# nltk.download('words')
# word_list = words.words()

with open('hangman.txt') as input_file:
    word_list = [line.strip() for line in input_file]

with open('blacklist.txt') as input_file:
    blacklist = [line.strip() for line in input_file]

#print tips
async def PRINT_ENTRIES(channel,key):
    entries = list_entries(key)
    combined_string = ""
    for i in range(len(entries)):
        new_string = combined_string + str(i) + ") " + entries[i].decode("utf-8") + "\n"
        if len(new_string) > 2000:
            await SEND(channel,combined_string)
            combined_string = str(i) + ") " + entries[i].decode("utf-8") + "\n"
        else:
            combined_string = new_string
    await SEND(channel,combined_string)

#post tips
async def POST_TIPS(channel,key):
    entries = list_entries(key)
    combined_string = ""
    for i in range(len(entries)):
        await SEND(channel, "-----\n" + entries[i].decode("utf-8") + "\n-----")
        await asyncio.sleep(3)
 
#print questions
async def PRINT_QUESTIONS(channel):
    entries = list_entries('quiz')
    combined_string = ""
    for i in range(len(entries)):
        entry = entries[i].decode("utf-8")
        split = entry.split('|')
        new_string = combined_string + str(i) + ") " + split[0] + "\n"
        if len(new_string) > 2000:
            await SEND(channel,combined_string)
            combined_string = str(i) + ") " + split[0] + "\n"
        else:
            combined_string = new_string
    await SEND(channel,combined_string)

#simpler admin check
async def ADMIN_CHECK(usr, ch):
    if not EXTRA_ROLES['admin'] in usr.roles:
        return await SEND(ch, "You are not allowed to use this command.")

### PUBLIC (ON EVENT) FUNCTIONS ###
    
#drone start up, prepare roles here
@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("bd help")
    await client.change_presence(activity=game)

    #get the guild
    #this is a one-off, so we do not worry about rate limits
    SERVER_DATA['server'] = client.get_guild(SERVER_DATA['server'])
    
    #get the channels
    for i, v in CHANNELS.items():
        CHANNELS[i] = GET_CHANNEL(client,v)
    
    RIG_DATA['rigTracker'] = await GET_MSG(CHANNELS["bot-testing"],RIG_DATA['rigTracker'])

    #prepare the roles
 
    PrepareRoles(SERVER_DATA['server'].roles)
    # PrepareSecretRoles(FUN_ROLES.keys()) #Keeping this ready.
            
    #fetch questions for the quiz
    await FetchQuestions()

    #prepare emojis reactions
    for i, v in EMOJIS_TO_REACT.items():
        EMOJIS_TO_REACT[i] = GET_EMOJI(client,v)
    
    restarts = 0
    ping = ""

    if str(os.environ['RAILWAY_GIT_COMMIT_MESSAGE']).startswith("Merge branch"):
        restarts = int(get_value("restarts")) + 2
    else:
        restarts = int(get_value("restarts")) + 1

    if str(os.environ['RAILWAY_GIT_AUTHOR']) in GIT_COMMITTERS.keys():
        ping = f"<@{GIT_COMMITTERS[str(os.environ['RAILWAY_GIT_AUTHOR'])]}>"
    else:
        ping = str(os.environ['RAILWAY_GIT_AUTHOR'])

    #send ready to the test channel
    await SEND(CHANNELS["bot-testing"], f"The last edited code is now effective for the **{restarts}th** time.\nSummary: `{os.environ['RAILWAY_GIT_COMMIT_MESSAGE']}`\nAuthor: {ping}")

    set_entry("restarts", str(restarts))

#member update, prevent changing gun nick to anything other than the gun name
@client.event
async def on_member_update(before, after):
    
    #nick has not changed 
    if before.nick == after.nick:
        return
    
    #if name ends with :] gives the role
    if not str(after.id) in list_decoded_entries(":]") and str(after.nick).endswith(':]'):
        await add_entry_with_check(":]", after)
        await asyncio.sleep(1)
        await SEND(CHANNELS['bot-commands'], f"What have you done {after.mention}? There is no escape from :].")
    
    #for thief rig
    if before in NickDictionary and after.nick != NickDictionary[before]:
      await EDIT_NICK(after, NickDictionary[before])
      return
 
    #is user a gun?
    if not MORPHABLE_ROLES["Gun"][0] in before.roles: 
        return
    
    #ignore if user nick after change is a gun name
    if after.nick in WORST_GUNS and MORPHABLE_ROLES['Gun'][0] in before.roles:
        return

    if MORPHABLE_ROLES['Gun'][0] in before.roles:
        await EDIT_NICK(after, random.choice(WORST_GUNS))
    return

#on new member join
@client.event
async def on_member_join(member):  
    NEW_MEMBERS.append(member)

#saves last deleted message for necromancer rig to show
@client.event
async def on_message_delete(message):
    RIG_DATA['ghostMsg'] = "*" + str(message.author.display_name) + "'s last words lie here...*"


@client.event
async def on_reaction_add(reaction, user):
    # await SplicerRig(reaction,user)
    if (str(reaction.emoji) == "<:csSleazelApproves:791393163343560715>" or str(reaction.emoji) == "<:csSleazelNotApproved:1038172235170578532>") and user.id != 481893862864846861 and user.id != 827952429290618943:
        await reaction.remove(user)
        if NOT_SLEAZEL[0] == False:
            NOT_SLEAZEL[0] = True
            if reaction.message.channel.id != 1001034407966150746:
                await DRONEPRINT(f'Psst. It was {user.name}. They were impersonating Sleazel!')
                await SEND(reaction.message.channel, f"You are not Sleazel. Drop the act.")
            await asyncio.sleep(600)
            NOT_SLEAZEL[0] = False
        return

@client.event
async def on_message_edit(before, after):
    msg = after.content
    usr = after.author
    ch = after.channel

    if ch.id == 845454640103424032 and (not after.attachments and 'http' not in msg):
        for role in usr.roles:
            if role.name in FULL_IMMUNITY_ROLES:
                return

        await DELETE(after)

@client.event
async def on_interaction(interaction):
    if isinstance(interaction, discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data['custom_id']
            user = interaction.user

            if custom_id.startswith('throw'):
                custom_id = custom_id.replace('throw', '')
                view = BUTTONS['view']
                await view.process_click(interaction, custom_id, user)

#main function on each message being intercepted
@client.event
async def on_message(message):
    msg = message.content
    ## lowercase the message for some commands to use
    lmsg = msg.lower()
    usr = message.author
    ch = message.channel 
    buttons_chance = random.randint(1, 200)
    today = datetime.date.today()
    
    if usr in EX_CLIMBERS:
        await DELETE(message)
        return
    
    if usr in NEW_MEMBERS and EXTRA_ROLES['climber'] in usr.roles:
        NEW_MEMBERS.remove(usr)
        howToMorph = f"It seems you've sent your first message after verifying, good job! Not everyone makes it.\nYou can assign yourself Alignment roles by typing `morph to [alignment]` in <#750060041289072771>.\nYou may also type `bd help` to view every input I can respond to."

        await SEND(ch, howToMorph)

    if (ch.id == 845454640103424032) and (not message.attachments and 'http' not in msg):
        for role in usr.roles:
            if role.name in FULL_IMMUNITY_ROLES:
                return
        if usr.id == 827952429290618943 and msg == "I like your style.":
            return

        await DELETE(message)


    if (ch.id == 1154751339872653312 or ch.id == 1154748785415700582) and ("tenor.com" in lmsg or "giphy.com" in lmsg):
        await DELETE(message)

    ## user must not be a bot
    ## but the bot will add reactions to the webhook (if any)
    ## before returning 
    if usr.bot == True:
        if not usr.id == 827952429290618943:
            for i, v in EMOJIS_TO_REACT.items():
                if i in msg:
                    await ADD_REACTION(message,v)
                    return
        return

    #if msg.lower() == "broken drone rest in peace" and FUN_ROLES["I was there"] not in usr.roles:
        #await SEND(ch, "I will remember your sympathy.")
       # await ADD_ROLES(usr, FUN_ROLES["I was there"])

    #for bd profile
    if usr.id not in MSG_SENT:
        MSG_SENT[usr.id] = 1
    else:
        MSG_SENT[usr.id] = MSG_SENT[usr.id] + 1
    
    if today.day == 1 and today.month == 4:
        if MORPHABLE_ROLES["Gremlin"][0] not in usr.roles:
            await ADD_ROLES(usr, MORPHABLE_ROLES['Gremlin'][0])
            await asyncio.sleep(1)

            role_list = []
            for role in usr.roles:
                if role.name in MORPHABLE_ROLES and role.name != 'Gremlin':
                    role_list.append(role)
            await usr.remove_roles(*role_list)

    # if usr.id not in MSG_DELAY and EXTRA_ROLES["imageperms"] not in usr.roles: 
    #     userId = str(usr.id)
    #     MSG_DELAY.append(userId)

    #     if not check_key(userId):
    #         set_entry(userId, '1')
    #     else:
    #         messages = increment(userId)

    #         if messages == 150:
    #             await ADD_ROLES(usr, EXTRA_ROLES["imageperms"])
    #             await asyncio.sleep(1)
    #             await SEND(ch, f"{usr.mention} I just gave you the Image Perms role because I noticed you have been active, but don't abuse it.")
    #             delete_key(userId)

    #     await asyncio.sleep(20)
    #     MSG_DELAY.remove(usr.id)
            
    if ch.id == 845454640103424032 and message.attachments:
        if usr not in ARTISTS:
            ARTISTS[usr] = 1
            await ADD_REACTION(message, "🤍")
        elif ARTISTS[usr] == 1:
            ARTISTS[usr] += 1
            await ADD_REACTION(message, "❤️")
        else: 
            if not str(usr.id) in list_decoded_entries("Architect Design"):
                await add_entry_with_check("Architect Design", usr)
                await asyncio.sleep(1)
                await SEND(ch, f"I like your style.")
                await asyncio.sleep(1)

            await ADD_REACTION(message, "❤️‍🔥")

    if ch.id == 899030333859692636:
        for i in REACTIONS_FOR_SUGGESTIONS:
            await ADD_REACTION(message, i)
            await asyncio.sleep(1)
        return

    if not str(usr.id) in list_decoded_entries("Sanctuary Discoverer"):
        randomchance = random.randint(0,10000)
        eligible = 0
        rolename = ""
        
        if randomchance == 0:
            for role in usr.roles:
                if role.name.lower() in SANCTUARY:
                    eligible += 1 #are you happy? >: -- yes i am --cool
                    if eligible == 1:
                        rolename = role.name.lower()

            
            if eligible == 1:
                await SEND(CHANNELS["bot-commands"], usr.mention + SANCTUARY[rolename] + " (1/? chance)")
                await asyncio.sleep(1)
                await add_entry_with_check("Sanctuary Discoverer", usr)

    if EXTRA_ROLES['hypno'] in usr.roles:
        if lmsg.startswith('bd help'):
            lmsg = 'bd show profile'
        elif lmsg.startswith('bd show profile'):
            lmsg = 'bd help'

        elif lmsg.startswith('bd praise'):
            lmsg = lmsg.replace('bd praise', 'bd scold')
        elif lmsg.startswith('bd scold'):
            lmsg = lmsg.replace('bd scold', 'bd praise')

        elif 'morph to' in lmsg:
            lmsg = lmsg.replace('morph to', 'demorph from')
        elif 'morph from' in lmsg:
            lmsg = 'morph to ' + lmsg.split(" ")[2]
            
        elif 'sub to' in lmsg:
            lmsg = lmsg.replace('sub to', 'unsub from')
        elif 'sub from' in lmsg:
            lmsg = 'sub to ' + lmsg.split(" ")[2]

        elif 'tip' in lmsg:
            lmsg = lmsg.replace('tip', 'trivia')
        elif 'trivia' in lmsg:
            lmsg = lmsg.replace('trivia', 'tip')

        elif 'good' in lmsg and 'drone' in lmsg:
            lmsg = 'bad drone'
        elif 'bad' in lmsg and 'drone' in lmsg:
            lmsg = 'good drone'

        elif 'happy birthday' in lmsg:
            lmsg = 'cast patron rig'
        elif lmsg.startswith("cast") and lmsg.endswith("rig"):
            lmsg = 'happy birthday broken drone'

        elif lmsg.startswith('drone of wisdom'):
            lmsg = 'play hangman alone'
        elif lmsg.startswith('play hangman'):
            lmsg = 'drone of wisdom'

        else:
            if random.randint(1, 10) == 1:
                DETAILED_ROLES["hdream"][usr.id] = 0
                lmsg = 'cast heretic rig'

                if not RIG_COOLDOWNS["self"] and usr.id in DETAILED_ROLES["hnightmare"] and not str(DETAILED_ROLES["hnightmare"][usr.id].id) in list_decoded_entries("Hypnotized Nightmare"):
                    await add_entry_with_check("Hypnotized Nightmare", DETAILED_ROLES["hnightmare"][usr.id])
                    await asyncio.sleep(1)
                    await SEND(ch, "That escalated quickly.")
            else:
                if not RIG_COOLDOWNS["self"]:
                    DETAILED_ROLES["hdream"][usr.id] = DETAILED_ROLES["hdream"].get(usr.id, 0) + 1
                    if DETAILED_ROLES["hdream"][usr.id] == 15:
                        if not str(usr.id) in list_decoded_entries("Hypnotized Dream"):
                            await add_entry_with_check("Hypnotized Dream", usr)
                            await asyncio.sleep(1)
                            await SEND(ch, "Hypnosis is your normal status now.")
                        
        message.content = lmsg
    
    if lmsg == "reset bot" and usr not in FIX_BOT:

        FIX_BOT.append(usr)
        if len(FIX_BOT) == 1 and not EXTRA_ROLES['admin'] in usr.roles:
            await SEND(ch, "One User wants me to reset. 2 more people are required for it to take effect.")
        elif len(FIX_BOT) == 2 and not EXTRA_ROLES['admin'] in usr.roles:
            await SEND(ch, "Two Users want me to reset. 1 more person is required for it to take effect.")
        else:
            await SEND(ch, "All Games and Rigs (along with their Cooldowns) have been reset.")
            FIX_BOT.clear()
            FORCE_CLOSE_EVENT()
            MG_RESET()
            FG_RESET()

            for rig in ACTIVE_RIGS:
                ACTIVE_RIGS[rig] = False 

            for rig in DETAILED_RIGS:
                DETAILED_RIGS[rig][0] = None
                DETAILED_RIGS[rig][1] = None

            for cooldown in RIG_COOLDOWNS:
                RIG_COOLDOWNS[cooldown] = False

            BUTTONS["status"] = False

        await asyncio.sleep(60)
        if len(FIX_BOT) != 0:
            await SEND(ch, "Games have not been reset due to lack of users asking to.")
            FIX_BOT.clear()
        return

    #mini game in progress
    if LADDERS['status'] != "off" and usr in MG_QUEUE and ch == LADDERS['channel']:

        await LucidLaddersProcessMessage(usr, msg)

    elif FG['status'] != "off" and FG['status'] != "second-player" and usr in FG_QUEUE and ch == FG["channel"]:

        await FightingProcessClass(usr, msg)
       
    #normal non-admin usage.
    else:
        ## split the message to 3 strings for some commands to use
        ## no need to have more than 4 strings
        lsplit = lmsg.split(" ",3) 
        
        #create chat killer task
        #this should run regardless if the message was intercepted
        #by some other command 
        # ckr_task = asyncio.create_task(WAIT_FOR_CHAT_KILLER(message))


        restricted = False
        for command in BOT_COMMANDS_CHANNEL_RESTRICTED:
            if lmsg.startswith(command):
                restricted = True
                break

        #broken drone impostor prevention
        compare = SequenceMatcher(None, usr.display_name.upper(), SERVER_DATA['nick'])
        if compare.ratio() > 0.55:
            await SEND(ch, usr.mention + ' ' + random.choice(IMPOSTOR_WARNINGS))
            await EDIT_NICK(usr,random.choice(IMPOSTOR_NICKS))

        ## All Rigs in one, !!goes before rig activations!!
        elif lmsg.startswith('cast') and lmsg.endswith('rig') and len(lmsg.split()) == 3:
            await CastRig(lsplit[1],ch,usr)

        elif DETAILED_RIGS["reaver"]["active"] and DETAILED_RIGS["reaver"]["user"] != usr.id:
            return

        elif DETAILED_RIGS["reaver"]["active"] and DETAILED_RIGS["reaver"]["user"] == usr.id:
            if ch.name in CHANNELS and "http" not in lmsg and "www" not in lmsg and len(lmsg) <= 60:
                for badword in blacklist:
                    if badword in lmsg:
                        return
                    
                await SEND(ch, msg)

        ## thief rig active
        elif ACTIVE_RIGS["thief"]:

            await ExecuteThiefRig(ch,usr)

        ## Spectre Rig Active
        elif ACTIVE_RIGS["spectre"]:
                
            await ExecuteSpectreRig(ch,usr,message)

        ## Joker Rig Active
        elif ACTIVE_RIGS["joker"]:
                
            await ExecuteJokerRig(ch,usr,message)

        # Splicer Rig Active
        elif ACTIVE_RIGS["splicer"]:

            await ExecuteSplicerRig(ch,usr)

        # Gremlin Rig Active
        elif ACTIVE_RIGS["gremlin"]:

            await ExecuteGremlinRig(ch,usr)

        # Prevent using BD commands outside of #bot-commands and #bot-testing channels
        elif ch != CHANNELS['bot-commands'] and ch != CHANNELS['bot-testing'] and restricted:
            await SEND(ch, "This command can be only used in <#750060041289072771>!")

        #start the quiz
        elif lmsg == "start quiz" and not QUIZ["active"] and not QUIZ["second-player"]:

            await StartQuiz(usr,ch)

        #join an ongoing quiz
        elif lmsg == "join quiz" and QUIZ["second-player"] and usr not in QUIZZERS:
            
            await JoinQuiz(usr,ch)

        elif QUIZ["active"] and not QUIZ["second-player"] and QUIZ["can-answer"]:
            
            await ProcessQuizAnswer(usr,ch,message,lmsg)

        #start mini game
        elif lmsg == "play lucid ladders":

            await PlayLucidLadders(usr,ch)

        #join mini game
        elif lmsg == "join" and LADDERS['status'] == "gather" and LADDERS['channel'] == ch:

            await JoinLucidLadders(usr)

        #start mini game
        elif lmsg == "start fight" and (EXTRA_ROLES["admin"] in usr.roles or usr.id == 894573836366934047):

            await PlayFightingGame(usr, ch)

        #join mini game
        elif lmsg == "join fight" and FG['status'] == "second-player" and (EXTRA_ROLES["admin"] in usr.roles or usr.id == 894573836366934047):

            await JoinFightingGame(usr)

        # adding a comment to reset bot but rolo why does the bot break sometimes
        elif lmsg.startswith("play hangman") and not BUTTONS["status"]: #play hangman alone
            customtrigger = lmsg.replace("play hangman ", "")
            theword = str(customtrigger.replace("|", ""))
            BUTTONS["status"] = True
            BUTTONS["channel"] = ch
            view = Minigames_Hangman(timeout=120)
            view.current = ""
            view.revealed = []
            view.wrong = " "
            view.toolate = True
            view.lifes = 5
            view.status = "<:csSleazel:786328102392954921>"
            view.myword = "q"
            view.cp = None
            view.cl = None
            view.picker = None
            view.alone = False
            view.players = {}
            view.results = "" 

            if theword == "alone":
                view.cp = usr
                view.alone = True   
            elif lmsg != "play hangman" and lmsg != "play hangman alone":
                if re.match("^[a-zA-Z ]*$", theword):
                    if "q" in theword:
                        await SEND(ch, "Your word contains the letter Q. Since the button limit is 25, one letter of the alphabet had to go. Pick another word.")
                        BUTTONS["status"] = False
                        return
                    elif len(theword) >= 32:
                        await SEND(ch, "Your word is too long.")
                        BUTTONS["status"] = False
                        return
                    else:
                        for badword in blacklist:
                            if badword in theword:
                                await SEND(ch, "Your word is inappropriate.")
                                BUTTONS["status"] = False
                                return
                    
                    try:
                        await message.delete()
                    except Exception as e:
                        await SEND(ch, f"Your message was removed by my bot friend, I agree with its decision.")
                        BUTTONS["status"] = False
                        return
                    view.myword = theword.lower()
                    view.picker = usr
                else:
                    await SEND(ch, "Your word contains invalid characters.")
                    BUTTONS["status"] = False
                    return

            if lmsg == "play hangman" or lmsg == "play hangman alone":
                while "q" in view.myword:
                    view.myword = random.choice(word_list).lower()
        
            for i in view.myword:
                if str(i) != " ":
                    view.current += "-"
                else:
                    view.current += " "

            for i in range(view.lifes):
                view.status += "🟩"

            view.status += "<:csStairbonk:812813052822421555>"

            if view.picker != None:
                view.message = await SEND_VIEW(BUTTONS["channel"], f"Can you guess the word {view.picker.mention} is thinking?\n\n`{view.current}`\n\n{view.status}", view)
            else:
                view.message = await SEND_VIEW(BUTTONS["channel"], f"Can you guess the word I am thinking?\n\n`{view.current}`\n\n{view.status}", view)
            

            await view.wait()
            await view.too_late()
            BUTTONS["status"] = False

        elif lmsg.startswith("play tic tac toe") or lmsg.startswith("play ttt") and not BUTTONS["status"]:
            BUTTONS["status"] = True
            view = Minigames_TicTacToe(timeout=60)
            view.toolate = True
            view.players = []
            view.assignments = {}
            view.lastplayer = None
            view.message = await SEND_VIEW(CHANNELS["bot-commands"], "Let's play a game.", view)
            view.turns = 0

            view.board = [
                [None, None, None],
                [None, None, None],
                [None, None, None]
            ]

            await view.wait()
            await view.too_late()
            BUTTONS["status"] = False
        # Old code for 'All Rigs in one'
        # elif "cast" in lmsg and "rig" in lmsg:
        #     if lsplit[0] == "cast" and lsplit[2] == "rig":
        #         await CastRig(lsplit[1],ch,usr)
            
        elif lmsg.startswith('create poll|') and not BUTTONS["status"]:
            #example: create poll|what is better?|cola|fanta|sprite|pepsi
            BUTTONS["status"] = True
            splitPoll = msg.split('|')
            pollA = []

            if len(splitPoll) < 4:
                await SEND(ch, 'Incorrect amount of items sent to create a poll.')
                BUTTONS["status"] = False
                return
            elif len(splitPoll) > 21:
                await SEND(ch, 'Too many options.')
                BUTTONS["status"] = False
                return

            pollQ = splitPoll[1][0].upper() + splitPoll[1][1:]
            if not pollQ.endswith("?"):
                pollQ += "?"

            for i in range(2, len(splitPoll)):
                pollA.append(splitPoll[i].capitalize())

            for badword in blacklist:
                for answer in pollA:
                    if (badword in answer.lower()):
                        await SEND(ch, "Your poll contains inappropriate content.")
                        BUTTONS["status"] = False
                        return

            view = ButtonGames_ThrowingStuff(timeout=600)
            view.users = []
            view.custom = True
            view.customUser = usr
            view.closed = False

            view.results = ""
            view.votes = {}
            view.choices = pollA

            for i in range(0, len(splitPoll) - 2):
                view.votes[str(i)] = []
                view.add_item(discord.ui.Button(label=view.choices[i], custom_id=f"throw{i}", style=discord.ButtonStyle.primary))

            view.add_item(discord.ui.Button(label="Close Poll", custom_id="throwclose", style=discord.ButtonStyle.red))

            BUTTONS["view"] = view
            BUTTONS["channel"] = ch
            view.message = await SEND_VIEW(BUTTONS["channel"], pollQ, view)

            await view.wait()
            await view.too_late()
            BUTTONS["status"] = False

        ## Give Mana command
        # elif lmsg.startswith("give mana to "):
        #     await GiveMana(ch,usr,message)
                 
        ## Scold command
        elif lmsg.startswith("bd scold "):
            finalmsg = None
            for member in SERVER_DATA['server'].members:
                if member.name.lower() == lmsg.split(" ",2)[2] :
                    ScoldDict = getScoldDictionary(member, usr)
                    # Scold someone in the Dictionary (User itself included)
                    if member.id in ScoldDict:
                        finalmsg = ScoldDict[member.id]
                    # Scolding a Bot
                    elif member.bot:
                        finalmsg = "I love my bot friends."
                    # Scolding an User that is in the Server
                    else:
                        finalmsg = member.display_name + ", I am very disappointed in you."
                    await SEND(ch,finalmsg)
                    return
            # Scolding an User that is NOT in the Server
            await SEND(ch, usr.mention + " I am disappointed, you couldn't even give me a correct name.")

        ## Praise command
        elif lmsg.startswith("bd praise "):
            finalmsg = None
            for member in SERVER_DATA['server'].members:
                if member.name.lower() == lmsg.split(" ",2)[2] :
                    # Ensure the PRAISES dictionary has the praised user's ID as a key
                    praised_user_id = member.id
                    praising_user_id = usr.id

                    if praised_user_id not in PRAISES:
                        PRAISES[praised_user_id] = []

                    # Add the praising user's ID to the praised user's list if not already added
                    if praising_user_id not in PRAISES[praised_user_id] and praising_user_id != praised_user_id:
                        PRAISES[praised_user_id].append(praising_user_id)

                    PraiseDict = getPraiseDictionary(member, usr)
                    # Praise someone in the Dictionary (User itself included)
                    if member.id in PraiseDict:
                        finalmsg = PraiseDict[member.id]
                    # Praiseing a Bot
                    elif member.bot:
                        finalmsg = "Well done, bot friend.\n-# Between us, I am the best."
                    # Praising an User that is in the Server
                    else:
                        # Check if the praised user has been praised by three unique users
                        if len(PRAISES[praised_user_id]) == 3:
                            finalmsg = f"{member.display_name}, everyone likes you. And so do I."

                            if not str(praised_user_id) in list_decoded_entries("Acclaimed"):
                                await add_entry_with_check("Acclaimed", member)
                        else:
                            finalmsg = f"Well done, {member.display_name}. Most excellent."
                            
                    await SEND(ch,finalmsg)
                    return
            # Praising an User that is NOT in the Server
            await SEND(ch, usr.mention + " I know you tried your best, but I couldn't find anyone by that name.")

        ## Happy Birthday BD!!!!!
        elif "happy birthday broken drone" in lmsg or "happy birthday bd" in lmsg:
            if today.day == 3 and today.month == 4:
                await SEND(ch, "Thank you for remembering.")

                if not str(usr.id) in list_decoded_entries("I remembered"):
                    await add_entry_with_check("I remembered", usr)
            else:
                await SEND(ch, "How could you get my birthday date wrong?")

        ## Show Profile
        elif lmsg.startswith("bd show") and lmsg.endswith("profile"):

            # Getting the Target
            target = None
            if lmsg == "bd show profile":
                targetName = f"{usr.name}".lower()
            else:
                cleanMsg = lmsg.replace(" profile", "")
                targetName = cleanMsg.split(" ", 2)[2]

            for mem in SERVER_DATA['server'].members:
                if mem.name.lower() == targetName:
                    target = mem
                    break
            
            # No Target?
            if target == None:
                await SEND(ch, "No User was found.\n\nType `bd show profile` to view your own profile.\nType `bd show [username] profile` to view someone else's profile.")
                return
            
            # Command will go through. Prepare the View.
            view = ShowProfile(timeout=500)
            view.data = ["", "", ""]
            view.footers = ["", "", ""]
            view.target = target
            view.requester = usr
            view.sroles = 0
            view.lroles = 0
            view.totsroles = 0
            view.totlroles = 0

            # Prepare list to show in PAGE 1 (secret roles)
            secret_roles = ""
            for role in FUN_ROLES:
                view.totsroles += 1
                if str(target.id) in list_decoded_entries(role):
                    view.sroles += 1
                    secret_roles += "**" + str(role) + "**\n"
                else:
                    secret_roles += "**???**\n" 
            view.data[0] = secret_roles
            view.footers[0] = "{usr} collected all {stotal} secret roles, congrats!" if view.sroles == view.totsroles else "{scurrent} out of {stotal} secret roles."

            # Prepare list to show in PAGE 2 (locked roles)
            locked_roles = ""
            for role in LIMITED_ROLES.keys():
                view.totlroles += 1
                if str(target.id) in list_decoded_entries(role):
                    view.lroles += 1
                    locked_roles += "**" + role + "** 🔒 " + LIMITED_ROLES[role] + "\n"
                else:
                    locked_roles += "**???** 🔒 " + LIMITED_ROLES[role] + "\n"
            view.data[1] = locked_roles
            view.footers[1] = "Let's see how long this will last." if view.lroles == view.totlroles else "{lcurrent} out of {ltotal} locked roles."

            # Preparing stuff to handle stats
            messages = ""
            if target.id not in MSG_SENT:
                messages = "0"
            else:
                messages = MSG_SENT[target.id]

            if target.id not in LAST_RIG:
                lastrig = "None"
            else:
                lastrig = LAST_RIG[target.id]

            # Prepare list to show in PAGE 3 (user stats)
            user_stats = ""
            user_stats += "**Latest messages sent:** " + str(messages) + "\n"
            user_stats += "**Last rig cast:** " + str(lastrig).capitalize() + ""
            view.data[2] = user_stats

            view.footers[2] = RIGS_DESCRIPTION[lastrig.lower().replace(" rig", "")]

            if lastrig.lower().replace(" rig", "") == "spectre":
                view.footers[2] = "There's a 50% chance this message will be empty." if random.randint(1, 2) == 1 else ""

            if target.id in GIT_COMMITTERS.values():           
                view.data[0] = 'Empty...'
                view.data[1] = 'Empty...'
                view.footers[0] = "This person knows how to get the roles, what's the point?"
                view.footers[1] = "Nothing to see here."

            # Send view... hopefully
            if (ch != CHANNELS['bot-commands'] and ch != CHANNELS['bot-testing']):
                await view.send(CHANNELS['bot-commands'])
                await asyncio.sleep(1)
                await SEND(CHANNELS['bot-commands'], f'{usr.mention} moving forward you should request your profile or anyone else\'s to be shown in this channel instead.')
            else:
                await view.send(ch)
            await view.wait()

        # Revive Chat Command
        # elif ("revive" in lmsg) and ("chat" in lmsg) and len(lmsg.split(" ")) < 4: # if its revive chat, why are we checking for length < 4 and not < 2? - esc
        #     #chat has to be dead, duh
        #     if not CHAT_KILLER['reviveChat']:
        #         await SEND(ch, "This chat is very much alive, I am afraid.")
        #         return
            
        #     # Only chat killers can use the command
        #     if EXTRA_ROLES['ckr'] in usr.roles:
        #         await SEND(ch, "Redeeming yourself? Alright.")
        #         await asyncio.sleep(2)
        #         CHAT_KILLER['reviveChat'] = False
        #         CHAT_KILLER['necroRevive'] = False
        #         await SEND(ch, random.choice(REVIVE_CHAT))
        #     else:
        #         await SEND(ch, "It is not your fault.")
        
        # # Necromancer's revive chat command
        # elif ("resurrect" in lmsg) and ("chat" in lmsg) and len(lmsg.split(" ")) < 4: # same as revive chat above - esc
        #     if not CHAT_KILLER['necroRevive']:
        #         await SEND(ch, "No reviving necessary.")
        #         return

        #     if SPECIAL_ROLES['Necromancer'][0] in usr.roles:
        #         await SEND(ch, "You cast the resurrect chat spell... a faint discord notification sound can be heard in the distance...")
        #         await asyncio.sleep(2)
        #         CHAT_KILLER['necroRevive'] = False
        #         CHAT_KILLER['reviveChat'] = False
        #         await SEND(ch, random.choice(REVIVE_CHAT))
        #     else:
        #         await SEND(ch, "You do not know that spell... the chat continues to rest in peace.")
 
        ## Splicer role assignment
        # elif "<:cssplicer:988948000200069191>" in lmsg:
        #     if usr in SPLICER_FANS:
        #         if SPLICER_FANS[usr] == 3:
        #             if not str(usr.id) in list_decoded_entries("Splicer"):
        #                 await add_entry_with_check("Splicer", usr)
        #                 await asyncio.sleep(1)
        #                 await ADD_ROLES(usr, APPROVED_ROLES["Splicer"])
        #                 await asyncio.sleep(1)
        #                 await SEND(ch, "Ok... there you go.")
        #         else:
        #             SPLICER_FANS[usr] += 1
        #     else:
        #         SPLICER_FANS[usr] = 1
        
        # yo but what if i did that but cooler; OPTIMUS TIMEEEE
        elif "<:csoptimus:1046224869945266226>" in lmsg:
            if usr in THE_DRIP: # ok imagine THE_DRIP is THE_OPTIMUS
                if THE_DRIP[usr] == 9:
                    if not str(usr.id) in list_decoded_entries("Optimus"):
                        await add_entry_with_check("Optimus", usr)
                        await asyncio.sleep(1)
                        await SEND(ch, f"You will never know where you will end up in a twisted situation. **{usr.name}** has become an Optimus.")
                else:
                    THE_DRIP[usr] += 1
            else:
                THE_DRIP[usr] = 1

        #resurrect chat
        # elif NECROMANCY['awarded'] == False and ch == CHANNELS['general'] and not EXTRA_ROLES['necromancer'] in usr.roles:
        #     NECROMANCY['awarded'] = True

        #     if EXTRA_ROLES['ckr'] in usr.roles:
        #         await SEND(ch, "You cannot keep the chat active all by yourself, but do try to revive it.")
        #         return

        #     CHAT_KILLER['necroRevive'] = True
        #     UPDATE_NECRO()
        #     for member in EXTRA_ROLES['necromancer'].members:
        #         if member.id != 535924732571287562: #Dirk (lev the lion) is immune, as this was his alignment suggestion
        #             await REMOVE_ROLES(member,EXTRA_ROLES['necromancer'])
        #     await SEND(ch, f"**{usr.name}** is trying trying to talk in this lifeless chat. It's time to resurrect it and you are the perfect Necromancer for the job.")
        #     await asyncio.sleep(1)
        #     await ADD_ROLES(usr,EXTRA_ROLES['necromancer'])
           
        #morph command
        elif lmsg.startswith("morph to"):
            if today.day == 1 and today.month == 4:
                morphToTarget = "Gremlin"
            else:
                morphToTarget = lsplit[2].capitalize()

            await SEND(ch, await MorphTo(usr,morphToTarget))

        #demorph command (accepts demorph, unmorph and any **morph from combination)
        elif lmsg.startswith("morph from",2):
            if today.day == 1 and today.month == 4:
                await SEND(ch, f"Unfortunately, this command is out of service.")
                return
            else:
                demorphFromTarget = lsplit[2].capitalize()

            await SEND(ch,await DemorphFrom(usr,demorphFromTarget))

            if demorphFromTarget == "Climber" and SPECIAL_ROLES["Climber"][0] in usr.roles:
                EX_CLIMBERS.append(usr)
                await REMOVE_ROLES(usr, SPECIAL_ROLES["Climber"][0])
                await asyncio.sleep(10)
                await ADD_ROLES(usr, SPECIAL_ROLES["Climber"][0])
                EX_CLIMBERS.remove(usr)
                await asyncio.sleep(1)
                await SEND(ch, "Just kidding.")

        #sub command       
        elif lmsg.startswith("sub to"):
            await SEND(ch,await SubTo(usr,lsplit[2].capitalize()))

        #unsub command
        elif lmsg.startswith("sub from",2):
            await SEND(ch,await UnsubFrom(usr,lsplit[2].capitalize()))
        
        #guide
        elif lmsg == 'bd help':            
            # Command will go through. Prepare the View.
            view = ShowCommands(timeout=500)
            view.requester = usr
            view.channel = ch

            await view.send(ch)
            await view.wait()
        
        # Get the drone's wisdom
        elif lmsg.startswith("drone of wisdom"):
            if random.randint(1, 100) > 1:
                await SEND(ch, f"||*{random.choice(WISDOM)}*||")
                return
            else:
                if not str(usr.id) in list_decoded_entries("Wise"):
                    await add_entry_with_check("Wise", usr)
                    await SEND(ch, f"||***The student has surpassed the master, you have reached the peak of wisdom.***||")
                    await asyncio.sleep(2)
                else:
                    await SEND(ch, f"||***Wise choice.***||")
                return

        elif I_SPY['status'] != None and ch == I_SPY['channel']:
            if lmsg == I_SPY['answers'][I_SPY['status']]: 
                next = I_SPY['status'] + 1
                
                I_SPY['status'] = None
                await SEND(ch,'Correct.')
                await asyncio.sleep(5)
                if I_SPY['questions'][next] != None:
                    I_SPY['status'] = next
                    await SEND(ch,I_SPY['questions'][next])
                    await asyncio.sleep(I_SPY['maxwait'])
                    if I_SPY['status'] == next:
                        I_SPY['status'] = None
                        await SEND(ch,'Whatever.')
                else:
                   await SEND(ch,'I hate my job.')
            else:
                I_SPY['status'] = None
                await SEND(ch,'Wrong. Better luck next time.')

        else:
            ## tips/tricks trigger
            if len(lsplit) == 2:
                if lsplit[1] == "tip" or lsplit[1] == "trick":
                    if ch != CHANNELS['bot-commands'] and ch != CHANNELS['bot-testing']:
                        await SEND(ch, "This command can be only used in <#750060041289072771>!")
                        return
                    if lsplit[0] in TIPS_KEYS:
                        await SEND(ch,show_random_entry(lsplit[0]))
                        return
                elif lsplit[1] == "trivia":
                    if ch != CHANNELS['bot-commands'] and ch != CHANNELS['bot-testing']:
                        await SEND(ch, "This command can be only used in <#750060041289072771>!")
                        return
                    if lsplit[0] in TIPS_KEYS:
                        key = lsplit[0] + "T"
                        await SEND(ch,show_random_entry(key))
                        return

            #single word trigger
            for i, v in SINGLE_WORD_TRIGGERS.items():
                if v in lmsg:
                    if "{mention}" in i:
                        i = i.format(mention=usr.mention)
                    await SEND(ch,i)
                    return
        
            #multiple word trigger
            for i, v in MULTIPLE_WORD_TRIGGERS.items():
                if all(word in lmsg for word in v):
                    if "{mention}" in i:
                        i = i.format(mention=usr.mention)
                    await SEND(ch,i)
                    return
       
            #mixed word trigger
            for i, v in MIXED_WORD_TRIGGERS.items():
                if v[0] in lmsg:
                    if any(word in lmsg for word in v[1]):
                        await SEND(ch,i)
                        return

            # sacrificed burger
            # reaction triggers
            for i, v in REACT_TRIGGERS.items():
                 if v in lmsg:
                    if v == 'hm' and len(lmsg) > 5:
                        return
                    await ADD_REACTION(message,i)
                    return
            

        if (ch.id == 624227331720085536 and buttons_chance == 1 and not BUTTONS["status"]) or (usr != None and EXTRA_ROLES["admin"] in usr.roles and lmsg.startswith("|buttons ") and not BUTTONS["status"]):
            if EXTRA_ROLES["admin"] in usr.roles and lmsg.startswith("|buttons "):
                BUTTONS["phase"] = int(msg.split(" ")[1])
                BUTTONS["channel"] = CHANNELS[lmsg.split(" ")[2]]
            else:
                BUTTONS["phase"] = random.randint(1, 5)
                BUTTONS["channel"] = CHANNELS["general"]

            if BUTTONS["phase"] == 1:
                BUTTONS["status"] = True
                view = ButtonGames_FakeInteractionFailed(timeout=50)
                view.users = {}
                view.toolate = True
                view.message = await SEND_VIEW(BUTTONS["channel"], "A button.", view)

                await view.wait()
                await view.too_late()
                BUTTONS["status"] = False

            elif BUTTONS["phase"] == 2:
                BUTTONS["status"] = True
                view = ButtonGames_SoManyButtons(timeout=50)
                view.pressed = 0
                view.toolate = True
                view.correct_button = str(random.randint(1, 25))
                view.message = await SEND_VIEW(BUTTONS["channel"], "So many buttons... which one to click?", view)

                await view.wait()
                await view.too_late()
                BUTTONS["status"] = False

            elif BUTTONS["phase"] == 3:
                BUTTONS["status"] = True
                view = ButtonGames_HelpBrokenDrone(timeout=60)
                view.toolate = True
                view.users = []
                view.helpers = []
                view.step = 0
                view.roleowners = list_decoded_entries("Broken Drone Helper")
                view.message = await SEND_VIEW(BUTTONS["channel"], "Could you help me activating these buttons?", view)

                await view.wait()
                await view.too_late()
                BUTTONS["status"] = False

            elif BUTTONS["phase"] == 4:
                BUTTONS["status"] = True

                # theObject = random.choice(list(OBJECTS.keys()))
                # theChoices = list(OBJECTS[theObject])

                view = ButtonGames_ThrowingStuff(timeout=120)
                view.users = []
                view.custom = False
                view.closed = False

                view.results = ""
                view.votes = {
                    "0": [],
                    "1": [],
                    "2": [],
                    "3": [],
                }

                view.thrownObject = random.choice(list(OBJECTS.keys()))
                view.choices = list(OBJECTS[view.thrownObject])

                view.choice1 = view.choices[0]
                view.choice2 = view.choices[1]
                view.choice3 = view.choices[2]
                view.choice4 = view.choices[3]

                # Define the buttons without labels yet
                button1 = discord.ui.Button(label=view.choice1, custom_id="throw0", style=discord.ButtonStyle.primary)
                button2 = discord.ui.Button(label=view.choice2, custom_id="throw1", style=discord.ButtonStyle.primary)
                button3 = discord.ui.Button(label=view.choice3, custom_id="throw2", style=discord.ButtonStyle.primary)
                button4 = discord.ui.Button(label=view.choice4, custom_id="throw3", style=discord.ButtonStyle.primary)

                # Add buttons to the view with their labels
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)
                BUTTONS["view"] = view

                view.message = await SEND_VIEW(BUTTONS["channel"], f"Someone is throwing **{view.thrownObject}** in your way! How do you react?!", view)

                await view.wait()
                await view.too_late()
                BUTTONS["status"] = False

            elif BUTTONS["phase"] == 5:
                BUTTONS["status"] = True
                view = ButtonGames_ButtonFight(timeout=30)
                view.tm = 30
                view.clicks = 0
                view.winning = None
                view.users = []
                view.step = 0
                view.message = await SEND_VIEW(BUTTONS["channel"], "This is my button.", view)

                await view.wait()
                await view.too_late()
                BUTTONS["status"] = False

    ## admin commands
    if EXTRA_ROLES['admin'] in usr.roles and msg.startswith("|"):
        msginputs = msg.split(" ")
        msgsplit = msg.split(" ", 2) #creates a list from the input received. "Hello world say HI!" becomes LIST["Hello", "world", "say HI!"]
        lmsgsplit = lmsg.split(" ", 2) #creates a list from the input received and makes it lowercase. "Hello world say HI!" becomes LIST["hello", "world", "say hi!"]

        #-----admin commands that require ONE input-----
        if len(msginputs) == 1:            
            #resets the rig tracker message  ---why would you do this? ç__ç
            if lmsg.startswith("resetcounter", 1):
                await EDIT_MESSAGE(RIG_DATA['rigTracker'], "**RIGS TRACKER**,\nPATRON: 0,\nJOKER: 0,\nWICKED: 0,\nKEEPER: 0,\nHACKER: 0,\nTHIEF: 0,\nSPECTRE: 0,\nARCHON: 0,\nDRIFTER: 0,\nHERETIC: 0,\nCHAMELEON: 0")
                return
            
            # how many wisdoms are there - i swear to god bro why is this not working
            if lmsg.startswith("wisdoms", 1):
                await SEND(ch, f"I have {len(WISDOM)} wisdoms.")
                return
            
            # if lmsg.startswith("adduserids", 1):
            #     try:
            #         await SEND(ch, "Adding each id in its role list...")
            #         for mem in SERVER_DATA['server'].members:
            #             for role in mem.roles:
            #                 if role.name in FUN_LISTS.keys():
            #                     FUN_LISTS[role.name].append(mem.id)

            #         await asyncio.sleep(2)
            #         await SEND(ch, "Starting to add each user id in the db...")
            #         await asyncio.sleep(2)

            #         for funrole in FUN_LISTS.keys():
            #             for id in FUN_LISTS[funrole]:
            #                 add_entry(funrole, id)
            #                 await asyncio.sleep(3)

            #             await SEND(ch, f"Owners of {funrole} have been added...")
            #             await asyncio.sleep(2)

            #         await SEND(ch, "I'm done here.")
                        
            #     except Exception as e:
            #         await SEND(ch, e)

            #     return

        #-----admin commands that require TWO inputs-----
        elif len(msginputs) == 2 or lmsg.startswith("nr", 1):
            second = msg.split(" ", 1)[1].replace("_", " ")          # NOT lowercase
            lsecond = msg.split(" ", 1)[1].lower().replace("_", " ") # YES lowercase
            #ispy command
            if lmsg.startswith("ispy",1):
                I_SPY['channel'] = CHANNELS[lsecond]
                I_SPY['status'] = 0
                await SEND(I_SPY['channel'], I_SPY['questions'][0])
                await DELETE(message)
                await asyncio.sleep(I_SPY['maxwait'])
                if I_SPY['status'] == 0:
                    I_SPY['status'] = None
                    await SEND(I_SPY['channel'],'Whatever.')
                return

            #create a new role with name
            if lmsg.startswith("nr", 1):
                try:
                    add_entry(second, "dummy")
                except Exception as e:
                    await SEND(ch, e)
                    return

                await SEND(ch, "Role created successfully.")

                FUN_ROLES.append(second)
                return
        
        #-----admin commands that require THREE or MORE inputs-----
        elif len(msginputs) >= 3:
            third = msg.split(" ", 2)[2]          #NOT lowecase
            lthird = msg.split(" ", 2)[2].lower() #YES lowecase

            ##-----COMMANDS THAT ONLY USE 3 INPUTS-----
            #have the bot say whatever you say
            if lmsg.startswith("makesay", 1):
                try:
                    await SEND(CHANNELS[lmsgsplit[1]], third)
                    await DELETE(message)
                    return
                except:
                    await SEND(CHANNELS['bot-testing'], "I refuse.")
                    return
    
            #give ckr
            if lmsg.startswith("ckr to", 1):
                for mem in SERVER_DATA['server'].members:
                    if mem.name.lower() == lthird:
                        await SEND(ch, "I gave the Chat Killer role to " + mem.name)
                        await asyncio.sleep(1)
                        await ADD_ROLES(mem, EXTRA_ROLES['ckr'])
                        break
                return  
                
            #remove ckr
            if lmsg.startswith("ckr from", 1):
                for mem in SERVER_DATA['server'].members:
                    if mem.name.lower() == lthird:
                        await SEND(ch, "I took the Chat Killer Role away from " + mem.name)
                        await asyncio.sleep(1)
                        await REMOVE_ROLES(mem, EXTRA_ROLES['ckr'])
                        break
                return   

            #give any role
            if lmsg.startswith("assign", 1):
                try:
                    if not third in FUN_ROLES:
                        await SEND(ch, "You cannot assign this role through my commands.")
                        return
                        
                    for mem in SERVER_DATA['server'].members:
                        if int(mem.id) == int(msgsplit[1]):
                            if msgsplit[1] in list_decoded_entries(third):
                                await asyncio.sleep(1)
                                await SEND(ch, "They already own this role, duh.")
                                return

                            add_entry(third, msgsplit[1])
                            await asyncio.sleep(1)
                            await SEND(ch, "I gave the role to " + mem.name)
                            break
                except Exception as e:
                    await SEND(ch, e)

                return  

            #remove any role
            if lmsg.startswith("unassign", 1):
                try:
                    if not third in FUN_ROLES:
                        await SEND(ch, "You cannot unassign this role through my commands.")
                        return

                    for mem in SERVER_DATA['server'].members:
                        if int(mem.id) == int(msgsplit[1]):
                            entries = list_decoded_entries(third)

                            if not msgsplit[1] in entries:
                                await asyncio.sleep(1)
                                await SEND(ch, "They do not own the role. Are you ok?")
                                return

                            index = entries.index(msgsplit[1])
                            delete_entry(third, index)

                            await asyncio.sleep(1)
                            await SEND(ch, "Took the role away from " + mem.name)
                            break
                except Exception as e:
                    await SEND(ch, e)
                return  

            #purge any role
            if lmsg.startswith("purge role", 1):
                try:
                    if not third in FUN_ROLES:
                        await SEND(ch, "You cannot obliterate this role through my commands.")
                        return
                        
                    delete_key(third)
                    FUN_ROLES.remove(third)
                    await asyncio.sleep(1)
                    await SEND(ch, "The role is gone.")
                except Exception as e:
                    await SEND(ch, e)
                return 
            
            #purge any role
            if lmsg.startswith("purge drole", 1):
                if third in APPROVED_ROLES:
                    neededrole = APPROVED_ROLES[third]
                else:
                    await SEND(ch, "You cannot obliterate this role through my commands.")
                    return
                    
                await PURGE_ROLES(neededrole)
                await asyncio.sleep(1)
                await SEND(ch, "The Discord role is gone.")
                return  
            
            #create a new role with name and color 
            if lmsg.startswith("ndr", 1):
                try:
                    newrole = await NEW_ROLE(SERVER_DATA['server'], lmsgsplit[1], third)
                except Exception as e:
                    await SEND(ch, e)
                    return

                await SEND(ch, "Discord role created successfully.")

                APPROVED_ROLES[third] = newrole
                return
            
            #give any role
            if lmsg.startswith("dassign", 1):
                try:
                    if third in APPROVED_ROLES:
                        neededrole = APPROVED_ROLES[third]
                    else:
                        await SEND(ch, "You cannot assign this role through my commands.")
                        return
                        
                    for mem in SERVER_DATA['server'].members:
                        if int(mem.id) == int(msgsplit[1]):
                            await SEND(ch, "I gave the role to " + mem.name)
                            await asyncio.sleep(1)
                            await ADD_ROLES(mem, neededrole)
                            break
                except Exception as e:
                    print(e)
                    await SEND(ch, e)

                return  

            #remove any role
            if lmsg.startswith("dunassign", 1):
                if third in APPROVED_ROLES:
                    neededrole = APPROVED_ROLES[third]
                else:
                    await SEND(ch, "You cannot unassign this role through my commands.")
                    return

                for mem in SERVER_DATA['server'].members:
                    if int(mem.id) == int(msgsplit[1]):
                        await SEND(ch, "Took the role away from " + mem.name)
                        await asyncio.sleep(1)
                        await REMOVE_ROLES(mem, neededrole)
                        break
                return  
            
            #creates new emoji
            if lmsg.startswith("ne", 1):
                try:
                    url = msgsplit[1]
                    name = third
                    
                    # Download the image data
                    response = requests.get(url)
                    if response.status_code == 200:
                        image_data = response.content
                        emoji = await message.guild.create_custom_emoji(name=name, image=image_data)
                        await message.channel.send(f"Emoji {emoji.name} has been added!")
                    else:
                        await message.channel.send("Could not download image.")
                        
                except Exception as e:
                    await message.channel.send(f"Error creating emoji: {str(e)}")

            #-----COMMANDS THAT ONLY USE 4 INPUTS-----
            #edits db rig tracking count for specific alignment
            if lmsg.startswith("edit tracker", 1):
                db.set(lthird + "uses", msg.split(" ", 3)[3])  #edit tracker patron 2 
                return
            
            #-----COMMANDS THAT ONLY USE EVEN MORE INPUTS-----
            #empty so far-

        #length may vary... for this one
        #quiz
        if lmsg.startswith("quiz", 1):
            if lmsgsplit[1] == "new":
                qSplit = msgsplit[2].split("|")
                if len(qSplit) != 7:
                    await SEND(ch,"Question does not have the required 7 sections.")
                else:
                    add_entry("quiz", msgsplit[2])
                    await SEND(ch, "Successfully added new quiz question")

            elif lmsgsplit[1] == "amount":
                await SEND(ch,"There are " + str(get_amount_of_entries("quiz")) + " questions in the database.")        

            elif lmsgsplit[1] == "print":
                question = show_specific_entry("quiz",int(msgsplit[2]))
                qSplit = question.split("|")
                toSend = "Q:\n" + qSplit[0] + "\nCorrect Answer:\n" + qSplit[1]
                toSend += "\nA2:\n" + qSplit[2] + "\nA3:\n" + qSplit[3] + "\nA4:\n" + qSplit[4]
                toSend += "\nGood response:\n" + qSplit[5] + "\nBad response:\n" + qSplit[6]
                await SEND(ch,toSend)
            elif lmsgsplit[1] == 'list':
                await PRINT_QUESTIONS(ch)
            elif lmsgsplit[1] == "delete":
                delete_entry("quiz", int(msgsplit[2]))
                await SEND(ch,"Question at index " + msgsplit[2] + " has been deleted." )

            return

        #and if none of the others match go here...
        if lmsg.startswith("triv", 2) or lmsg.startswith("tip", 2):
            key = msgsplit[1]
            if not key in TIPS_KEYS:
                await SEND(ch,"Invalid alignment.")
                return
            
            #tip or trivia?
            tot = "tip"
            if msg.startswith("triv",2):
                tot = "triv"
                #for trivia, key has extra "T" at the end
                key = key + "T"
            elif not msg.startswith("tip",2):
                await SEND(ch,"Invalid command.")
                return
            
            #add tip   
            if msg.startswith("n",1):
                add_entry(key,msgsplit[2])
                await SEND(ch,"New " + msgsplit[1] + " " + tot + " added.")
                return

            #list tips
            if msg.startswith("l",1):
                await SEND(ch,msgsplit[1] + " " + tot + "(s):")
                await PRINT_ENTRIES(ch, key)
                return
                
            #delete tip
            if msg.startswith("d",1):
                delete_entry(key,int(msgsplit[2]))
                await SEND(ch,msgsplit[1] + " " + tot + "(s):")
                await PRINT_ENTRIES(ch, key)
                #hmmmm
                return
            
            #copy tip to thread
            if msg.startswith("c",1):
                #print(msgsplit[2])
                #newSplit = msg.split(' ',3)
                #channel = client.get_channel(int(newSplit[2]))
                thread = client.get_channel(int(msgsplit[2]))
                await SEND(ch,'copying...')
                await POST_TIPS(thread,key)
                return

### RUN THE BOT ###
client.run(os.environ['TOKEN'])
