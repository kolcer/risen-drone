import random

from rated import *
from globals import *

def PrepareRoles(roles):
    for role in roles:
        #morphable
        if role.name in MORPHABLE_ROLES:
            MORPHABLE_ROLES[role.name][0] = role
            continue
        #ping roles
        if role.name in PING_ROLES:
            PING_ROLES[role.name] = role
            continue
        #drone admin
        if role.id == EXTRA_ROLES['admin']:
            EXTRA_ROLES['admin'] = role
            continue
        #chat killer
        if role.id == EXTRA_ROLES['ckr']:
            EXTRA_ROLES['ckr'] = role
            SPECIAL_ROLES["Ultimate"][0] = role
            continue
        #possessed (for the rig)
        if role.id == EXTRA_ROLES['possessed']:
            EXTRA_ROLES['possessed'] = role
            SPECIAL_ROLES['Possessed'][0] = role
        #climber
        if role.id == EXTRA_ROLES['climber']:
            EXTRA_ROLES['climber'] = role
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
        if role.id == EXTRA_ROLES['murdurator']:
            EXTRA_ROLES['murdurator'] = role
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

        if role == "Guns":
            return "Not today matey."

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
        CHAT_KILLER['last'] = msg.created_at
        
        #wait 2 hours
        await asyncio.sleep(CHAT_KILLER['wait'])
        
        if msg.created_at == CHAT_KILLER['last'] and not EXTRA_ROLES['ckr'] in msg.author.roles:
            #thirdkill = None # Nick - i have removed this, seems to be unused - sleazel #Sleazel - it seems i have used it for something and then forgot to delete - rolo(?)
            CHAT_KILLER['reviveChat'] = True
            print("new chat killer")
            await SEND(CHANNELS["general"],msg.author.mention + " do not worry, I can talk with you if no one else will.")
            UPDATE_CKR()
            for member in EXTRA_ROLES['ckr'].members:
                await REMOVE_ROLES(member,EXTRA_ROLES['ckr'])
            await asyncio.sleep(5)
            await ADD_ROLES(msg.author,EXTRA_ROLES['ckr'])
            await asyncio.sleep(1)

            if EXTRA_ROLES['ckr'].name != "Ultimate Chat Killer":
                print("attempt to change the name of the role to: Ultimate Chat Killer")
                await EDIT_ROLE(EXTRA_ROLES['ckr'], "Ultimate Chat Killer", "New chat killer. They are not Professionals yet.")
                print(EXTRA_ROLES['ckr'].name)
            return

        elif msg.created_at == CHAT_KILLER['last'] and EXTRA_ROLES['ckr'] in msg.author.roles:
            CHAT_KILLER['reviveChat'] = True
            print("user already has the chat killer role")
            print(EXTRA_ROLES['ckr'].name)

            if EXTRA_ROLES['ckr'].name != "Ultimate Chat Killer":
                print("attempt to change the name of the role to: The Awkward One")
                await SEND(CHANNELS["general"],msg.author.mention + " what have you done to this chat.")
                await asyncio.sleep(1)

                await EDIT_ROLE(EXTRA_ROLES['ckr'], "The Awkward One", "Awkward.")
                print(EXTRA_ROLES['ckr'].name)

            if EXTRA_ROLES['ckr'].name == "Ultimate Chat Killer":
                print("attempt to change the name of the role to: Professional Chat Murderer")
                await SEND(CHANNELS["general"],msg.author.mention + " you did it again...")
                await asyncio.sleep(1)

                await EDIT_ROLE(EXTRA_ROLES['ckr'], "Professional Chat Murderer", "Yikes, they have killed the chat again.")
                print(EXTRA_ROLES['ckr'].name)
      
    
