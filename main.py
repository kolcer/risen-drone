### IMPORTS ###

import discord
import os
import random
import asyncio
#from datetime import date
from difflib import SequenceMatcher

from globals import *
from roles import *
from ladders import *
from rated import *
from rigs import *
from database import *
from quiz import *

### INITIAL SETUP ###

# This allows us to know if user has updated their presence
# Mosty for the gun role nick change prevention
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

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
        await SEND(channel, "-----\n" + entries[i].decode("utf-8") + "\n------")
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
            
    #fetch questions for the quiz
    await FetchQuestions()

    #prepare emojis reactions
    for i, v in EMOJIS_TO_REACT.items():
        EMOJIS_TO_REACT[i] = GET_EMOJI(client,v)
    
    #send ready to the test channel
    await SEND(CHANNELS["bot-testing"], 'The last edited code is now effective.')

#member update, prevent changing gun nick to anything other than the gun name
@client.event
async def on_member_update(before, after):
    
    #nick has not changed 
    if before.nick == after.nick:
        return
    
    #for thief rig
    if before in NickDictionary and after.nick != NickDictionary[before]:
      await EDIT_NICK(after, NickDictionary[before])
      return
 
    #is user a gun?
    if not MORPHABLE_ROLES["Guns"][0] in before.roles:
        return
    
    #ignore if user nick after change is a gun name
    if after.nick in WORST_GUNS:
        return

    await EDIT_NICK(after, random.choice(WORST_GUNS))
    return

#on new member join
@client.event
async def on_member_join(member):
    await SEND(CHANNELS["general"],
        "Welcome to Crazy Stairs Discord Server!"
        "\nUnlike other Jokers around here, I am a real bot."
        "\nPlease read the <#750056989207429143>, to avoid misunderstandings."
        "\nHave fun, and remember: It's okay to be a little crazy.")

#saves last deleted message for necromancer rig to show
@client.event
async def on_message_delete(message):
  RIG_DATA['ghostMsg'] = "*" + str(message.author.display_name) + "'s last words lie here...*"


@client.event
async def on_reaction_add(reaction, user):

    await SplicerRig(reaction,user)

    if (reaction.emoji == "csSleazelApproves" or reaction.emoji == "csSleazelNotApproved") and user.id != 481893862864846861:
        await reaction.remove(user)

@client.event
async def on_message_edit(before, after):
    msg = after.content
    usr = after.author
    ch = after.channel

    if ch.id == 845454640103424032 and (not after.attachments and 'http' not in msg):
        for role in usr.roles:
            if role.name in IMMUNITY_ROLES:
                return

        await DELETE(after)

#main function on each message being intercepted
@client.event
async def on_message(message):
    msg = message.content
    ## lowercase the message for some commands to use
    lmsg = msg.lower()
    usr = message.author
    ch = message.channel

    if ch.id == 845454640103424032 and (not message.attachments and 'http' not in msg):
        for role in usr.roles:
            if role.name in IMMUNITY_ROLES:
                return
        if usr.id == 827952429290618943:
            return

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

    if usr not in MSG_SENT:
        MSG_SENT[usr] = 1
    else:
        MSG_SENT[usr] += 1

            

    if ch.id == 845454640103424032 and message.attachments:
        if usr not in ARTISTS:
            ARTISTS[usr] = 1
            await ADD_REACTION(message, "🤍")
        elif ARTISTS[usr] == 1:
            ARTISTS[usr] += 1
            await ADD_REACTION(message, "❤️")
        else: 
            if not FUN_ROLES["Architect Design"] in usr.roles:
                await ADD_ROLES(usr, FUN_ROLES["Architect Design"])
                await asyncio.sleep(1)
                await SEND(ch, "I like your style.")
                await ADD_REACTION(message, "❤️‍🔥")
        
    randomchance = random.randint(0,5000)
    eligible = 0
    rolename = ""

    if randomchance == 0:
        for role in usr.roles:
            if role.name.lower() in SANCTUARY:
                eligible += 1 #are you happy? >:      
                if eligible == 1:
                    rolename = role.name.lower()

        
        if eligible == 1:
            await SEND(CHANNELS["bot-commands"], usr.mention + SANCTUARY[rolename] + " (1/? chance)")
            await asyncio.sleep(1)
            if not FUN_ROLES["Sanctuary Discoverer"] in usr.roles:
                await usr.add_roles(FUN_ROLES["Sanctuary Discoverer"])
    
    if msg.lower() == "reset bot" and usr not in FIX_BOT:

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

            for rig in ACTIVE_RIGS:
                ACTIVE_RIGS[rig] = False 

            for cooldown in RIG_COOLDOWNS:
                RIG_COOLDOWNS[cooldown] = False


        await asyncio.sleep(60)
        if len(FIX_BOT) != 0:
            await SEND(ch, "Games have not been reset due to lack of users asking to.")
            FIX_BOT.clear()
        return

    #mini game in progress
    if LADDERS['status'] != "off" and usr in MG_QUEUE and ch == LADDERS['channel']:

        await LucidLaddersProcessMessage(usr,msg)
       
    #normal non-admin usage.
    else:
        

        ## split the message to 3 strings for some commands to use
        ## no need to have more than 4 strings
        lsplit = lmsg.split(" ",3) 
        
        #create chat killer task
        #this should run regardless if the message was intercepted
        #by some other command 
        ckr_task = asyncio.create_task(WAIT_FOR_CHAT_KILLER(message))
 
        #broken drone impostor prevention
        compare = SequenceMatcher(None, usr.display_name.upper(), SERVER_DATA['nick'])
        if compare.ratio() > 0.7:
            await SEND(ch, usr.mention + ' ' + random.choice(IMPOSTOR_WARNINGS))
            await EDIT_NICK(usr,random.choice(IMPOSTOR_NICKS))
 
        #start the quiz
        elif ch == CHANNELS["bot-commands"] and lmsg == "start quiz" and not QUIZ["active"] and not QUIZ["second-player"]:

            await StartQuiz(usr,ch)

        #join an ongoing quiz
        elif ch == CHANNELS["bot-commands"] and lmsg == "join quiz" and QUIZ["second-player"] and usr not in QUIZZERS:
            
            await JoinQuiz(usr,ch)

        elif ch == CHANNELS["bot-commands"] and QUIZ["active"] and not QUIZ["second-player"] and QUIZ["can-answer"]:
            
            await ProcessQuizAnswer(usr,ch,message,lmsg)

        #start mini game
        elif lmsg == "play lucid ladders":

            await PlayLucidLadders(usr,ch)

        #join mini game
        elif lmsg == "join" and LADDERS['status'] == "gather" and LADDERS['channel'] == ch:

            await JoinLucidLadders(usr)

        # ## All Rigs in one
        elif lsplit[0] == "cast" and lsplit[2] == "rig":

            await CastRig(lsplit[1],ch,usr)

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

        ## Give Mana command
        elif msg.lower().startswith("give mana to "):
        
            await GiveMana(ch,usr,message)
                 
        ## Scold command
        elif lmsg.startswith("bd scold "):
            finalmsg = None
            for member in SERVER_DATA['server'].members:
                if member.name.lower() + "#" + member.discriminator == lsplit[3]:
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

        ## Show Profile
        elif lmsg == "bd show profile":
            messages = ""
            profilemsg = str(usr.display_name) + "'s roles:\n\n"
            for role in FUN_ROLES:
                if FUN_ROLES[role] in usr.roles:
                    if str(role) in LIMITED_ROLES:
                        profilemsg += "**" + str(role) + "** 🔒 " + LIMITED_ROLES[str(role)] + "\n"
                    else:
                        profilemsg += "**" + str(role) + "**\n"
                else:
                    if str(role) in LIMITED_ROLES:
                        profilemsg += "**???** 🔒 " + LIMITED_ROLES[str(role)] + "\n"
                    else:
                        profilemsg += "**???**\n"

            if usr not in MSG_SENT:
                messages = "0"
            else:
                messages = MSG_SENT[usr]

            if usr not in LAST_RIG:
                lastrig = "None"
            else:
                lastrig = LAST_RIG[usr]

            profilemsg += "\n" + str(usr.display_name) + "'s stats:\n\n"
            profilemsg += "**Latest messages sent:** " + str(messages) + "\n"
            profilemsg += "**Last rig cast:** " + str(lastrig).capitalize() + "\n"
            
            await SEND(ch, profilemsg)

        ## Revive Chat Command
        elif "revive" in lmsg and "chat" in lmsg and len(lmsg.split(" ")) < 4:
            #chat has to be dead, duh
            if not CHAT_KILLER['reviveChat']:
                await SEND(ch, "This chat is very much alive, I am afraid.")
                return

            #only chat killers can use the command
            if not EXTRA_ROLES['ckr'] in message.author.roles:
                await SEND(ch, "It is not your fault.")
                return

            await SEND(ch, "Redeeming yourself? Alright.")
            await asyncio.sleep(2)
            await SEND(ch, random.choice(REVIVE_CHAT))
            CHAT_KILLER['reviveChat'] = False
 
        ## Splicer role assignment
        elif "<:csSplicer:988948000200069191>" in msg:
            if usr in SPLICER_FANS:
                if SPLICER_FANS[usr] == 3:
                    if not FUN_ROLES["Splicer"] in usr.roles:
                        await ADD_ROLES(usr, FUN_ROLES["Splicer"])
                        await asyncio.sleep(1)
                        await SEND(ch, "Ok... there you go.")
                else:
                    SPLICER_FANS[usr] += 1
            else:
                SPLICER_FANS[usr] = 1

        #morph command
        elif lmsg.startswith("morph to"):
            morphToTarget = lsplit[2].capitalize()
            await SEND(ch, await MorphTo(usr,morphToTarget))

        #demorph command (accepts demorph, unmorph and any **morph from combination)
        elif lmsg.startswith("morph from",2):
            demorphFromTarget = lsplit[2].capitalize()
            await SEND(ch,await DemorphFrom(usr,demorphFromTarget))

            if demorphFromTarget == "Climber" and SPECIAL_ROLES["Climber"][0] in usr.roles:
                await REMOVE_ROLES(usr, SPECIAL_ROLES["Climber"][0])
                await asyncio.sleep(10)
                await ADD_ROLES(usr, SPECIAL_ROLES["Climber"][0])
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

            await SEND(ch,''' **Broken Drone commands:**

Please use these commands only in <#750060041289072771>!    

**morph to** _[alignment]_
➡️ Get chosen alignment role in this server

**demorph from** _[alignment]_
➡️ Remove chosen alignment role

**sub to** _[ping role]_
➡️ Subscribe to chosen ping role

**unsub from** _[ping role]_
➡️ Unsubscribe from chosen ping role

**general tip**
➡️ Show a general tip

_[alignment]_ **tip**
➡️ Show chosen alignment tip

**general trivia**
➡️ Show a general trivia

_[alignment]_ **trivia**
➡️ Show chosen alignment trivia

**cast** _[alignment]_ **rig**
➡️ A fun command to mess around in the server

**play lucid ladders**
➡️ Start Lucid Ladders mini game (requires at least 2 playres)

**start quiz**
➡️ Start Crazy Stairs knowledge quiz (2 players required)

**bd scold** _[username#discriminator]_
➡️ Scolds chosen user

**revive chat**
➡️ Revive chat (only for true chat killers)

**bd show profile**
➡️ Shows Your stats and special roles

**give mana to** _[username#discriminator]_
➡️ Rescues a possessed user

**reset bot**
➡️ Use this command if the bot breaks (3 users required)

**Available aligments**: Patron, Joker, Wicked, Spectre, Muggle, Chameleon, Keeper, Hacker, Thief, Archon, Drifter, Heretic.
**Extra alignments** (cannot be morphed into): Possessed, None, Architect.
**Available ping roles**: Updates, Announcements, Events, Polls, Minigames, Sleazel-in-game (sub if you want Prank The Creator badge)
''')
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
                    if lsplit[0] in TIPS_KEYS:
                        await SEND(ch,show_random_entry(lsplit[0]))
                        return
                elif lsplit[1] == "trivia":
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
      
    ## admin commands
    if EXTRA_ROLES['admin'] in usr.roles and msg.startswith("|"):
        msginputs = msg.split(" ")
        msgsplit = msg.split(" ", 2) #creates a list from the input received. "Hello world say HI!" becomes LIST["Hello", "world", "say HI!"]
        lmsgsplit = lmsg.split(" ", 2) #creates a list from the input received and makes it lowercase. "Hello world say HI!" becomes LIST["hello", "world", "say hi!"]

        #-----admin commands that require ONE input-----
        if len(msginputs) == 1:
            #full admin commands list
            if lmsg.startswith("cmdlist", 1):
                if ch.id != 813882658156838923:
                    SEND(ch, "Try to be more discreet, they do not need to know.")
                    return

                await SEND(ch,''' **ADMIN COMMANDS:**  
|ispy [channel-name]: Starts an "ispy" mini-game in the specified channel.

|quiz [action] [?]:

New: Creates a new quiz question with the format "Question|Correct answer|Option 1|Option 2|Option 3|[Automatic user mention +] Good response|Bad response".
Count: Displays the number of currently existing quiz questions.
Print: Prints a specified quiz question with its answer, options, and responses. Specify the question index in the [?] section.
List: Lists all current quiz questions.
Delete: Deletes the specified quiz question by index.

|makesay [channel-name] [message]: Forces the bot to type the specified message in the indicated channel.

|ckr to/from [user#discriminator]: Gives or removes the Chat Killer role from the specified user.

|nr [hexadecimal-color] [name]: Creates a new role with the specified color and name.

|un/assign [!!USER ID!!] [role-name]: Removes or assigns the specified role to the indicated user. The role must be in the FUN_ROLES list.

|alter [old-name] [new-name]: Changes the old role name to the new one. The old name should contain underscores instead of spaces, and the role must be in the FUN_ROLES list.

|purge role [role-name]: Deletes the specified role. The role must be in the FUN_ROLES list.

|edit tracker [alignment] [new-count]: Changes the tracker count for the selected alignment to the specified number.
''')
                return
            
            #resets the rig tracker message  ---why would you do this? ç__ç
            if lmsg.startswith("resetcounter", 1):
                await EDIT_MESSAGE(RIG_DATA['rigTracker'], "**RIGS TRACKER**,\nPATRON: 0,\nJOKER: 0,\nWICKED: 0,\nKEEPER: 0,\nHACKER: 0,\nTHIEF: 0,\nSPECTRE: 0,\nARCHON: 0,\nDRIFTER: 0,\nHERETIC: 0,\nCHAMELEON: 0")
                return

        #-----admin commands that require TWO inputs-----
        elif len(msginputs) == 2:
            #ispy command
            if lmsg.startswith("ispy",1):
                I_SPY['channel'] = CHANNELS[lmsgsplit[1]]
                I_SPY['status'] = 0
                await SEND(I_SPY['channel'], I_SPY['questions'][0])
                await DELETE(message)
                await asyncio.sleep(I_SPY['maxwait'])
                if I_SPY['status'] == 0:
                    I_SPY['status'] = None
                    await SEND(I_SPY['channel'],'Whatever.')
                return
        
        #-----admin commands that require THREE or MORE inputs-----
        elif len(msginputs) >= 3:
            third = msg.split(" ", 2)[2]          #NOT lowecase
            lthird = msg.split(" ", 2)[2].lower() #YES lowecase

            ##-----COMMANDS THAT ONLY USE 3 INPUTS-----
            #have the bot say whatever you say
            if lmsg.startswith("makesay", 1):
                await SEND(CHANNELS[lmsgsplit[1]], third)
                await DELETE(message)
                return

            #create a new role with name and color
            if lmsg.startswith("nr", 1):
                try:
                    newrole = await NEW_ROLE(SERVER_DATA['server'], lmsgsplit[1], third)
                except Exception as e:
                    await SEND(ch, e)
                    return

                await SEND(ch, "Role created successfully.")

                FUN_ROLES[third] = newrole
                return
    
            #give ckr
            if lmsg.startswith("ckr to", 1):
                print(lthird)
                for mem in SERVER_DATA['server'].members:
                    if mem.name.lower() + "#" + mem.discriminator == lthird:
                        await SEND(ch, "I gave the Chat Killer role to " + mem.name + "#" + mem.discriminator)
                        await asyncio.sleep(1)
                        await ADD_ROLES(mem, EXTRA_ROLES['ckr'])
                        break
                    return  

            #give any role
            if lmsg.startswith("assign", 1):
                if third in FUN_ROLES:
                    neededrole = FUN_ROLES[third]
                else:
                    await SEND(ch, "You cannot assign this role through my commands.")
                    return
                    
                for mem in SERVER_DATA['server'].members:
                    if mem.id == msgsplit[1]:
                        await SEND(ch, "I gave the role to " + mem.name + "#" + mem.discriminator)
                        await asyncio.sleep(1)
                        await ADD_ROLES(mem, neededrole)
                        break
                return  

            #remove any role
            if lmsg.startswith("unassign", 1):
                if third in FUN_ROLES:
                    neededrole = FUN_ROLES[third]
                else:
                    await SEND(ch, "You cannot unassign this role through my commands.")
                    return

                for mem in SERVER_DATA['server'].members:
                    if mem.id == msgsplit[1]:
                        await SEND(ch, "Took the role away from " + mem.name + "#" + mem.discriminator)
                        await asyncio.sleep(1)
                        await REMOVE_ROLES(mem, neededrole)
                        break
                return  

            #edit any role ---deleting and adding the role again is recommended
            if lmsg.startswith("alter", 1):
                if msgsplit[1].replace("_", " ") in FUN_ROLES:
                    neededrole = FUN_ROLES[msgsplit[1].replace("_", " ")]
                else:
                    await SEND(ch, "You cannot edit this role through my commands.")
                    return

                await EDIT_ROLE(neededrole, third, "changing name")
                await asyncio.sleep(1)
                await SEND(ch, "You changed the name correctly.")
                FUN_ROLES[msgsplit[1].replace("_", " ")] = neededrole
                return  

            #purge any role
            if lmsg.startswith("purge role", 1):
                if third in FUN_ROLES:
                    neededrole = FUN_ROLES[third]
                else:
                    await SEND(ch, "You cannot obliterate this role through my commands.")
                    return
                    
                await PURGE_ROLES(neededrole)
                await asyncio.sleep(1)
                await SEND(ch, "The role is gone.")
                return  

            #remove ckr
            if lmsg.startswith("ckr from", 1):
                for mem in SERVER_DATA['server'].members:
                    if mem.name.lower() + "#" + mem.discriminator == lthird:
                        await SEND(ch, "I took the Chat Killer Role away from " + mem.name + "#" + mem.discriminator)
                        await asyncio.sleep(1)
                        await REMOVE_ROLES(mem, EXTRA_ROLES['ckr'])
                        break
                return   

            ##-----COMMANDS THAT ONLY USE 4 INPUTS-----
            #edits db rig tracking count for specific alignment
            if lmsg.startswith("edit tracker", 1):
                db.set(lthird + "uses", msg.split(" ", 3)[3])  #edit tracker patron 2 
                return
            
            ##-----COMMANDS THAT ONLY USE EVEN MORE INPUTS!!!!!!-----
            #empty so far-

        ##length may vary... for this one
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
                print(msgsplit[2])
                channel = client.get_channel(int(msgsplit[2]))
                await SEND(ch,'copying...')
                await POST_TIPS(channel,key)
                return

### RUN THE BOT ###
client.run(os.environ['TOKEN'])
