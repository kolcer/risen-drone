import asyncio
import discord
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
    if isinstance(roles, list):
        await usr.add_roles(*roles)
    else:
        await usr.add_roles(roles)
    
#remove roles
async def REMOVE_ROLES(usr,roles):
    if isinstance(roles, list):
        await usr.remove_roles(*roles)
    else:
        await usr.remove_roles(roles)

#edit nick
async def EDIT_NICK(usr,new_nick):
    if usr.id != 481893862864846861 and EXTRA_ROLES["admin"] not in usr.roles:
        await usr.edit(nick=new_nick)

#edit role
async def EDIT_ROLE(targetrole, newname, motivation):
    await targetrole.edit(name = newname, reason = motivation)

#send message
async def SEND(channel, message, view=None):
    if message == None or message == "":
        #cannot send empty message
        return
    
    if EVENTS["Easter"]:
        message = str(message) + " 🐇"

    if view is not None:
        return await channel.send(message, view=view)
    else:
        return await channel.send(message)
    
#edit message
async def EDIT_MESSAGE(msg, con, view=None, embed=None):
    kwargs = {
        "content": con,
    }

    if view is not None:
        kwargs["view"] = view
    if embed is not None:
        kwargs["embed"] = embed

    await msg.edit(**kwargs)

#sends a view with a message
async def SEND_VIEW(channel, content, view):
    return await channel.send(content, view = view)

#send follow up message
async def FOLLOWUP(message, interaction, ephemeral=False, view=None, embed=None):
    if not message and not view and not embed:
        return 

    if EVENTS.get("Easter") and message:
        message = str(message) + " 🐇"

    kwargs = {
        "content": message,
        "ephemeral": ephemeral
    }

    # 4. ONLY add view/embed if they are NOT None
    if view is not None:
        kwargs["view"] = view
    if embed is not None:
        kwargs["embed"] = embed

    return await interaction.followup.send(**kwargs)

# async def FOLLOWUP(message, interaction, ephemeral=False, view=None, embed=None):
#     if message == None or message == "":
#         #cannot send empty message
#         return
    
#     if EVENTS["Easter"]:
#         message = str(message) + " 🐇"

#     if view is not None:
#         return await interaction.followup.send(message, ephemeral=ephemeral, view=view)
#     else:
#         return await interaction.followup.send(message, ephemeral=ephemeral)

#defer
async def DEFER(interaction, ephemeral=False):
    return await interaction.response.defer(ephemeral=ephemeral)

#DM an user
async def SEND_DM(member, message):
    if message == None or message == "":
        #cannot send empty message
        return
    return await member.send(message)

#send to interactiom, optional ephemeral 
async def INTERACTION(interaction, content: str, secret: bool=False):
    if content == None or content == "":
        #cannot send empty message
        return
    
    return await interaction.response.send_message(content, ephemeral = secret)

async def EDIT_INTERACTION(interaction, content: str, view=None, embed=None):
    if content == None or content == "":
        #cannot send empty message
        return
    
    kwargs = {
        "content": content,
    }

    # 4. ONLY add view/embed if they are NOT None
    if view is not None:
        kwargs["view"] = view
    if embed is not None:
        kwargs["embed"] = embed

    return await interaction.response.edit_message(**kwargs)

    # return await interaction.send_message(content, ephemeral = secret)

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

#edit views and/or its message
async def EDIT_VIEW_MESSAGE(msg, con, view):
    await msg.edit(content = con, view = view) 
    
async def DELETE(message):
    await asyncio.sleep(2)
    await message.delete()

async def DRONEPRINT(message):
    await SEND(CHANNELS["drone-masters"], message)
    await asyncio.sleep(2)

async def NEW_ROLE(server,colorpick, rolename):
    return await server.create_role(name = rolename, colour = discord.Colour(int(colorpick, 16)))

async def PIN_MESSAGE(message):
    await message.pin()
    
async def UNPIN_MESSAGE(message):
    await message.unpin()

