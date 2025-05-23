import asyncio
import discord
import time
from globals import EXTRA_ROLES
from globals import SERVER_DATA
from globals import CHANNELS
from globals import EVENTS

def GET_CHANNEL(client,id):
    return client.get_channel(id)

def GET_EMOJI(client,id):
    return client.get_emoji(id)

#get up to date ckr members
def UPDATE_CKR():
    EXTRA_ROLES['ckr'] = SERVER_DATA['server'].get_role(EXTRA_ROLES['ckr'].id)

def UPDATE_NECRO():
    EXTRA_ROLES['necromancer'] = SERVER_DATA['server'].get_role(EXTRA_ROLES['necromancer'].id)

# rate limited functions

#get message
async def GET_MSG(ch,msgID):
    return await ch.fetch_message(msgID)

#add roles
async def ADD_ROLES(usr,roles):
    await usr.add_roles(roles)
    
#remove roles
async def REMOVE_ROLES(usr,roles):
    await usr.remove_roles(roles)

#edit nick
async def EDIT_NICK(usr,new_nick):
    if usr.id != 481893862864846861 and EXTRA_ROLES["admin"] not in usr.roles:
        await usr.edit(nick=new_nick)

#edit role
async def EDIT_ROLE(targetrole, newname, motivation):
    await targetrole.edit(name = newname, reason = motivation)

#send message
async def SEND(channel, message):
    if message == None or message == "":
        #cannot send empty message
        return
    
    if EVENTS["Easter"]:
        message = str(message) + " 🐇"

    return await channel.send(message)

#DM an user
async def SEND_DM(member, message):
    if message == None or message == "":
        #cannot send empty message
        return
    return await member.send(message)

#send to interactiom, optional ephemeral 
async def INTERACTION(message, content: str, secret: bool):
    if content == None or content == "":
        #cannot send empty message
        return
    return await message.send_message(content, ephemeral = secret)

#sends a view with a message
async def SEND_VIEW(channel, content, view):
    return await channel.send(content, view = view)

#send a reply! ephemeral option included
# included where???
async def REPLY(message, content):
    if content == None or content == "":
        #cannot reply with empty message
        return
    return await message.reply(content = content)

#purge roles
async def PURGE_ROLES(role):
    await role.delete()
    
#add reaction    
async def ADD_REACTION(msg,reaction):
    await msg.add_reaction(reaction)

#edit message
async def EDIT_MESSAGE(msg, con):
    await msg.edit(content = con)

#edit views and/or its message
async def EDIT_VIEW_MESSAGE(msg, con, view):
    await msg.edit(content = con, view = view) 
    
async def DELETE(message):
    await asyncio.sleep(2)
    await message.delete()

async def DRONEPRINT(message):
    await SEND(CHANNELS["bot-testing"], message)
    await asyncio.sleep(2)

async def NEW_ROLE(server,colorpick, rolename):
    return await server.create_role(name = rolename, colour = discord.Colour(int(colorpick, 16)))

async def PIN_MESSAGE(message):
    await message.pin()
    
async def UNPIN_MESSAGE(message):
    await message.unpin()

