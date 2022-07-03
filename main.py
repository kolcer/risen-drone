### IMPORTS ###

import discord
import os
import random
import asyncio
import redis
from datetime import date
from difflib import SequenceMatcher

## CONSTANTS ##

#chat killer requires 2 hours of inactivity(in seconds)
CHAT_KILLER_WAIT = 7200

#ids will be replaced with objects on startup
SERVER = 624227331720085528

#fallen drone name (to prevent impostors)
FALLEN_DRONE_NICK = "FALLEN DRONE"

#special roles
#roles that bot can assing to, but not by a regular user commannd
#values replaced by roles on startup
CKR = "Ultimate Chat Killer"
POSSESSED = "Possessed (rig)"
MURDURATOR = "Murdurators"
CLIMBER = "Climbers"

#this is for administrating tips and trivia database
ADMINS = [
    int(os.environ['USER1']),
    int(os.environ['USER2']),
    int(os.environ['USER3']),
    int(os.environ['USER4']),
    int(os.environ['USER5']),
    int(os.environ['USER6']),
] 

#channels where bot is allowed to post
CHANNELS = {
    "general": 624227331720085536,
    "bot-commands": 750060041289072771,
    "crazy-stairs": 750060054090219760,  
    "bot-testing": 813882658156838923,
}

#worst guns ever made for the gun role
WORST_GUNS = [
    "Cochran Turret Revolver",
    "Chauchat",
    "Nambu Type 94 Pistol",
    "Krummlauf",
    "2 mm Kolibri",
    "Glisenti Model 1910",
    "Davy Crockett",
    "Northover Projector",
    "Duck's Foot Pistol",
    "Puckle Gun",
    "Nock Volley Gun",
    "Grossflammenwerfer",
    "Gyrojet",
    "FP-45 Liberator"
    "Ross Rifle",
    "Arsenal AF2011-A1",
    "CZ-38",
    "LeMat Revolver",
    "Boys Anti-Tank Rifle",
    "No gun name for you",
]

#this is for tips and trivia database
TIPS_KEYS = [
    "patron", "joker", "wicked", "spectre", "keeper", "muggle", "chameleon",
    "thief", "hacker", "archon", "drifter", "heretic", "none", "general",
    "possessed", "architect",
]

#this roles can be assigned via a morph to command
#at 0 index we will put a role object during the login proccess.
#make sure indexes match role name in the server!
MORPHABLE_ROLES = {
    "Patron": [ 
        None,
        "Go help those noobs, you are now a Patron!",
        "What about protecting the noobs? Without a Patron around they will be lost.",
    ],
    "Joker": [ 
        None,
        "As if there weren't enough clowns here, you are now a Joker!",
        "Did you run out of jokes? The Joker guild will hear about this.",
    ],
    "Wicked": [ 
        None,
        "Unleash all your wickedness, you are now a Wicked!",
        "You destroyed everything and left nothing behind. Thank you for your services, a Wicked is not needed anymore.",
    ],
    "Spectre": [ 
       None,
       "Our quote's founder has been identified, you are now a Spectre",
       "Once again, Spectre's Founder went MIA.",
    ],
    "Keeper": [ 
       None,
       "The staircase is now under your supervision, you successfully became a Keeper.",
       "You failed to take care of the stairs, and so you are no longer a Keeper.",
    ],
    "Muggle": [ 
       None,
       "Work smarter, not harder. You are now a Muggle!",
       "The tower was too overwhelming for a weakling like you. Your Muggle license has been revoked.",
    ],
    "Chameleon": [ 
       None,
       "Do not let them know your next move, you are now a Chameleon!",
       "You had many options, yet you came back. You do not get to be a Chameleon anymore.",
    ],
    "Hacker": [ 
        None,
       "Welcome to the backdoor, you are now a Hacker!",
       "You tried to execute some code but as a result you accidentally removed your Hacker permissions.",
    ],
    "Thief": [ 
        None,
        "Is it really called borrowing? You are now a Thief!",
        "You actually gave me back the role? How generous. But also that doesn't make you a Thief anymore.",
     ],
    "Archon": [ 
        None,
        "Typo fixed, happy? You are now an Archon!",
        "Traveling between portals has been fun, but fun eventually comes to an end. You are no longer an Archon.",
     ],
     "Drifter": [ 
        None,
        "You took the elevator and rose to the top. You are now a Drifter.",
        "I saw you taking the stairs, you are no longer a Drifter.",
     ],
     "Heretic": [ 
        None,
        "We have banned dark magic, but you do not seem to care. You successfully became a Heretic.",
        "The circle has made their decision. You are permanently banned from being a Heretic ever again.",
    ],
     "Guns": [ 
        None,
        "smh, FINE!",
        "Finally you came to your senses.",
     ],
}

#not morphable roles
# 0 - role itself
# 1 - doesnt have role, and wants it
# 2 - has role, and wants it
# 3 - doesnt have role, and wants to remove it
# 4 - has role, and wants to remove it
SPECIAL_ROLES = {
    "Admin": [
        None,
        "You are now an Admin! ...Wait, what?",
        "How funny!",
        "You are no longer an Admin... You never were.",
        "I believe you could just go and do it yourself.",
    ],
    "Architect": [
        None,
        "You should boost the server if you crave for that role.",
        "You are already an Architect, smh.",
        "You are not an Architect...",
        "Just wait for the boost to expire.",
    ],
    "Climber": [
        None,
        "Please verify to become a climber.",
        "To the tower you go!",
        "You are no longer a Climber. Goodbye.",
        "You are no longer a Climber. Goodbye.",
    ],
    "Possessed": [
        None,
        "Wait for someone to cast a Heretic Rig",
        "You are already possessed...",
        "You are not possessed...",
        "Ask someone for mana",
    ],
    #multiple words (ultimate chat killer) would break the script logic
    "Ultimate": [
        None,
        "Your message needs to be last for 2 hours in the <#624227331720085536> channel.",
        "You have already killed the chat.",
        "You were not a chat killer in the first place.",
        "There was an attempt.",
    ],
}

#pingable roles, no custom messages
#roles will be fetched on bot startup
PING_ROLES = {
    "Announcements":
        None,
    "Events":
        None,
    "Polls":
        None,
    "Updates":
        None,
}
IMMUNITY_ROLES = ["Admin", "Murdurators"]

#bot will react to the webhook emoji, if it finds in a webhook message
#values will be replaced by emoji objects during startup
EMOJIS_TO_REACT = {
    "_patron": 758081038697103504,
    "_joker": 758081245157654599,
    "_wicked": 792143453035167754,
    "_keeper": 758081314912993283,
    "_muggle": 758081353932603414,
    "_hacker": 758081540063494288,
    "_thief": 758081386203840644,
    "_heretic": 786323224115281921,
    "_archon": 786323402172530688,
    "_drifter": 786323335880507483,
    "_spectre": 758083065988776017,
    "_chameleon": 758083033738903692,
    "csSleazelApproves": 791393163343560715,
    "csSecret": 786318938350813215,
    "csPranked": 786317086066343936,
    "csSuperSecret": 987709883010916383,
    "csMegaSecret": 987819430639730699,
}

#this keywords will trigger the bot with a single occurence
# value is the trigger, key is theresponse!
#it DOES NOT have to be a single word
SINGLE_WORD_TRIGGERS = {
    "<:cs_Stairbonk:812813052822421555>":
        'gun',
    "It needs to be earned, sorry.":
        'morph to ultimate chat killer',
    "Tsk.":
        'cstrollpain',
    "{mention} <:csRbxangryping:786325219727638535>":
        '827952429290618943',
}

#all words nedd to be present for this trigger to occur
#but the order of the words does not matter
MULTIPLE_WORD_TRIGGERS = {
    "Keeper obviously. Stop asking stupid questions.": 
        ["best", "alignment"], 
    "Please stop abusing the tutorial. Poor Sleazel can\'t sleep at night...":
        ['bug', 'tutorial'], 
    "Haha. You got stuck in stairs!":
        ['stuck', 'stairs'],
    "I fell, okay?":
        ['fallen', 'drone', 'how'],
    "Are you expecting me to answer with None?": 
        ['worst', 'alignment', '?'], 
    "Muggle Tower project has been cancelled. You can simulate it by managing the settings of a Custom Tower, instead.":
        ['when', 'muggle', 'tower', '?'], 
    "Thanks.":
        ['good', 'drone'], 
    "Nobody is perfect. Robots included.":
        ['bad', 'drone'],
    "Not on my watch.": 
        ['dead', 'chat'],
    "{mention} is a true stair jumper.":
        ["found", "secret", "badge"],
}

#first word is required and any of the pool of rest of the words
MIXED_WORD_TRIGGERS = {
    "Hello!":   [
        'fallen drone', 
        ["hi", "hello", "howdy", "sup"],
    ],
    "Wrong.": [
        'drone',
        ["dead", "down", "off", "vacation", "sleep"],
    ],    
}

IMPOSTOR_WARNINGS = [
    "It's time to stop.", "I took the liberty to change your name.",
    "Identity theft doesn't give you a good look.", "Do not try that again.",
    "There, I picked a fitting name for you.",
    "You've come a long way, phony me.",
    "There will be no phonies as long as I'm here.",
    "Copy me all you want, my knowledge is unparalleled.",
    "*Reversion of your actions is currently in progress...*",
    "I put an end to this buffoonery.", "Someone had to do it.",
    "We are through here.", "My disappointment is immeasurable.",
    "I do not speak like that.", "I am not fooled."
]

IMPOSTOR_NICKS = [
    "i am a thief",
    "my plan, foiled!",
    "unoriginal display name",
    "there was an attempt",
    "original display name",
    "funny name",
    "pin of shame",
    "could be better",
    "could be worse",
    "good job",
    "your prize",
    "Name offered by Me. F.D.",
]

RIG_LIST = [
    "thief",
    "spectre",
    "joker",
    "archon",
    "heretic",
    "patron",
    "wicked",
    "keeper",
    "hacker",
    "drifter",
]

COOLDOWN_SELECT = {
    "thief": "tsj",
    "spectre": "tsj",
    "joker": "tsj",
    "archon": "ha",
    "heretic": "ha",
    "patron": "patron",
    "wicked": "general",
    "keeper": "general",
    "hacker": "general",
    "drifter": "general",
}

COOLDOWN_DURATION = {
    "thief": 0, #cooldown embeded in rig effect
    "spectre": 0, #cooldown embeded in rig effect
    "joker": 0, #cooldown embeded in rig effect
    "archon": 120,
    "heretic": 60,
    "patron": 900,
    "wicked": 60,
    "keeper": 20,
    "hacker": 20,
    "drifter": 20,
}

LIMITED_USE_RIGS = [
    "joker",   
    "thief",
    "spectre",
]

COOLDOWN_DESCRIPTIONS = {
    "general": "General cooldown: ",
    "tsj": "Thief, Spectre, and Joker cooldown: ",
    "ha": "Heretic and Archon cooldown: ",
    "patron": "Patron cooldown: ",
}

### GLOBAL VARIABLES ###

# for chat killer role, time when the last message was sent
# (seconds from unix epoch)
Last = 0
rigCaster = None
ghostMsg = ""

ACTIVE_RIGS = {
    "joker": False,
    "thief": False,
    "spectre": False,
}

RIG_COOLDOWNS = {
    "general": False,
    "tsj": False,
    "ha": False,
    "patron": False,
}

RIG_SPAMMERS = {}
NickDictionary = {}
### INITIAL SETUP ###

# This allows us to know if user has updated their presence
# Mosty for the gun role nick change prevention
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Set up the data base
db = redis.from_url(os.environ.get("REDIS_URL"))

### PRIVATE SYNC FUNTIONS ###

def add_tip(key, new_tip):
    db.rpush(key,new_tip)

def delete_tip(key, index):
    db.lset(key,index,"_del_")
    db.lrem(key,1,"_del_")

def list_tips(key):
    result = db.lrange(key,0,-1)
    return result

def show_random_tip(key):
    index = random.randint(0,db.llen(key))
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")

def getScoldDictionary(victim, author):
    ScoldDict = {
        481893862864846861:
            "I am thankful to my creator, not disappointed.",
        827952429290618943:
            author.mention + " nice try.",
        828423681914437663:
            victim.mention + ", I am EXTREMELY disappointed in you. You know why. I do not forget.",
        author.id:
            author.mention + " you do not need Me to be disappointed in yourself.",
    }
    return ScoldDict

def rigImmunity(usr1, usr2):
    for roles in usr1.roles:
        if roles.name in IMMUNITY_ROLES:
            return True
    if usr1 == usr2:
        return True
    return False

### RATE LIMITED FUNCTIONS ###

def GET_CHANNEL(id):
    return client.get_channel(id)

def GET_EMOJI(id):
    return client.get_emoji(id)

#get up to date ckr members
def UPDATE_CKR():
    global CKR
    CKR = SERVER.get_role(CKR.id)

### PRIVATE ASYNC FUNCTIONS ###
async def SEND(channel,message):
    if message == None or message == "":
        #cannot send empty message
        return
    return await channel.send(message)

#add roles
async def ADD_ROLES(usr,roles):
    await usr.add_roles(roles)
    
#remove roles
async def REMOVE_ROLES(usr,roles):
    await usr.remove_roles(roles)

#edit nick
async def EDIT_NICK(usr,new_nick):
    if usr.id != 481893862864846861:
        await usr.edit(nick=new_nick)
    
#add reaction    
async def ADD_REACTION(msg,reaction):
    await msg.add_reaction(reaction)

#edit message
async def EDIT_MESSAGE(msg, con):
    await msg.edit(content=con)
    
async def DELETE(message):
  await message.delete()

### END OF RATE LIMITED FUNCTIONS ###

#below function can also cause rate limts, but
#they are using only above functions so we do not need 
#to worry about these ones

#print tips
async def PRINT_TIPS(channel,key):
    tips = list_tips(key)
    combined_string = ""
    for i in range(len(tips)):
        new_string = combined_string + str(i) + ") " + tips[i].decode("utf-8") + "\n"
        if len(new_string) > 2000:
            await SEND(channel,combined_string)
            combined_string = str(i) + ") " + tips[i].decode("utf-8") + "\n"
        else:
            combined_string = new_string
    await SEND(channel,combined_string)

#chat killer functions
async def WAIT_FOR_CHAT_KILLER(msg):
    if msg.channel == CHANNELS["general"]:
        global Last
        Last = msg.created_at
        
        #wait 2 hours
        await asyncio.sleep(CHAT_KILLER_WAIT)
        
        if msg.created_at == Last:
            await SEND(CHANNELS["general"],msg.author.mention + " do not worry, I can talk with you if no one else will.")
            UPDATE_CKR()
            for member in CKR.members:
                await REMOVE_ROLES(member,CKR)
            await asyncio.sleep(5)
            await ADD_ROLES(msg.author,CKR)

### RIGS ###

async def Rig(rigType, ch, usr):
   
    if RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]]:
        await SEND(ch, "Ultimate spells are in cooldown.")
        return
        
    spamCount = 0
    if usr in RIG_SPAMMERS:
        spamCount = RIG_SPAMMERS[usr]
    
    if rigType in LIMITED_USE_RIGS:
        if spamCount == 3:
            await SEND(message.channel, "You've been using these commands too often.")
            await asyncio.sleep(3600)
            if usr in RIG_SPAMMERS:
                del RIG_SPAMMERS[usr]
            return
        else:
            spamCount += 1
            RIG_SPAMMERS[usr] = spamCount
            
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = True
    global rigCaster
    
    match rigType:
        
        case "heretic":
            if MURDURATOR in usr.roles:
                await SEND(ch, "You cast Heretic Rig but thanks to your Unbeliever rank, you didn't get possessed.")
                RIG_COOLDOWNS["ha"] = False
                return
            #for member in SERVER.members:
               # if POSSESSED in member.roles:
                   # await SEND(ch, "Another ultimate spell is in progress. Please wait.")
                   # RIG_COOLDOWNS["ha"] = False
                   # return
            await ADD_ROLES(usr, POSSESSED)
            await asyncio.sleep(1)
            await SEND(ch,"You cast Heretic Rig but forgot to unlock Unbeliever rank first and ended up getting Possessed..."
                       "\nMaybe someone could give you some Mana?")
            await asyncio.sleep(60)
            await REMOVE_ROLES(usr, POSSESSED)
            
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
            await SEND(ch, "You cast Hacker Rig an- anddd##dddddddd############")
            await asyncio.sleep(3)
            await EDIT_NICK(usr, im)
            if usr.display_name == '11111111' or usr.display_name == '00000000':
                await SEND(message.channel,"That's some luck right there.")
            
        case "keeper":
            im = ''.join(sorted(usr.display_name))
            await EDIT_NICK(usr, im)
            await asyncio.sleep(1)
            await SEND(ch, "You cast Keeper Rig and now your name is alphabetically ordered!")
        
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
            for rig in ACITVE_RIGS.keys():
                ACITVE_RIGS[rig] = False
                
        case ("joker"|"thief"|"spectre"):
            ACTIVE_RIGS[rigType] = True
            rigCaster = usr
            if rigType == "joker":
                await SEND(ch, usr.mention + " just cast Joker Rig. Someone will be in for a treat.")
            elif rigType == "thief":
                await SEND(ch, usr.mention + " just cast Thief Rig! Watch out everyone.")
            else:
                await SEND(ch, usr.mention + " just cast Spectre Rig! Careful.")
            await asyncio.sleep(600)
            if ACTIVE_RIGS[rigType]:
                 ACTIVE_RIGS[rigType] = False
                 await SEND(ch, rigType.capitalize() + " Rig cooldown is over, and the current Rig effect has worn off.")
                
          
            
    await asyncio.sleep(COOLDOWN_DURATION[rigType])
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = False
    await SEND(message.channel, rigType.capitalize() + " Rig cooldown is over.")
    
    #reset spam count
    await asyncio.sleep(3600)
    if usr in RIG_SPAMMERS and spamCount == RIG_SPAMMERS[usr]:
        del RIG_SPAMMERS[usr]
   


async def necromancer(usr, message, server):
  global ghostedMsg
  
  if ghostMsg != "":
    await SEND(message.channel, ghostMsg)
  else:
    await SEND(message.channel, "*but nobody came...*")

################################################################### END RIGS

### PUBLIC (ON EVENT) FUNCTIONS ###
    
#drone start up, prepare roles here
@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Lucid Ladders")
    await client.change_presence(activity=game)

    #get the guild
    global SERVER
    #this is a one-off, so we do not worry about rate limits
    SERVER = client.get_guild(SERVER)
    
    #get the channels
    for i, v in CHANNELS.items():
        CHANNELS[i] = GET_CHANNEL(v)
    
    #prepare the roles
    global CKR
    global POSSESSED
    global MURDURATOR
    global CLIMBER
    for role in SERVER.roles:
        #morphable
        if role.name in MORPHABLE_ROLES:
            MORPHABLE_ROLES[role.name][0] = role
            continue
        #ping roles
        if role.name in PING_ROLES:
            PING_ROLES[role.name] = role
            continue
        if role.name in SPECIAL_ROLES:
            SPECIAL_ROLES[role.name][0] = role
            continue
        #chat killer
        if role.name == CKR:
            CKR = role
            SPECIAL_ROLES["Ultimate"][0] = role
            continue
        #possessed (for the rig)
        if role.name == POSSESSED:
            POSSESSED = role
            SPECIAL_ROLES["Possessed"][0] = role
            continue
        #climber
        if role.name == CLIMBER:
            CLIMBER = role
            SPECIAL_ROLES["Climber"][0] = role
        #architect
        if role.name == "Architect (Booster)":
            SPECIAL_ROLES["Architect"][0] = role
            continue
        #murdurator
        if role.name == MURDURATOR:
            MURDURATOR = role
            
    #prepare emojis reactions
    for i, v in EMOJIS_TO_REACT.items():
        EMOJIS_TO_REACT[i] = GET_EMOJI(v)
    
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
    if after.nick in Worst_guns:
        return

    await EDIT_NICK(usr,random.choice(WORST_GUNS))
    return

#on new member join
@client.event
async def on_member_join(member):
    await SEND(CHANNELS["general"],
        "Welcome to Crazy Stairs Discord Server!"
        "\nUnlike other Jokers around here, I am a real bot."
        "\nPlease read the <#750056989207429143>, to avoid misunderstandings."
        "\nHave fun, and remember: It's okay to be a little crazy.")
    
#main function on each message being intercepted
@client.event
async def on_message(message):

    msg = message.content
    usr = message.author
    ch = message.channel
    
    ## user must not be a bot
    ## but the bot will add reactions to the webhook (if any)
    ## before returning
    if usr.bot == True:
        for i, v in EMOJIS_TO_REACT.items():
            if i in msg:
                await ADD_REACTION(message,v)
                return
        return
    
    #this will avoid old activatig with old bot
    if msg.startswith(">"):
        return
    
    #normal non-admin usage
    if not msg.startswith("|"):
        
        ## lowercase the message for some commands to use
        lmsg = msg.lower()
        ## split the message to 3 strings for some commands to use
        ## no need to have more than 4 strings
        lsplit = lmsg.split(" ",3) 
        
        #create chat killer task
        #this should run regardless if the message was intercepted
        #by some other command
        ckr_task = asyncio.create_task(WAIT_FOR_CHAT_KILLER(message))
 
        #fallen drone impostor prevention
        compare = SequenceMatcher(None, usr.display_name.upper(), FALLEN_DRONE_NICK)
        if compare.ratio() > 0.5:
            await SEND(ch, usr.mention + ' ' + random.choice(IMPOSTOR_WARNINGS))
            await EDIT_NICK(usr,random.choice(IMPOSTOR_NICKS))
            return
        
        ## All Rigs in one
        if lsplit[0] == "cast" and lsplit[2] == "rig":
            rigPick = lsplit[1]
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
            if rigPick not in RIG_LIST:
                await SEND(ch, rigPick + " is not a valid Rig. Try again.")
                return
            await Rig(rigPick,ch,usr)
            return
        
        ## thief rig acitve
        if ACTIVE_RIGS["thief"]:
          
            if ch.name not in CHANNELS or len(rigCaster.display_name + ", " + usr.display_name) > 32 or not CLIMBER in usr.roles or rigImmunity(usr, rigCaster):
                return
                          
            ACTIVE_RIGS["thief"] = False
            victim = usr.display_name

            NickDictionary[usr] = "N/A"
            await EDIT_NICK(usr, "N/A")

            await asyncio.sleep(1)
          
            if rigCaster in NickDictionary:
              NickDictionary[rigCaster] = rigCaster.display_name + ", " + victim
              await EDIT_NICK(rigCaster, NickDictionary[rigCaster])
              await SEND(ch, rigCaster.mention + " has just stolen your name!")
              return
              
            await EDIT_NICK(rigCaster, rigCaster.display_name + ", " + victim)
            await SEND(ch, rigCaster.mention + " has just stolen your name!")
          
            await asyncio.sleep(1800)
            del NickDictionary[usr]
            return

        ## Spectre Rig Active
        if ACTIVE_RIGS["spectre"]:
            
            if ch.name not in CHANNELS or rigImmunity(usr, rigCaster) or not CLIMBER in usr.roles:
                return
            global ghostMsg
            ACTIVE_RIGS["spectre"] = False

            chances = random.randint(0, 1)

            if chances == 1:
                await SEND(ch, rigCaster.mention + " has made your Message disappear with a 50% chance!")
                await DELETE(message)
                return

            await SEND(ch, rigCaster.mention + " has NOT made your Message disappear with a 50% chance.")
            return

        ## Joker Rig Active
        if ACTIVE_RIGS["joker"]:
            
            if ch.name not in CHANNELS or not CLIMBER in usr.roles or msg.startswith("https"):
                return
            ACTIVE_RIGS["joker"] = False

            msgcontent = message.content

            await DELETE(message)
            await asyncio.sleep(2)

            await SEND(ch, str(msgcontent) + " -" + ":nerd::clown:")
          
            return
                 
        ## Scold command
        if lmsg.startswith("fallen drone scold "):
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

        #morph command
        if lmsg.startswith("morph to"):
            role = lsplit[2].capitalize()
            if role == "Gun":
                role = "Guns"
            if role in MORPHABLE_ROLES:
                if role == "Guns":
                    await EDIT_NICK(usr,random.choice(WORST_GUNS))
                await SEND(ch,MORPHABLE_ROLES[role][1])
                await ADD_ROLES(usr,MORPHABLE_ROLES[role][0])
                return
            if role in SPECIAL_ROLES:
                if SPECIAL_ROLES[role][0] in usr.roles:
                    await SEND(ch,SPECIAL_ROLES[role][2])
                else:
                    await SEND(ch,SPECIAL_ROLES[role][1])
                return
        
        #demorph command (accepts demorph, unmorph and any **morph from combination)
        if lmsg.startswith("morph from",2):
            role = lsplit[2].capitalize()
            if role == "Gun":
                role = "Guns"
            if role in MORPHABLE_ROLES:
                await SEND(ch,MORPHABLE_ROLES[role][2])
                await REMOVE_ROLES(usr,MORPHABLE_ROLES[role][0])
                return
            if role in SPECIAL_ROLES:
                if SPECIAL_ROLES[role][0] in usr.roles:
                    await SEND(ch,SPECIAL_ROLES[role][4])
                else:
                    await SEND(ch,SPECIAL_ROLES[role][3])
                return
        
        #sub command
        if lmsg.startswith("sub to"):
            role = lsplit[2].capitalize()
            if role in PING_ROLES:
                await SEND(ch,"You have subscribed to " + role + "!")
                await ADD_ROLES(usr,PING_ROLES[role])
                return

        #unsub command (aceppts unsub, desub and any **sub from combination)
        if lmsg.startswith("sub from",2):
            role = lsplit[2].capitalize()
            if role in PING_ROLES:
                await SEND(ch,"You have unsubscribed from " + role + "!")
                await REMOVE_ROLES(usr,PING_ROLES[role])
                return
                
        
        
        ## tips/tricks trigger
        if len(lsplit) == 2:
            if lsplit[1] == "tip" or lsplit[1] == "trick":
                if lsplit[0] in TIPS_KEYS:
                    await SEND(ch,show_random_tip(lsplit[0]))
                    return
            elif lsplit[1] == "trivia":
                if lsplit[0] in TIPS_KEYS:
                    key = lsplit[0] + "T"
                    await SEND(ch,show_random_tip(key))
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
        if not usr.id in ADMINS:
            await SEND(ch,"You are not allowed to use this command.")
            return
            
        #deterimine the key (this is an alignment name in most cases)
        split = msg.split(" ", 2)
   
        #give ckr
        if msg.startswith("ckr to ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split[2]:
                   await ADD_ROLES(mem,CKR)
                   break
            return  
        #remove ckr
        if msg.startswith("ckr from ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split[2]:
                   await REMOVE_ROLES(mem,CKR)
                   break
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
            add_tip(key,split[2])
            await SEND(ch,"New " + split[1] + " " + tot + " added.")
            return

        #list tips
        if msg.startswith("l",1):
            await SEND(ch,split[1] + " " + tot + "(s):")
            await PRINT_TIPS(ch, key)
            return
            
        #delete tip
        if msg.startswith("d",1):
            delete_tip(key,int(split[2]))
            await SEND(ch,split[1] + " " + tot + "(s):")
            await PRINT_TIPS(ch, key)
            return
               
### RUN THE BOT ###
client.run(os.environ['TOKEN'])
