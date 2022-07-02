### IMPORTS ###

import discord
import os
import random
import asyncio
import redis
from datetime import date

## CONSTANTS ##

#ids will be replaced with objects on startup
SERVER = 624227331720085528

#special roles
#roles that bot can assing to, but not by a regular user commannd
#values replaced by roles on startup
CKR = "Ultimate Chat Killer"
POSSESSED = "Possessed (rig)"

#this is for administrating tips and trivia database
ADMINS = [
    481893862864846861, #sleazel
    267014823315898368, #rolo
    745478913999896637, #bluestar
    487107394774630401, #hmster
    380938705667620874, #jeff
    786743350950494219, #td
] 

#channels where bot is allowed to post
CHANNELS = {
    "general": 624227331720085536,
    "commands": 750060041289072771,
    "crazy-stairs": 750060054090219760,  
    "test": 813882658156838923,
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
       "The staircase is now under your supervision, you successfully became a Keeper."
       "You failed to take care of the stairs, and so you are no longer a Keeper.",
    ],
    "Muggle": [ 
       None,
       "Work smarter, not harder. You are now a Muggle!",
       "The tower was too overwhelming for a weakling like you. Your Muggle license has been revoked.",
    ],
    "Chameleon": [ 
       None,
       "Do not let them know your next move, you are now a Chameleon!"
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
        "I saw you taking the stairs, you are no longer a Drifter",
     ],
     "Heretic": [ 
        None,
        "We have banned dark magic, but you do not seem to care. You successfully became a Heretic."
        "The circle has made their decision. You are permanently banned from being a Heretic ever again.",
    ],
     "Guns": [ 
        None,
        "smh, FINE!",
        "Finally you came to your senses.",
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
     "There was an attempt.": 
        'demorph from ultimate chat killer',
    "It needs to be earned, sorry.":
        'morph to ultimate chat killer',
     "Tsk.":
        'cstrollpain',
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
    "{stairjumper} is a true stair jumper.":
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

### GLOBAL VARIABLES ###

# for chat killer role, time when the last message was sent
# (seconds from unix epoch)
Last = 0
PreviousKiller = None

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
    
### RATE LIMITED FUNCTIONS ###

def GET_CHANNEL(id):
    return client.get_channel(id)

def GET_EMOJI(id):
    return client.get_emoji(id)

### PRIVATE ASYNC FUNCTIONS ###
async def SEND(channel,message):
    if message == None or message == "":
        #cannot send empty message
        return
    await channel.send(message)

#add roles
async def ADD_ROLES(usr,roles):
    await usr.add_roles(roles)
    
#remove roles
async def REMOVE_ROLES(usr,roles):
    await usr.remove_roles(roles)

#edit nick
async def EDIT_NICK(usr,new_nick):
    await usr.edit(nick=new_nick)
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
        global PreviousKiller
        Last = msg.created_at
        
        #wait 2 hours
        await asyncio.sleep(7200)
        
        if msg.created_at == Last:
            await SEND(CHAT_KILLER_CHANNEL,msg.author.mention + " do not worry, I can talk with you if no one else will.")
            for member in CKR.members:
                await REMOVE_ROLES(member,CKR)
            if PreviousKiller:
                await REMOVE_ROLES(PreviousKiller,CKR)
            await asyncio.sleep(5)
            await ADD_ROLES(usr,CKR)
            PreviousKiller = usr


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
    for role in SERVER.roles:
        #morphable
        if role.name in MORPHABLE_ROLES:
            MORPHABLE_ROLES[role.name][0] = role
            continue
        #ping roles
        if role.name in PING_ROLES:
            PING_ROLES[role.name] = role
            continue
        #chat killer
        if role.name == CKR:
            CKR = role
            continue
        #possessed (for the rig)
        if role.name == POSSESSED:
            POSSESSED = role
            continue
            
    #prepare emojis reactions
    for i, v in EMOJIS_TO_REACT.items():
        EMOJIS_TO_REACT[i] = GET_EMOJI(v)
    
    #send ready to the test channel
    await SEND(CHANNELS["test"],'The last edited code is now effective.')

#member update, prevent changing gun nick to anything other than the gun name
@client.event
async def on_member_update(before, after):
    
    #nick has not changed
    if before.nick == after.nick:
        return
    
    #is user a gun?
    if not MORPHABLE_ROLES["Guns"][0] in before.roles:
        return
    
    #ignore if user nick after change is a gun name
    if after.nick in Worst_guns:
        return

    await EDIT_NICK(usr,random.choice(WORST_GUNS))
    return

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
                await message.add_reaction(v)
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
        ## no need to have more than 3 strings
        lsplit = lmsg.split(" ",2) 
        
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
        
        #demorph command (accepts demorph, unmorph and any **morph from combination)
        if lmsg.startswith("morph from",2):
            role = lsplit[2].capitalize()
            if role == "Gun":
                role = "Guns"
            if role in MORPHABLE_ROLES:
                await SEND(ch,MORPHABLE_ROLES[role][2])
                await REMOVE_ROLES(usr,MORPHABLE_ROLES[role][0])
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
                await SEND(ch,i)
                return
        
        #multiple word trigger
        for i, v in MULTIPLE_WORD_TRIGGERS.items():
            if all(word in lmsg for word in v):
                if "{stairjumper}" in i:
                    i = i.format(stairjumper=usr.mention)
                await SEND(ch,i)
                return
       
        #mixed word trigger
        for i, v in MIXED_WORD_TRIGGERS.items():
            if v[0] in lmsg:
                if any(word in lmsg for word in v[1]):
                    await SEND(ch,i)
                    return
        
        #chat killer
        await WAIT_FOR_CHAT_KILLER(msg)
               
    ## admin command
    else:

        #check for admin
        if not usr.id in ADMINS:
            await SEND(ch,"You are not allowed to use this command.")
            return
            
        #deterimine the key (this is an alignment name in most cases)
        split = msg.split(" ", 2)
        key = split[1]
        target = split[2]
   
        #give ckr
        if msg.startswith("ckr to ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == target:
                   await ADD_ROLES(mem,CKR)
                   break
            return  
        #remove ckr
        if msg.startswith("ckr from ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == target:
                   await REMOVE_ROLES(mem,CKR)
                   break
            return   
        
        if not key in TIPS_KEYS:
            await SEND(ch,"Invalid alignment.")
            return
           
        #tip or trick?
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
