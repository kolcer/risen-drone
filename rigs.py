import time
import datetime

from views import *
from globals import *
from rated import *
from roles import *
from database import *
from redis import *
from discord.ext import commands

# ---VIEWS---

# class CastAgain(discord.ui.View):  was added mostly for Zero. But I locked the role. Also it was my first experiment with buttons.
#     async def on_timeout(self):
#         for item in self.children:
#             item.disabled = True

#         self.caster = None
#         self.channel = None
#         self.type = None

#         await EDIT_VIEW_MESSAGE(self.message, self.message.content, self)

#     @discord.ui.button(label="Cast again!", custom_id = "Recast", style = discord.ButtonStyle.primary)
#     async def casting(self, interaction: discord.Interaction, button: discord.ui.Button):
#         usr = interaction.user
#         if usr == self.caster:
#             await Rig(self.type, self.channel, self.caster)
#             self.stop()
#         else:
#             await INTERACTION(interaction.response, "You did not cast this rig.", True)

# ---END VIEWS---

def rigImmunity(usr1, usr2, fullImmunity):
    if fullImmunity: 
        for roles in usr1.roles:
            if roles.name in FULL_IMMUNITY_ROLES:
                return True
        if usr1 == usr2:
            return True
        return False
    else:
        for roles in usr1.roles:
            if roles.name in BASIC_IMMUNITY_ROLES:
                return True
        if usr1 == usr2:
            return True
        return False
    
def isNewUser(usr):
    if (not EXTRA_ROLES['climber'] in usr.roles) and (not EXTRA_ROLES['manuallyverified'] in usr.roles):
        True
    else:
        False

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


async def necromancer(channel):
 
    if RIG_DATA['ghostMsg'] != "hehehehaw":
        await SEND(channel, RIG_DATA['ghostMsg'])
    else:
        await SEND(channel, "*but nobody came...*")

async def muggle(channel, user):
    if MORPHABLE_ROLES["Muggle"][0] in user.roles:
        await SEND(channel, "You knew there wasn't a rig for Muggle and in fact there isn't one.")
    else:
        await SEND(channel, "You thought there was a rig for Muggle but there wasn't.")

async def Rig(rigType, ch, usr):
    newRigType = rigType
    msgCounting = None
    today = datetime.date.today()
 
    # if rigType.lower() == "splicer": no longer a secret :(
    #     if str(usr.id) not in list_decoded_entries("Splicer"):
    #         await SEND(ch, "The Splicer main has not given you permissions to cast this rig yet.")
    #         return
   
    if RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]]:
        await SEND(ch, "Ultimate spells are in cooldown.")
        return
        
    spamCount = 0
    if usr in RIG_SPAMMERS:
        spamCount = RIG_SPAMMERS[usr]
    
    if rigType in LIMITED_USE_RIGS:
        if spamCount == 2:
            await SEND(ch, "You should take a break.")
            return
        else:
            spamCount += 1
            RIG_SPAMMERS[usr] = spamCount
            
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = True

    if DETAILED_ROLES["nonerig"]:
        DETAILED_ROLES["nonerig"] = False
        newRigType = "noneified"

    # await updateRigTracker(rigType)
    messageAppend = "."
    msgCountingContent = ""
    match newRigType:
        case "heretic":
            if EXTRA_ROLES['murdurator'] in usr.roles:
                await SEND(ch, "You cast Heretic Rig but thanks to your Unbeliever rank, you didn't get possessed.")
                RIG_COOLDOWNS["self"] = False
                return

            #for member in SERVER_DATA['server'].members:
               # if EXTRA_ROLES['possessed'] in member.roles:
                   # await SEND(ch, "Another ultimate spell is in progress. Please wait.")
                   # RIG_COOLDOWNS["ha"] = False
                   # return
            await ADD_ROLES(usr, EXTRA_ROLES['possessed'])
            await asyncio.sleep(1)

            if EXTRA_ROLES['hypno'] in usr.roles:
                msgCounting = await SEND(ch,"You accidentally walked backwards and triggered a Heretic Rig!"
                                "\nMaybe someone could give you some Mana?")
            else:
                msgCounting = await SEND(ch,"You cast Heretic Rig but as a result you ended up getting Possessed..."
                                "\nMaybe someone could give you some Mana?")
                
            msgCountingContent = msgCounting.content
            await EDIT_MESSAGE(msgCounting, msgCountingContent + f"\n\n*Cooldown ends* <t:{round(time.time() + 120)}:R>")
            await asyncio.sleep(60)
            await REMOVE_ROLES(usr, EXTRA_ROLES['possessed'])
            
        case "wicked":
            rigActive = False
            for active in ACTIVE_RIGS.values():
                if active:
                    rigActive = True
                    break
            if not rigActive:
                await SEND(ch, "Nothing to destroy.")
                RIG_COOLDOWNS["meddle"] = False
                return
            msgCounting = await SEND(ch, "You cast Wicked Rig and destroyed all the nasty stairs along with your roles!")
            for rig in ACTIVE_RIGS.keys():
                ACTIVE_RIGS[rig] = False

            if not EVENTS["Easter"]:
                role_list = []
                for role in usr.roles:
                    if (role.name in MORPHABLE_ROLES or role.name in PING_ROLES) and role.name != "Wicked":
                        role_list.append(role)
                #TODO: Rolo, check if we can use REMOVE_ROLES() function here...
                await usr.remove_roles(*role_list)
                await asyncio.sleep(1)

            if MORPHABLE_ROLES["Wicked"][0] not in usr.roles and not EVENTS["Easter"]:
                await ADD_ROLES(usr, MORPHABLE_ROLES["Wicked"][0])
            
         
        case "drifter":
            im = usr.display_name[::-1]
            await EDIT_NICK(usr, im)
            msgCounting = await SEND(ch, "You cast Drifter Rig but you were looking the other way, causing your name to be reversed...")
            
        case "archon":
            if ch.name not in CHANNELS:
                await SEND(ch, "Impossible to create a Gate here. This channel is restricted.")
                RIG_COOLDOWNS["chat"] = False
                return
            ch2 = ch

            while True:
                ch2 = random.choice(list(CHANNELS.values()))

                if (ch2.name != ch.name) and (ch2.name not in SECRET_CHANNELS):
                    break

            firstmsg = await SEND(ch, "You cast Archon Rig and created a Gate in another channel!")
            await SEND(ch, "https://giphy.com/gifs/jiSabjDlIahx2P1xI0")
            await asyncio.sleep(3)
            secondmsg = await SEND(ch2, usr.mention + " has just created a Gate in this channel! They come from "
                + firstmsg.jump_url + ".")
            await SEND(ch2, "https://giphy.com/gifs/BdtSfK2OBGu3tKyvJF")
            await asyncio.sleep(3)
            await EDIT_MESSAGE(firstmsg, firstmsg.content + " " + secondmsg.jump_url)     
        
        case "hacker":
            nameInList = list(usr.display_name)
            random.shuffle(nameInList)
            im = ''.join(nameInList)
            # im = "".join(random.sample(usr.nick, len(usr.nick)))
            msgCounting = await SEND(ch, "You cast Hacker Rig an- ####01111001##à#01101111###01110101###01110010#00100000###01101110#01100001#01101101#01100101#00100000#01101001#01110011#00100000####à01101110#01101111#01110111#00100000#01110010#01100001#01101110#01100100##01101111#01101101#01101001#01111010#01100101#01100100#00100001")
            await asyncio.sleep(3)
            await EDIT_NICK(usr, im)
            
        case "keeper":
            im = ''.join(sorted(usr.display_name))
            await EDIT_NICK(usr, im)
            await asyncio.sleep(1)
            msgCounting = await SEND(ch, "You cast Keeper Rig and now your name follows a logic order!")
        
        case "patron":
            possessedRole = EXTRA_ROLES['possessed']
            hypnoRole = EXTRA_ROLES['hypno']
            for member in SERVER_DATA['server'].members:
                if possessedRole in member.roles:
                    await REMOVE_ROLES(member, possessedRole)
                elif hypnoRole in member.roles:
                    await REMOVE_ROLES(member, hypnoRole)

            msgCounting = await SEND(ch, "You cast Patron Rig and set up Mana Rigs all over the server!")

        case "reaver":
            length = len(usr.display_name)
            half = length // 2

            if random.randint(1, 2) == 1:
                # Mirror the first half
                to_mirror = usr.display_name[:half]
                mirrored = to_mirror + to_mirror[::-1]
            else:
                # Mirror the second half
                to_mirror = usr.display_name[half:]
                mirrored = to_mirror + to_mirror[::-1]

            await EDIT_NICK(usr, mirrored)

            msgCounting = await SEND(ch, "You cast Reaver Rig and placed a mirror in your name!")

        case "janitor":
            if MORPHABLE_ROLES["Janitor"][0] not in usr.roles:
                await SEND(ch, "You are not skilled enough to cast Janitor Rig.")
                RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = False
                return

            activeFound = False
            for i, v in RIG_COOLDOWNS.items():
                if v and i != 'janitor':
                    activeFound = True
                    break

            if activeFound:
                for rig in ACTIVE_RIGS:
                    ACTIVE_RIGS[rig] = False 

                for rig in DETAILED_RIGS:
                    DETAILED_RIGS[rig][0] = None
                    DETAILED_RIGS[rig][1] = None

                for cooldown in RIG_COOLDOWNS:
                    RIG_COOLDOWNS[cooldown] = False

                msgCounting = await SEND(ch, "You cast Janitor Rig and cleaned up all active cooldowns!")
            else:
                RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = False
                await SEND(ch, "The are no loose ends in need of cleaning.")
                return
            
        case "noneified":
            msgCounting = await SEND(ch, "nonealtevent")
                
        case ("joker"|"thief"|"spectre"|"splicer"|"gremlin"|"none"):

            ACTIVE_RIGS[rigType] = True
            RIG_DATA['rigCaster'] = usr
            if rigType == "joker":
                msgCounting = await SEND(ch, usr.mention + " just cast Joker Rig! Someone will be in for a treat.")
            elif rigType == "thief":
                msgCounting = await SEND(ch, usr.mention + " just cast Thief Rig! Hold tight your belongings.")
            elif rigType == "spectre":
                msgCounting = await SEND(ch, usr.mention + " just cast Spectre Rig! Watch your step.")
            elif rigType == "splicer":
                msgCounting = await SEND(ch, usr.mention + " just cast Splicer Rig! Careful.")
            elif rigType == "gremlin":
                DETAILED_ROLES["hnightmare"]["caster"] = usr
                msgCounting = await SEND(ch, usr.mention + " just cast Gremlin Rig! Be on guard.")
            elif rigType == "none":
                DETAILED_ROLES["nonerig"] = True
                msgCounting = await SEND(ch, usr.mention + " just cast None Rig! This better not-")
        
        # case "gun":
        #     if not MORPHABLE_ROLES["Guns"][0] in usr.roles:
        #         await SEND(ch, "no gun imagine lmao")
        #         return
        #     ACTIVE_RIGS['gun'] = True
        #     RIG_DATA['rigCaster'] = usr
        #     msgCounting = await SEND(ch, usr.mention + " just cast Gun Rig! I was forced to do this.")
        
        # case "impostor":
        #     ACTIVE_RIGS['impostor'] = True
        #     RIG_DATA['rigCaster'] = usr
        #     msgCounting = await SEND(ch, f"{usr.mention} just cast Impostor rig, I guess... ?")
                
    theCooldown = COOLDOWN_DURATION[rigType]

    if newRigType != "archon" and newRigType != "heretic":
        msgCountingContent = msgCounting.content
        await EDIT_MESSAGE(msgCounting, msgCountingContent + f"\n\n*Cooldown ends* <t:{round(time.time() + theCooldown)}:R>")

    await asyncio.sleep(theCooldown)

    if newRigType != "archon":
        await EDIT_MESSAGE(msgCounting, msgCountingContent)

    if newRigType in LIMITED_USE_RIGS and ACTIVE_RIGS[newRigType]:
        ACTIVE_RIGS[rigType] = False
        messageAppend = ", and the current Rig effect has worn off."
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = False

    await SEND(ch, f"{rigType.capitalize()} Rig cooldown is over{messageAppend}")
    
    #reset spam 
    if today.day == 1 and today.month == 4:
        await asyncio.sleep(300)
    else:
        await asyncio.sleep(3600)

    if usr in RIG_SPAMMERS and spamCount == RIG_SPAMMERS[usr]:
        del RIG_SPAMMERS[usr]      

async def CastRig(rigPick,ch,usr):
    # easterRng = None
    randomRig = ""
    randomAttempts = 0
    # chameleonSuccess = True
    today = datetime.date.today()

    if rigPick not in RIG_LIST:
        await SEND(ch, "That's not a valid rig. Type `bd help` to check which rigs you can cast.")

        if EVENTS["Easter"] and not str(usr.id) in list_decoded_entries("None Egg"):
            await add_egg_with_check("None Egg", usr)
            await SEND(ch, f"{usr.mention} found the None Egg lying on the ground.")
        return
    
    if MORPHABLE_ROLES["Gun"][0] in usr.roles and rigPick != "gun":
        await SEND(ch, "Would you look at that. A gun trying to cast a rig.")
        return

    if ch.id not in [750060041289072771, 813882658156838923]:
        rigPick = "heretic"

    if today.day == 1 and today.month == 4:
        rigPick = "joker"
        COOLDOWN_DURATION["joker"] = 90
    else:
        COOLDOWN_DURATION["joker"] = 600

    
    # if MORPHABLE_ROLES[rigPick.capitalize()] in usr.roles:
    #     easterRng = random.randint(0, EGG_RNG[rigPick] // 2)
    # else:
    #     easterRng = random.randint(0, EGG_RNG[rigPick])

    if rigPick == "chameleon":
        cd = False
        for i, v in RIG_COOLDOWNS.items():
            if v and i != 'janitor':
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
            await SEND(ch, " One or more rigs are still in cooldown. \n" + cdList)
            # chameleonSuccess = False
            return

        await SEND(ch, "What will it be? 🥁🥁🥁")
        await asyncio.sleep(4)

        while True:
            randomRig = random.choice(RIG_LIST)

            if randomAttempts == 3:
                await SEND(ch, "You know what. We can do without these rigs right now.")
                # chameleonSuccess = False

                if not str(usr.id) in list_decoded_entries("Rig Failure"):
                    await add_entry_with_check("Rig Failure", usr)
                    return
                break
            
            elif randomRig in RANDOM_BLACKLIST:
                if randomAttempts == 0:
                    await SEND(ch, "No, that's not it. Let me try again. Suspense!! 🥁🥁")
                elif randomAttempts == 1:
                    await SEND(ch, "We can't have this one either. The next outcome will surprise you! 🥁")
                elif randomAttempts == 2:
                    await SEND(ch, "Anything could happen now.")
                
                randomAttempts = randomAttempts + 1
                await asyncio.sleep(4)

            elif usr in RIG_SPAMMERS and RIG_SPAMMERS[usr] == 2 and randomRig in LIMITED_USE_RIGS:
                await SEND(ch, "Considering you are on a break, we should reserve this one for another time. Behold... 🥁")
                randomAttempts = randomAttempts + 1
                await asyncio.sleep(4)
            else:
                break

        if randomAttempts < 3:   
            await Rig(randomRig,ch,usr)
        return

    # if not (rigPick == "chameleon" and not chameleonSuccess):
    #     if easterRng == 0 and (rigPick == "chameleon" and chameleonSuccess):
    #         if not str(usr.id) in list_decoded_entries(f"{rigPick.capitalize()} Egg"):
    #             await add_egg_with_check(f"{rigPick.capitalize()} Egg", usr)
    #             await SEND(ch, EGGS[rigPick].format(user=usr.mention))

    LAST_RIG[usr.id] = str(rigPick) + " Rig"

    if rigPick == "necromancer":
        await necromancer(ch)
        return
    
    if rigPick == "muggle":
        await muggle(ch, usr)
        return

    await Rig(rigPick,ch,usr)
    return

async def ExecuteThiefRig(ch,usr):
    isMurdurator = False
    victim = usr.display_name

    if (ch.name not in CHANNELS) or isNewUser(usr) or rigImmunity(usr, RIG_DATA['rigCaster'], False) or (MORPHABLE_ROLES["Gun"][0] in usr.roles): #or len(RIG_DATA['rigCaster'].display_name + ", " + usr.display_name) > 32:
        return

    ACTIVE_RIGS["thief"] = False

    for roles in usr.roles:
        if roles.name in FULL_IMMUNITY_ROLES:
            isMurdurator = True
            break

    if not isMurdurator:       
        NickDictionary[usr] = "N/A"
        await EDIT_NICK(usr, "N/A")

    await asyncio.sleep(1)

    await SEND(ch, RIG_DATA['rigCaster'].mention + " has just stolen your name for 5 minutes!")

    if len(RIG_DATA['rigCaster'].display_name + "," + victim) > 32:
        await SEND(CHANNELS["bot-commands"], RIG_DATA['rigCaster'].mention + " someone fell for your Thief Rig, but your name is too long to include their name. I'll wipe it out. (Old name: `" + RIG_DATA['rigCaster'].display_name + "`)")
        await asyncio.sleep(1)
        await EDIT_NICK(RIG_DATA['rigCaster'], victim)
    else:
        await EDIT_NICK(RIG_DATA['rigCaster'], RIG_DATA['rigCaster'].display_name + "," + victim)

    if not isMurdurator: 
        await asyncio.sleep(300) #300#1800 
        del NickDictionary[usr]

    return


async def ExecuteSpectreRig(ch,usr, message):
    if (ch.name not in CHANNELS) or rigImmunity(usr, RIG_DATA['rigCaster'], True) or isNewUser(usr):
        return
    
    ACTIVE_RIGS["spectre"] = False

    chances = random.randint(0, 1)

    if chances == 1:
        await SEND(ch, RIG_DATA['rigCaster'].mention + " has made your message disappear with a 50% chance!")
        await DELETE(message)
        return

    await SEND(ch, RIG_DATA['rigCaster'].mention + " has NOT made your message disappear with a 50% chance.")
    return

# async def ExecuteGunRig(ch,usr,message):
#     if ch.name not in CHANNELS or rigImmunity(usr, RIG_DATA['rigCaster']) or not EXTRA_ROLES['climber'] in usr.roles or MORPHABLE_ROLES['Guns'] in usr.roles:
#         return
#     ACTIVE_RIGS["gun"] = False

#     # shoot message pew pew

#     await MorphTo(usr, "Gun")
#     await SEND(ch, f"{RIG_DATA['rigCaster'].mention}, someone fell for your trap! They are now a gun!")
#     await asyncio.sleep(300)
#     await DemorphFrom(usr, "Gun")
#     return

async def ExecuteJokerRig(ch,usr, message):

    if (ch.name not in CHANNELS) or isNewUser(usr) or ("http" in message.content) or (len(message.content) > 45):
        return

    ACTIVE_RIGS["joker"] = False

    msgcontent = message.content

    await DELETE(message)
    await asyncio.sleep(2)

    await SEND(ch, str(msgcontent) + " - " + ":nerd: :clown:\nFrom: " + usr.mention)
            
    return

async def ExecuteJokerRig(ch, usr, message):
    if (ch.name not in CHANNELS) or isNewUser(usr) or ("http" in message.content) or (len(message.content) > 45):
        return

    ACTIVE_RIGS["joker"] = False

    msgcontent = message.content

    to_line = ""
    if message.reference and message.reference.resolved:
        replied_msg = message.reference.resolved
        replied_user = replied_msg.author

        to_line = f"To: {replied_user.display_name}\n"

    await DELETE(message)
    await asyncio.sleep(2)

    await SEND(ch, f"{to_line}{msgcontent} - :nerd: :clown:\nFrom: {usr.mention}")
    return

async def ExecuteSplicerRig(ch,usr):
 
    if (ch.name not in CHANNELS) or isNewUser(usr) or rigImmunity(usr, RIG_DATA['rigCaster'], False) or (MORPHABLE_ROLES["Gun"][0] in usr.roles):
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

    toSend = RIG_DATA['rigCaster'].mention + " wants to splice their name with yours! Press a button to proceed.\n`" + usr.name + "`'s name will be: " + SPLICER_RIG["user-name"] + ".\n`" + RIG_DATA['rigCaster'].name + "`'s name will be: " + SPLICER_RIG["rigcaster-name"] + "."


    view = SplicerView(timeout = 100)
    message = await SEND_VIEW(ch, toSend, view)
    view.message = message
    view.toolate = True

    await view.wait()
    await view.too_late()

    # await ADD_REACTION(focusmsg, "❌")
    # await asyncio.sleep(1)
    # await ADD_REACTION(focusmsg, "✅")

    # await asyncio.sleep(60)
    # if SPLICER_RIG["active"]:
    #     SPLICER_RIG["user"] = None
    #     SPLICER_RIG["answer"] = None
    #     SPLICER_RIG["active"] = False
    #     SPLICER_RIG["reactionmessage"] = None
    #     SPLICER_RIG["user-name"] = ""
    #     SPLICER_RIG['rigcaster-name'] = ""
            
    return

async def ExecuteGremlinRig(ch,usr):
    if (ch.name not in CHANNELS) or rigImmunity(usr, RIG_DATA['rigCaster'], True) or isNewUser(usr) or EXTRA_ROLES['hypno'] in usr.roles:
        return

    ACTIVE_RIGS["gremlin"] = False
    DETAILED_ROLES["hnightmare"][usr.id] = DETAILED_ROLES["hnightmare"]["caster"]

    await ADD_ROLES(usr, EXTRA_ROLES['hypno'])
    await asyncio.sleep(1)

    if not EVENTS["Easter"]:
        role_list = []
        for role in usr.roles:
            if (role.name in MORPHABLE_ROLES):
                role_list.append(role)
        #TODO: Rolo, check if we can use REMOVE_ROLES() function here...
        await usr.remove_roles(*role_list)
        await asyncio.sleep(1)

    await SEND(ch, RIG_DATA['rigCaster'].mention + " has hypnotized you! You don't feel too good...")
            
    return

# async def GiveMana(ch,usr,message):
 
#     role = EXTRA_ROLES['possessed']
#     hypnoRole = EXTRA_ROLES['hypno']

#     if (role in message.author.roles) and ch.id != 813882658156838923:
#         await SEND(message.channel, "How silly of me. It seems I have forgotten to cover this area. Nice try though!")
#         return

#     split_message = message.content.split(" ", 3)
#     target = split_message[3].lower()
#     for member in SERVER_DATA['server'].members:
#         if member.name.lower() == target:
#             if role in member.roles:
#                 await SEND(message.channel, member.display_name + " has received some Mana and is no longer Possessed!")
#                 await asyncio.sleep(3)
#                 await REMOVE_ROLES(member, role)
#                 await asyncio.sleep(1)
#                 if not str(usr.id) in list_decoded_entries("Heretic Defier"):
#                     await add_entry_with_check("Heretic Defier", usr)
#             elif hypnoRole in member.roles:
#                 if usr.id == member.id:
#                     await SEND(message.channel,"You accidentally stepped on a Patron Rig and freed yourself from hypnosis!")
#                 else:
#                     await SEND(message.channel, member.display_name + " has received some Mana and is no longer Hypnotized!")

#                 await asyncio.sleep(3)
#                 await REMOVE_ROLES(member, hypnoRole)
#                 await asyncio.sleep(1)
#             else:
#                 await SEND(message.channel,
#                     member.display_name +
#                             " refused to get your Mana."
#                         )
#             return
#     await SEND(message.channel,
#         "Who are you trying to share your Mana with?")
#     return