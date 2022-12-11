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


### PUBLIC (ON EVENT) FUNCTIONS ###
    
#drone start up, prepare roles here
@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Bioforge")
    await client.change_presence(activity=game)

    #get the guild
    global SERVER
    global RIGTRACKER
    #this is a one-off, so we do not worry about rate limits
    SERVER = client.get_guild(SERVER)
    
    #get the channels
    for i, v in CHANNELS.items():
        CHANNELS[i] = GET_CHANNEL(client,v)
    
    RIGTRACKER = await GET_MSG(CHANNELS["bot-testing"],RIGTRACKER)

    #prepare the roles
    PrepareRoles(SERVER.roles)
    
    #fetch questions for the quiz
    FetchQuestions()

    #prepare emojis reactions
    for i, v in EMOJIS_TO_REACT.items():
        EMOJIS_TO_REACT[i] = GET_EMOJI(client,v)
    
    #send ready to the test channel
    await SEND(CHANNELS["bot-testing"],'The last edited code is now effective.')

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
  global ghostMsg
  ghostMsg = "*" + str(message.author.display_name) + "'s last words lie here...*"


@client.event
async def on_reaction_add(reaction, user):

    SplicerRig(reaction,user)

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

    global MSG_SENT
    global ARTISTS

    msg = message.content
    usr = message.author
    ch = message.channel

    if ch.id == 845454640103424032 and (not message.attachments and 'http' not in msg):
        for role in usr.roles:
            if role.name in IMMUNITY_ROLES:
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

    if usr.id == 861582242023079987:
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
                eligible = eligible + 1                
                if eligible == 1:
                    rolename = role.name.lower()

        
        if eligible == 1:
            await SEND(CHANNELS["bot-commands"], usr.mention + SANCTUARY[rolename] + " (1/? chance)")
            await asyncio.sleep(1)
            if not FUN_ROLES["Sanctuary Discoverer"] in usr.roles:
                await usr.add_roles(FUN_ROLES["Sanctuary Discoverer"])
    
    #this will avoid old activatig with old bot
    if msg.startswith(">"):
        return
    
    global FIX_BOT

    if msg.lower() == "reset bot" and usr not in FIX_BOT:
        if ADMIN in usr.roles:
            await SEND(ch, "All Games have been resetted.")
            FIX_BOT.clear()
            FORCE_CLOSE_EVENT()
            MG_RESET()
            NickDictionary.clear()
            return

        FIX_BOT.append(usr)
        if len(FIX_BOT) == 1:
            await SEND(ch, "One User wants me to reset. 2 more people are required for it to take effect.")
        elif len(FIX_BOT) == 2:
            await SEND(ch, "Two Users want me to reset. 1 more person is required for it to take effect.")
        else:
            await SEND(ch, "All Games have been resetted.")
            FIX_BOT.clear()
            FORCE_CLOSE_EVENT()
            MG_RESET()


        await asyncio.sleep(60)
        if len(FIX_BOT) != 0:
            await SEND(ch, "Games have not been resetted due to lack of users asking to.")
            FIX_BOT.clear()
        return

    #mini game in progress
    if MG_STATUS != "off" and usr in MG_QUEUE and ch == MG_CHANNEL:

        await LucidLaddersProcessMessage(usr,msg)
       
    #normal non-admin usage.
    elif not msg.startswith("|"):
        
        ## lowercase the message for some commands to use
        lmsg = msg.lower()
        ## split the message to 3 strings for some commands to use
        ## no need to have more than 4 strings
        lsplit = lmsg.split(" ",3) 
        
        #create chat killer task
        #this should run regardless if the message was intercepted
        #by some other command
        ckr_task = asyncio.create_task(WAIT_FOR_CHAT_KILLER(message))
 
        #broken drone impostor prevention
        compare = SequenceMatcher(None, usr.display_name.upper(), BROKEN_DRONE_NICK)
        if compare.ratio() > 0.7:
            await SEND(ch, usr.mention + ' ' + random.choice(IMPOSTOR_WARNINGS))
            await EDIT_NICK(usr,random.choice(IMPOSTOR_NICKS))
            return

        #start the quiz
        if ch == CHANNELS["bot-commands"] and lmsg == "broken drone start quiz" and not QUIZ["active"] and not QUIZ["second-player"]:

            await StartQuiz(usr,ch)

        #join an ongoing quiz
        if ch == CHANNELS["bot-commands"] and lmsg == "join quiz" and QUIZ["second-player"] and usr not in QUIZZERS:
            
            await JoinQuiz(usr,ch)

        if ch == CHANNELS["bot-commands"] and QUIZ["active"] and not QUIZ["second-player"] and QUIZ["can-answer"]:
            
            await ProcessQuizAnswer(usr,ch,message,lmsg)

        #start mini game
        if lmsg == "play lucid ladders":

            await PlayLucidLadders(usr,ch)

        #join mini game
        if lmsg == "join" and MG_STATUS == "gather" and MG_CHANNEL == ch:

            await JoinLucidLadders(usr)

        # ## All Rigs in one
        if lsplit[0] == "cast" and lsplit[2] == "rig":

            await CastRig(lsplit[1],ch,usr)

        ## thief rig active
        if ACTIVE_RIGS["thief"]:

            await ExecuteThiefRig(ch,usr)

        ## Spectre Rig Active
        if ACTIVE_RIGS["spectre"]:
                
            await ExecuteSpectreRig(ch,usr,message)

        ## Joker Rig Active
        if ACTIVE_RIGS["joker"]:
                
            await ExecuteJokerRig(ch,usr,message)

        # Splicer Rig Active
        if ACTIVE_RIGS["splicer"]:

            await ExecuteSplicerRig(ch,usr)

        ## Give Mana command
        if msg.lower().startswith("give mana to "):
        
            await GiveMana(ch,usr,message)
                 
        ## Scold command
        if lmsg.startswith("broken drone scold "):
            finalmsg = None
            for member in SERVER.members:
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
            return

        ## Show Profile
        if lmsg == "bd show profile":
            messages = ""
            profilemsg = str(usr.display_name) + "'s roles:\n\n"
            for role in FUN_ROLES:
                if FUN_ROLES[role] in usr.roles:
                    profilemsg += "**" + str(role) + "**\n"
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
        if "revive" in lmsg and "chat" in lmsg and len(lmsg.split(" ")) < 4:
            global revivechat
            #chat has to be dead, duh
            if not revivechat:
                await SEND(ch, "This chat is very much alive, I am afraid.")
                return

            #only chat killers can use the command
            if not CKR in message.author.roles:
                await SEND(ch, "It is not your fault.")
                return

            await SEND(ch, "Reedeming yourself? Alright.")
            await asyncio.sleep(2)
            await SEND(ch, random.choice(REVIVE_CHAT))
            revivechat = False
            return

        ## Splicer role assignment
        if "<:_splicer:988948000200069191>" in msg:
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
        if lmsg.startswith("morph to"):
            await SEND(ch,await MorphTo(usr,lsplit[2].capitalize()))

        #demorph command (accepts demorph, unmorph and any **morph from combination)
        if lmsg.startswith("morph from",2):
            await SEND(ch,await DemorphFrom(usr,lsplit[2].capitalize()))

        #sub command       
        if lmsg.startswith("sub to"):
            await SEND(ch,await SubTo(usr,lsplit[2].capitalize()))

        #unsub command
        if lmsg.startswith("sub from",2):
            await SEND(ch,await UnsubFrom(usr,lsplit[2].capitalize()))
       
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
      

               
    ## admin command
    else:
        #check for admin
        if not ADMIN in usr.roles:
            return

        #deterimine the key (this is an alignment name in most cases)
        split = msg.split(" ", 2)
        split2 = msg.lower().split(" ", 2)
        msgback = msg.split(" ", 2)[2]
        targetrole = msg.split(" ")[1].replace("_", " ")

        #have the bot say whatever you say
        if msg.startswith("makesay", 1):
            await SEND(CHANNELS[split[1]], msgback)
            return

        #create a new role with name and color
        if msg.startswith("nr", 1):
            try:
                newrole = await NEW_ROLE(SERVER,split[1], msgback.replace("_"," "))
            except Exception as e:
                await SEND(ch, e)
                return

            await SEND(ch, "Worked.")
            FUN_ROLES[msgback.replace("_"," ")] = newrole
            return
    
        #give ckr
        if msg.startswith("ckr to ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split2[2]:
                    await SEND(ch, "I gave the Chat Killer Role to " + split2[2])
                    await asyncio.sleep(1)
                    await ADD_ROLES(mem,CKR)
                    break
            return  

        #give any role
        if msg.startswith("assign", 1):
            if targetrole in FUN_ROLES:
                neededrole = FUN_ROLES[targetrole]
            else:
                await SEND(ch, "You cannot assign this role through my commands.")
                return
                
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split2[2]:
                    await SEND(ch, "I gave the Role to " + split2[2])
                    await asyncio.sleep(1)
                    await ADD_ROLES(mem, neededrole)
                    break
            return  

        #remove any role
        if msg.startswith("unassign", 1):
            if targetrole in FUN_ROLES:
                neededrole = FUN_ROLES[targetrole]
            else:
                await SEND(ch, "You cannot unassign this role through my commands.")
                return

            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split2[2]:
                    await SEND(ch, "Took the role away from " + split2[2])
                    await asyncio.sleep(1)
                    await REMOVE_ROLES(mem,neededrole)
                    break
            return  

        #edit any role
        if msg.startswith("alter", 1):
            if targetrole in FUN_ROLES:
                neededrole = FUN_ROLES[targetrole]
            else:
                await SEND(ch, "You cannot edit this role through my commands.")
                return

            await EDIT_ROLE(neededrole, msgback.replace("_", " "), "changing name")
            await asyncio.sleep(1)
            await SEND(ch, "You changed the name correctly.")
            FUN_ROLES[msgback.replace("_", " ")] = neededrole
            return  

        #purge any role
        if msg.startswith("purge role", 1):
            if msgback.replace("_"," ") in FUN_ROLES:
                neededrole = FUN_ROLES[msgback]
            else:
                await SEND(ch, "You cannot obliterate this role through my commands.")
                return
                
            await PURGE_ROLES(neededrole)
            await asyncio.sleep(1)
            await SEND(ch, "The role is gone.")
            return  

        #remove ckr
        if msg.startswith("ckr from ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split2[2]:
                    await SEND(ch, "I took the Chat Killer Role away from " + split2[2])
                    await asyncio.sleep(1)
                    await REMOVE_ROLES(mem,CKR)
                    break
            return   

        #resets the rig tracker message
        if msg.startswith("reset rig tracker", 1):
            await EDIT_MESSAGE(RIGTRACKER, "**RIGS TRACKER**,\nPATRON: 0,\nJOKER: 0,\nWICKED: 0,\nKEEPER: 0,\nHACKER: 0,\nTHIEF: 0,\nSPECTRE: 0,\nARCHON: 0,\nDRIFTER: 0,\nHERETIC: 0,\nCHAMELEON: 0")
            return

        #edits db rig tracking count for specific alignment
        if msg.startswith("edit tracker ", 1):
            track = msgback

            db.set(track + "uses", msg.split(" ", 3)[3])  #edit tracker patron 2 
            return


        #quiz
        if msg.startswith("quiz",1):
            if split[1] == "new":
                qSplit = split[2].split("|")
                if len(qSplit) != 7:
                    await SEND(ch,"Question does not have the required 7 sections.")
                else:
                    add_entry("quiz",split[2])
                    await SEND(ch,"Successfully added new quiz question")

            elif split[1] == "amount":
                await SEND(ch,"There are " + str(get_amount_of_entries("quiz")) + " questions in the database.")        

            elif split[1] == "print":
                question = show_specific_entry("quiz",int(split[2]))
                qSplit = question.split("|")
                toSend = "Q:\n" + qSplit[0] + "\nCorrect Answer:\n" + qSplit[1]
                toSend += "\nA2:\n" + qSplit[2] + "\nA3:\n" + qSplit[3] + "\nA4:\n" + qSplit[4]
                toSend += "\nGood response:\n" + qSplit[5] + "\nBad response:\n" + qSplit[6]
                await SEND(ch,toSend)

            elif split[1] == "delete":
                delete_entry("quiz",int(split[2]))
                await SEND(ch,"Question at index " + split[2] + " has been deleted." )

            return

        key = split[1]
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
            add_entry(key,split[2])
            await SEND(ch,"New " + split[1] + " " + tot + " added.")
            return

        #list tips
        if msg.startswith("l",1):
            await SEND(ch,split[1] + " " + tot + "(s):")
            await PRINT_ENTRIES(ch, key)
            return
            
        #delete tip
        if msg.startswith("d",1):
            delete_entry(key,int(split[2]))
            await SEND(ch,split[1] + " " + tot + "(s):")
            await PRINT_ENTRIES(ch, key)
            return
               
### RUN THE BOT ###
client.run(os.environ['TOKEN'])
