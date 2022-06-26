### IMPORTS ###

import discord
import os
import random
import asyncio
import redis
from datetime import date

## CONSTANTS ##

#this is for administrating tips and trivia database
ADMINS = [
    481893862864846861, #sleazel
    267014823315898368, #rolo
    745478913999896637, #bluestar
    487107394774630401, #hmster
    380938705667620874, #jeff
    786743350950494219, #td
] 

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



#this keywords will trigger the bot with a single occurence
#key is the trigger, value is the response
#it DOES NOT have to be a single word
SINGLE_WORD_TRIGGERS = {
    'gun': "<:cs_Stairbonk:812813052822421555>",
    'demorph from ultimate chat killer': "There was an attempt.",
    'morph to ultimate chat killer': "It needs to be earned, sorry.",
    'csTrollpain': "Tsk." 
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
    
### PRIVATE ASYNC FUNCTIONS ###

#TODO: implement anti rate-limit measures here
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

#edit nick
async def EDIT_NICK(usr,new_nick):
    await usr.edit(new_nick)
    
    
#drone start up, prepare roles here
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Lucid Ladders")
    await client.change_presence(activity=game)
    
    #prepare roles
    guild = client.get_guild(624227331720085528)
    server_roles = guild.roles
    
    #morphable
    for role in server_roles:
        if role.name in MORPHABLE_ROLES:
            MORPHABLE_ROLES[role.name][0] = role
    
    channel = client.get_channel(813882658156838923)
    await SEND(channel,'The last edited code is now effective.')
    return

#member update, prevent changing gun nick to anything other than the gun name
@client.event
async def on_member_update(before, after):
    
    #nick has not changed
    if before.nick == after.nick:
        return
    
    #is user a gun?
    is_gun = False
    for role in before.roles:
        if role.name == "Guns":
            is_gun = True
    #not a gun
    if not is_gun:
        return
    
    #ignore if user nick after change is a gun name
    if after.nick in Worst_guns:
        return

    await EDIT_NICK(usr,nick=random.choice(WORST_GUNS))
    return

@client.event
async def on_message(message):

    msg = message.content
    usr = message.author
    ch = message.channel
    
    ## user must not be a bot
    if usr.bot == True:
        return
    
    #this will avoid old activatig with old bot
    if msg.startswith(">"):
        return
    
    #normal non-admin usage
    if not msg.startswith("|"):
        
        ## lowercase the message for some commands to use
        lmsg = msg.lower()
        
        #morph command
        if lmsg.startswith("morph to"):
            split = lmsg.split(" ",2)
            role = split[2].capitalize()
            if role == "Gun":
                role = "Guns"
            if role in MORPHABLE_ROLES:
                if role == "Guns":
                    await EDIT_NICK(usr,nick=random.choice(WORST_GUNS))
                await SEND(ch,MORPHABLE_ROLES[role][1])
                await ADD_ROLES(usr,MORPHABLE_ROLES[role][0])
                
        if lmsg.startswith("unmorph from") or lmsg.startswith("demorph from"):
            split = lmsg.split(" ",2)
            role = split[2].capitalize()
            if role == "Gun":
                role = "Guns"
            if role in MORPHABLE_ROLES:
                await SEND(ch,MORPHABLE_ROLES[role][2])
                await REMOVE_ROLES(usr,MORPHABLE_ROLES[role][0])
        
        ## tips/tricks trigger
        split = lmsg.split(" ", 1)
        if len(split) == 2:
            if split[1] == "tip" or split[1] == "trick":
                if split[0] in TIPS_KEYS:
                    await SEND(ch,show_random_tip(split[0]))
                    return
            elif split[1] == "trivia":
                if split[0] in TIPS_KEYS:
                    key = split[0] + "T"
                    await SEND(ch,show_random_tip(key))
                    return

        #single word trigger
        for i, v in SINGLE_WORD_TRIGGERS.items():
            if i in lmsg:
                await SEND(ch,v)
                return
        
        #multiple word trigger
        for i, v in MULTIPLE_WORD_TRIGGERS.items():
            if all(word in lmsg for word in v):
                await SEND(ch,i)
                return
       
        #mixed word trigger
        for i, v in MIXED_WORD_TRIGGERS.items():
            if v[0] in lmsg:
                if any(word in lmsg for word in v[1]):
                    await SEND(ch,i)
                    return
                
               
    ## tips/tricks admin command
    else:

        #check for admin
        if not usr.id in ADMINS:
            await SEND(ch,"You are not allowed to use this command.")
            return
            
        #deterimine the key (this is an alignment name in most cases)
        split = msg.split(" ", 2)
        key = split[1]
        
        if not key in TIPS_KEYS:
            await SEND(ch,"Invalid alignment.")
            return
           
        #tip or trick?
        tot = "ti"
        if msg.startswith("tr",2):
            tot = "tr"
            #for trivia, key has extra "T" at the end
            key = key + "T"
        elif not msg.startswith("ti",2):
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
    
         
#run the bot 
client.run(os.environ['TOKEN'])
