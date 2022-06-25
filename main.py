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
  481893862864846861,
] 

### INITIAL SETUP ###

# This allows us to know if user has updated their presence
# Mosty for the gun role nick change prevention
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Set up the data base
db = redis.StrictRedis(host = 'localhost',port = 6379, db = 0)

### PRIVATE SYNC FUNTIONS ###

def add_tip(key, new_tip):
    db.rpush(key,new_tip)

def delete_tip(key, index):
    db.lset(key,index,"_del_")
    db.lrem(key,1,"_del_")

def list_tips(key):
    return db.lrange(key,0,-1)

### PRIVATE ASYNC FUNCTIONS ###

#TODO: implement anti rate-limit measures here
async def SEND(channel,message)
    await channel.send('The last edited code is now effective.')

#print tips
async def PRINT_TIPS(channel,key)
    tips = list_tips(key)
    for i in range(len(tips)):
        new_string = combined_string + str(i) + ") " + tips[i] + "\n"
        if len(new_string) > 2000:
            await SEND(channel,combined_string)
            combined_string = str(i) + ") " + tips[i] + "\n"
        else:
            combined_string = new_string
            await SEND(channel,combined_string)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Lucid Ladders")
    await client.change_presence(activity=game)

    channel = client.get_channel(813882658156838923)
    await send_message(channel,'The last edited code is now effective.')
    return


@client.event
async def on_message(message):

    msg = message.content
    usr = message.author

    ## user must not be a bot
    if usr.bot == False:
        
        ## tips/tricks command
        if msg.startswith("]"):

            #check for admin
            is_admin = False
            for admin in admins:
                if admin == str(usr.id):
                    is_admin = True
                    break
            if is_admin == False:
                await SEND(channel,"You are not allowed to use this command.")
                return
            
            #lowercase the message
            msg = msg.lower()
            
            #deterimine the key (this is an alignment name in most cases)
            split = msg.split(" ", 2)
            key = split[1]
            #tip or trick?
            tot = "tip"
            #for trivia, key has extra "T" at the end
            if "triv" in msg:
                key = key + "T"
                tot = "trivia"
                
            #add tip   
            if msg.startswith("]n"):
               add_tip(key,split[2])
               await SEND(channel,"New " + split[1] + " " + tot + "  added.")
               return

            #list tips
            if msg.startswith("]l"):
               await SEND(channel,split[1] + " " + tot + "(s):")
               await PRINT_TIPS(channel, key)
               return
            
            #delete tip
            if msg.startswith("]d"):
               delete_tip(key,int(split[2]))
               await SEND(channel,split[1] + " " + tot + "(s):")
               await PRINT_TIPS(channel, key)
               return

            
#run the bot 
client.run(os.environ['TOKEN'])
