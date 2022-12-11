import random

from rated import *
from globals import *

def PrepareRoles(serverRoles):
    #prepare the roles
    global CKR
    global POSSESSED
    global MURDURATOR
    global CLIMBER
    global ADMIN

    for role in serverRoles:
        #morphable
        if role.name in MORPHABLE_ROLES:
            MORPHABLE_ROLES[role.name][0] = role
            continue
        #ping roles
        if role.name in PING_ROLES:
            PING_ROLES[role.name] = role
            continue
        #drone admin
        if role.id == ADMIN:
            ADMIN = role
            continue
        #chat killer
        if role.id == CKR:
            CKR = role
            SPECIAL_ROLES["Ultimate"][0] = role
            continue
        #possessed (for the rig)
        if role.id == POSSESSED:
            POSSESSED = role
            SPECIAL_ROLES['Possessed'][0] = role
        #climber
        if role.id == CLIMBER:
            CLIMBER = role
            SPECIAL_ROLES["Climber"][0] = role
        #architect
        if role.name == "Architect (Booster)":
            SPECIAL_ROLES["Architect"][0] = role
            continue
        #discord admin
        if role.name == 'Admin':
            SPECIAL_ROLES['Admin'][0] = role
            continue
        #murdurator
        if role.id == MURDURATOR:
            MURDURATOR = role
        #drone tips/tricks admins
        if role.id == ADMIN:
            ADMIN = role
        #fun roles
        if role.name in FUN_ROLES:
            FUN_ROLES[role.name] = role
            continue

async def MorphTo(usr,role):
    if role == "Gun":
        role = "Guns"

    if role in MORPHABLE_ROLES:
        if role == "Guns":
            await EDIT_NICK(usr,random.choice(WORST_GUNS))

        if MORPHABLE_ROLES[role][0] in usr.roles:
            return MORPHABLE_ROLES[role][3]
        else:
            await ADD_ROLES(usr,MORPHABLE_ROLES[role][0])
            return MORPHABLE_ROLES[role][1]
               

    if role in SPECIAL_ROLES:
        if SPECIAL_ROLES[role][0] in usr.roles:
            return SPECIAL_ROLES[role][2]
        else:
            return SPECIAL_ROLES[role][1]
                

async def DemorphFrom(usr,role):     
    if role == "Gun":
        role = "Guns"
                
    if role in MORPHABLE_ROLES:
        if MORPHABLE_ROLES[role][0] not in usr.roles:
            return MORPHABLE_ROLES[role][4]
        else:
            await REMOVE_ROLES(usr,MORPHABLE_ROLES[role][0])
            return MORPHABLE_ROLES[role][2]
               
                
    if role in SPECIAL_ROLES:
        if SPECIAL_ROLES[role][0] in usr.roles:
            return SPECIAL_ROLES[role][4]
        else:
            return SPECIAL_ROLES[role][3]

async def SubTo(usr,role):
     if role in PING_ROLES:
        await ADD_ROLES(usr,PING_ROLES[role])
        return "You have subscribed to " + role + "!"

#unsub command (aceppts unsub, desub and any **sub from combination)
async def UnsubFrom(usr,role):       
    if role in PING_ROLES:
        await REMOVE_ROLES(usr,PING_ROLES[role])
        return "You have unsubscribed from " + role + "!"
               
#chat killer function
async def WAIT_FOR_CHAT_KILLER(msg):
    if msg.channel == CHANNELS["general"]:
        global Last
        global revivechat
        Last = msg.created_at
        
        #wait 2 hours
        await asyncio.sleep(CHAT_KILLER_WAIT)
        
        if msg.created_at == Last and not CKR in msg.author.roles:
            thirdkill = None
            revivechat = True
            await SEND(CHANNELS["general"],msg.author.mention + " do not worry, I can talk with you if no one else will.")
            UPDATE_CKR()
            for member in CKR.members:
                await REMOVE_ROLES(member,CKR)
            await asyncio.sleep(5)
            await ADD_ROLES(msg.author,CKR)
            await asyncio.sleep(1)

            if CKR.name != "Ultimate Chat Killer":
                await EDIT_ROLE(CKR, "Ultimate Chat Killer", "New chat killer. They are not Definitive yet.")
            return

        elif msg.created_at == Last and CKR in msg.author.roles:
            revivechat = True
            if CKR.name == "Definitive Ultimate Chat Killer" or CKR.name == "Professional Chat Murderer":
                await SEND(CHANNELS["general"],msg.author.mention + " stop killing the chat...")
                await asyncio.sleep(1)

                if CKR.name != "Professional Chat Murderer":
                    await EDIT_ROLE(CKR, "Professional Chat Murderer", "This user has killed the chat thrice in a row.")
                return

            await SEND(CHANNELS["general"],msg.author.mention + " what have you done to this chat.")
            await asyncio.sleep(1)
      
    