### IMPORTS ###

import discord
import os
import random
import asyncio
import redis
from datetime import date

## CONSTANTS ##

TIPS_KEYS = [
    "patron", "joker", "wicked", "spectre", "keeper", "muggle", "chameleon",
    "thief", "hacker", "archon", "drifter", "heretic", "none", "general",
    "possessed", "architect",
]

ADMINS = [
    481893862864846861, #sleazel
    267014823315898368, #rolo
    745478913999896637, #bluestar
    487107394774630401, #hmster
    380938705667620874, #jeff
    786743350950494219, #td
] 

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


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Lucid Ladders")
    await client.change_presence(activity=game)

    channel = client.get_channel(813882658156838923)
    await SEND(channel,'The last edited code is now effective.')
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
        
        lmsg = msg.lower()
        
        ## tips/tricks trigger
        split = lmsg.split(" ", 1)
        if split[1] == "tip" or split[1] == "trick":
            if split[0] in TIPS_KEYS:
                await SEND(ch,show_random_tip(split[0]))
        elif split[1] == "trivia":
            if split[0] in TIPS_KEYS:
                key = split[0] + "T"
                await SEND(ch,show_random_tip(key))
                
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
        tot = "tip"
        if msg.startswith("triv",2):
            tot = "trivia"
            #for trivia, key has extra "T" at the end
            key = key + "T"
        elif not msg.startswith("tip",2):
            await SEND(ch,"Invalid command.")
            return
        
        #add tip   
        if msg.startswith("n",1):
            add_tip(key,split[2])
            await SEND(ch,"New " + split[1] + " " + tot + "  added.")
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
