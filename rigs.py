from globals import *
from rated import *
from roles import *
from globals import *
from database import *


def rigImmunity(usr1, usr2):
    for roles in usr1.roles:
        if roles.name in IMMUNITY_ROLES:
            return True
    if usr1 == usr2:
        return True
    return False


async def updateRigTracker(rigType):
    initialmsg = RIG_DATA['rigTracker'].content
    blankmsg = initialmsg.replace("\n","").split(",")
    currentnumber = None
    finalmsg = ""
    counter = 0

    for i in blankmsg:
        counter += 1
        if rigType.upper() in i:
            #currentnumber = i.split(" ")[1].replace(",","")
            currentnumber = db.get(rigType.lower() + "uses")

            #i = i.replace(currentnumber, str(int(currentnumber) + 1))
            db.set(rigType.lower() + "uses", int(currentnumber) + 1)
            newnumber = db.get(rigType.lower() + "uses").decode("utf-8")
            i = i.replace(i.split(" ")[1].replace(",",""), str(newnumber))

            finalmsg += i + ",\n"
        else:
            if counter == 12:
                finalmsg += i + "\n"
            else:
                finalmsg += i + ",\n"

    await EDIT_MESSAGE(RIG_DATA['rigTracker'], finalmsg)


async def necromancer(message):
 
    if RIG_DATA['ghostMsg'] != "":
        await SEND(message, RIG_DATA['ghostMsg'])
    else:
        await SEND(message, "*but nobody came...*")


async def Rig(rigType, ch, usr):
 
    if rigType.lower() == "splicer":
        if not FUN_ROLES["Splicer"] in usr.roles:
            await SEND(ch, "You are not able to cast this rig yet!")
            return
   
    if RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]]:
        await SEND(ch, "Ultimate spells are in cooldown.")
        return
        
    spamCount = 0
    if usr in RIG_SPAMMERS:
        spamCount = RIG_SPAMMERS[usr]
    
    if rigType in LIMITED_USE_RIGS:
        if spamCount == 2:
            await SEND(ch, "You've been using these commands too often.")
            return
        else:
            spamCount += 1
            RIG_SPAMMERS[usr] = spamCount
            
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = True
    
    await updateRigTracker(rigType)
    messageAppend = "."
    match rigType:
        
        case "heretic":
            if EXTRA_ROLES['murdurator'] in usr.roles:
                await SEND(ch, "You cast Heretic Rig but thanks to your Unbeliever rank, you didn't get possessed.")
                RIG_COOLDOWNS["ha"] = False
                return

            #for member in SERVER_DATA['server'].members:
               # if EXTRA_ROLES['possessed'] in member.roles:
                   # await SEND(ch, "Another ultimate spell is in progress. Please wait.")
                   # RIG_COOLDOWNS["ha"] = False
                   # return
            await ADD_ROLES(usr, EXTRA_ROLES['possessed'])
            await asyncio.sleep(1)
            await SEND(ch,"You cast Heretic Rig but forgot to unlock Unbeliever rank first and ended up getting Possessed..."
                       "\nMaybe someone could give you some Mana?")
            await asyncio.sleep(60)
            await REMOVE_ROLES(usr, EXTRA_ROLES['possessed'])
            
        case "wicked":
            role_list = []
            for role in usr.roles:
                if role.name in MORPHABLE_ROLES or role.name in PING_ROLES:
                    role_list.append(role)
            #TODO: Rolo, check if we can use REMOVE_ROLES() function here...
            await usr.remove_roles(*role_list)       
            await SEND(ch, "You cast Wicked Rig but forgot to unlock Devil rank first and ended up purging all your roles!")
         
        case "drifter":
            im = usr.display_name[::-1]
            await EDIT_NICK(usr, im)
            await SEND(ch, "You cast Drifter Rig but forgot to unlock Voyager rank first and now your name is reversed...")
            
        case "archon":
            if ch.name not in CHANNELS:
                await SEND(ch, "Impossible to create a Split here. This channel is restricted.")
                RIG_COOLDOWNS["ha"] = False
                return
            ch2 = ch
            while ch2 == ch or ch2.name == "bot-testing":
                ch2 = random.choice(list(CHANNELS.values()))
            firstmsg = await SEND(ch, "You cast Archon Rig and created a Split in another channel!")
            await SEND(ch, "https://media.giphy.com/media/LUjKnselKZBc5Zb4t4/giphy.gif")
            await asyncio.sleep(3)
            secondmsg = await SEND(ch2, usr.mention + " has just created a Split in this channel! They come from "
                + ch.mention + ". " + firstmsg.jump_url)
            await SEND(ch2, "https://media.giphy.com/media/QM1yEJoR1Z7oKAGg4Y/giphy.gif")
            await asyncio.sleep(3)
            await EDIT_MESSAGE(firstmsg, firstmsg.content + " " + secondmsg.jump_url)           
        
        case "hacker":
            im = ""
            for i in range(8):
                temp = str(random.randint(0, 1))
                im += temp
            await SEND(ch, "You cast Hacker Rig an- anddd##dddddddd#############")
            await asyncio.sleep(3)
            await EDIT_NICK(usr, im)
            if usr.display_name == '00000000':
                await SEND(ch, "You truly deserve the Zero rank.")

                if FUN_ROLES["Zero"] not in usr.roles:
                    await ADD_ROLES(usr, FUN_ROLES["Zero"])
            
        case "keeper":
            im = ''.join(sorted(usr.display_name))
            await EDIT_NICK(usr, im)
            await asyncio.sleep(1)
            await SEND(ch, "You cast Keeper Rig and now your name follows a logic order!")
        
        case "patron":
            rigActive = False
            for active in ACTIVE_RIGS.values():
                if active:
                    rigActive = True
                    break
            if not rigActive:
                await SEND(ch, "It would be useless casting this spell now.")
                RIG_COOLDOWNS["patron"] = False
                return
            await SEND(ch, "You cast Patron Rig and restored the Server!")
            for rig in ACTIVE_RIGS.keys():
                ACTIVE_RIGS[rig] = False
                
        case ("joker"|"thief"|"spectre"|"splicer"):#

            ACTIVE_RIGS[rigType] = True
            RIG_DATA['rigCaster'] = usr
            if rigType == "joker":
                await SEND(ch, usr.mention + " just cast Joker Rig! Someone will be in for a treat.")
            elif rigType == "thief":
                await SEND(ch, usr.mention + " just cast Thief Rig! Hold tight your belongings.")
            elif rigType == "spectre":
                await SEND(ch, usr.mention + " just cast Spectre Rig! Watch your step.")
            else:
                await SEND(ch, usr.mention + " just cast Splicer Rig! Careful.")
                
          
            
    await asyncio.sleep(COOLDOWN_DURATION[rigType])

    if rigType in LIMITED_USE_RIGS and ACTIVE_RIGS[rigType] == True:
        ACTIVE_RIGS[rigType] = False
        messageAppend = ", and the current Rig effect has worn off."
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = False

    if HERETIC_DISABLED[0] and rigType.lower() == "heretic":
        RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = True

    await SEND(ch, rigType.capitalize() + " Rig cooldown is over" + messageAppend)
    
    #reset spam count
    await asyncio.sleep(3600)
    if usr in RIG_SPAMMERS and spamCount == RIG_SPAMMERS[usr]:
        del RIG_SPAMMERS[usr]


async def SplicerRig(reaction,user):
 
    if user == SPLICER_RIG["user"] and SPLICER_RIG["active"] == True and reaction.message == SPLICER_RIG["reactionmessage"]:
        if reaction.emoji == "❌":
            SPLICER_RIG["user"] = None
            SPLICER_RIG["answer"] = None
            SPLICER_RIG["active"] = False
            SPLICER_RIG["reactionmessage"] = None
            SPLICER_RIG["user-name"] = ""
            SPLICER_RIG['rigcaster-name'] = ""
  
            await SEND(reaction.message.channel, "Splice request declined. That's too bad.")
        elif reaction.emoji == "✅":
            await EDIT_NICK(user, SPLICER_RIG["user-name"])
            await asyncio.sleep(1)
            await EDIT_NICK(RIG_DATA['rigCaster'], SPLICER_RIG['rigcaster-name'])

            await SEND(reaction.message.channel, "Splice request accepted. Enjoy your new display names.")

            
            SPLICER_RIG["user"] = None
            SPLICER_RIG["answer"] = None
            SPLICER_RIG["active"] = False
            SPLICER_RIG["reactionmessage"] = None
            SPLICER_RIG["user-name"] = ""
            SPLICER_RIG['rigcaster-name'] = ""
            

async def CastRig(rigPick,ch,usr):

    if rigPick not in RIG_LIST and rigPick != "necromancer" and rigPick != "chameleon":
        await SEND(ch, "That is not a valid rig. Try again.")
        return
    
    if MORPHABLE_ROLES["Guns"][0] in usr.roles:
        await SEND(ch, "Would you look at that. A gun trying to cast a rig.")
        return

    if ch != CHANNELS["bot-commands"] and ch != CHANNELS["bot-testing"]:
        rigPick = "heretic"
    
    if rigPick == "heretic" and HERETIC_DISABLED[0]:
        await SEND(ch, "Heretic Rig is currently disabled. The bot is restarting soon and I wouldn't want you to be stuck with the Possessed role.")
        return

    if rigPick == "chameleon":
        cd = False
        for active in RIG_COOLDOWNS.values():
            if active:
                cd = True
                break
        if cd:
            cdList = ""
            for i, v in RIG_COOLDOWNS.items():
                cdList += COOLDOWN_DESCRIPTIONS[i]
                if v:
                    cdList += ":x: \n"
                else:
                    cdList += ":white_check_mark: \n"
            await SEND(ch, " All cooldowns must be over for this Rig to take place. \n" + cdList)
            return

        await SEND(ch, "*drum roll*")
        await asyncio.sleep(4)
        await Rig(random.choice(RIG_LIST),ch,usr)
        return

    LAST_RIG[usr] = str(rigPick) + " Rig"

    if rigPick == "necromancer":
        await necromancer(ch)
        return

    await Rig(rigPick,ch,usr)
    return

async def ExecuteThiefRig(ch,usr):

    tooLong = False
            
    if ch.name not in CHANNELS or not EXTRA_ROLES['climber'] in usr.roles or rigImmunity(usr, RIG_DATA['rigCaster']): #or len(RIG_DATA['rigCaster'].display_name + ", " + usr.display_name) > 32:
        return

                            
    if len(RIG_DATA['rigCaster'].display_name + ", " + usr.display_name) > 32:
        await SEND(CHANNELS["bot-commands"], RIG_DATA['rigCaster'].mention + " someone fell for your Thief Rig, but your name is too long to include their name. I'll wipe it out. (Old name: `" + RIG_DATA['rigCaster'].display_name + "`)")
        await asyncio.sleep(1)
        await EDIT_NICK(RIG_DATA['rigCaster'], ".")
        tooLong = True

    ACTIVE_RIGS["thief"] = False
    victim = usr.display_name

    NickDictionary[usr] = "N/A"

    if not usr.id == 481893862864846861:
        await EDIT_NICK(usr, "N/A")

    await asyncio.sleep(1)
            
    # if RIG_DATA['rigCaster'] in NickDictionary:
    #     if tooLong:
    #         NickDictionary[RIG_DATA['rigCaster']] = victim
    #     else:
    #         NickDictionary[RIG_DATA['rigCaster']] = RIG_DATA['rigCaster'].display_name + ", " + victim

    #     await EDIT_NICK(RIG_DATA['rigCaster'], NickDictionary[RIG_DATA['rigCaster']])
    #     await SEND(ch, RIG_DATA['rigCaster'].mention + " has just stolen your name for 5 minutes!")

    #     if tooLong == True:
    #         await asyncio.sleep(1)
    #         await EDIT_NICK(RIG_DATA['rigCaster'], RIG_DATA['rigCaster'].display_name.replace("., ","", 1))

    #     await asyncio.sleep(300) #300#1800 
    #     del NickDictionary[RIG_DATA['rigCaster']]

    #     return
                
    await EDIT_NICK(RIG_DATA['rigCaster'], RIG_DATA['rigCaster'].display_name + ", " + victim)
    await SEND(ch, RIG_DATA['rigCaster'].mention + " has just stolen your name for 5 minutes!")


    if tooLong == True:
        await asyncio.sleep(1)
        await EDIT_NICK(RIG_DATA['rigCaster'], RIG_DATA['rigCaster'].display_name.replace("., ","", 1))
            
    await asyncio.sleep(300) #300#1800 
    del NickDictionary[usr]
    return


async def ExecuteSpectreRig(ch,usr,message):
    if ch.name not in CHANNELS or rigImmunity(usr, RIG_DATA['rigCaster']) or not EXTRA_ROLES['climber'] in usr.roles:
        return
    ACTIVE_RIGS["spectre"] = False

    chances = random.randint(0, 1)

    if chances == 1:
        await SEND(ch, RIG_DATA['rigCaster'].mention + " has made your Message disappear with a 50% chance!")
        await DELETE(message)
        return

    await SEND(ch, RIG_DATA['rigCaster'].mention + " has NOT made your Message disappear with a 50% chance.")
    return


async def ExecuteJokerRig(ch,usr,message):

    if (ch.name not in CHANNELS) or (not EXTRA_ROLES['climber'] in usr.roles) or ("https" in message.content) or (len(message.content) > 45):
        return
    ACTIVE_RIGS["joker"] = False

    msgcontent = message.content

    await DELETE(message)
    await asyncio.sleep(2)

    await SEND(ch, str(msgcontent) + " -" + ":nerd::clown:\nFrom: " + usr.mention)
            
    return


async def ExecuteSplicerRig(ch,usr):
 
    if ch.name not in CHANNELS or not EXTRA_ROLES['climber'] in usr.roles or rigImmunity(usr, RIG_DATA['rigCaster']):
        return
                
    ACTIVE_RIGS["splicer"] = False

    SPLICER_RIG["active"] = True
    SPLICER_RIG["user"] = usr

    rcn = RIG_DATA['rigCaster'].display_name
    print(rcn)
    rcn1 = rcn[:len(rcn)//2]
    rcn2 = rcn[len(rcn)//2:]
    print(rcn1 + "/" + rcn2)

    usrn = usr.display_name
    print(usr)
    usrn1 = usrn[:len(usrn)//2]
    usrn2 = usrn[len(usrn)//2:]
    print(usrn1 + "/" + usrn2)


    SPLICER_RIG["user-name"] = usrn1 + rcn2
    # SPLICER_RIG["RIG_DATA['rigCaster']-name"] = rcn1 + usrn2 // why is a reference to RIG-DATA[] in a string? -roibrari
    SPLICER_RIG["rigcaster-name"] = rcn1 + usrn2
    print(SPLICER_RIG["user-name"])
    print(SPLICER_RIG["RIG_DATA['rigCaster']-name"])

    focusmsg = await SEND(ch, RIG_DATA['rigCaster'].mention + " wants to splice their name with yours! React to proceed.\n`" + usr.name + "#" + usr.discriminator + "`'s name will be: " + SPLICER_RIG["user-name"] + ".\n`" + RIG_DATA['rigCaster'].name + "#" + RIG_DATA['rigCaster'].discriminator + "`'s name will be: " + SPLICER_RIG["RIG_DATA['rigCaster']-name"] + ".")
    SPLICER_RIG["reactionmessage"] = focusmsg

    await ADD_REACTION(focusmsg, "❌")
    await asyncio.sleep(1)
    await ADD_REACTION(focusmsg, "✅")

    await asyncio.sleep(60)
    if SPLICER_RIG["active"]:
        SPLICER_RIG["user"] = None
        SPLICER_RIG["answer"] = None
        SPLICER_RIG["active"] = False
        SPLICER_RIG["reactionmessage"] = None
        SPLICER_RIG["user-name"] = ""
        SPLICER_RIG['rigcaster-name'] = ""
 

        await ADD_REACTION(focusmsg, "🛑")
            
    return


async def GiveMana(ch,usr,message):
 
    role = EXTRA_ROLES['possessed']

    if role in message.author.roles:
        await SEND(message.channel, "How silly of me. It seems I have forgotten to cover this area. Nice try though!")
        return

    split_message = message.content.split(" ", 3)
    target = split_message[3].lower()
    for member in SERVER_DATA['server'].members:
        if member.name.lower() + "#" + member.discriminator == target:
            if role in member.roles:
                await SEND(message.channel, member.display_name + " has received some Mana and is no longer Possessed!")
                await asyncio.sleep(3)
                # await member.remove_roles(role)
                await REMOVE_ROLES(member, role)
                await asyncio.sleep(1)
                if not FUN_ROLES["Heretic Defier"] in usr.roles:
                    await ADD_ROLES(usr, FUN_ROLES["Heretic Defier"])
            else:
                await SEND(message.channel,
                    member.display_name +
                            " received your Mana, but they do not seem to need it."
                        )
            return
    await SEND(message.channel,
        "Who are you trying to share your Mana with?")
    return

