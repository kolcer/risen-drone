import random

from rated import *
from globals import *
from database import list_decoded_entries

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
        #necromancer - gone, reduced into atoms
        # if role.id == EXTRA_ROLES['necromancer']:
        #     EXTRA_ROLES['necromancer'] = role
        #     SPECIAL_ROLES['Necromancer'][0] = role
        #     continue
        #possessed (for the rig)
        if role.id == EXTRA_ROLES['possessed']:
            EXTRA_ROLES['possessed'] = role
            SPECIAL_ROLES['Possessed'][0] = role
        #hypnotized (for the rig)
        if role.id == EXTRA_ROLES['hypno']:
            EXTRA_ROLES['hypno'] = role
            SPECIAL_ROLES['hypno'][0] = role
        #climber
        if role.id == EXTRA_ROLES['climber']:
            EXTRA_ROLES['climber'] = role
            SPECIAL_ROLES["Climber"][0] = role
        #manually verified
        if role.id == EXTRA_ROLES['manuallyverified']:
            EXTRA_ROLES['manuallyverified'] = role
        #image perms
        if role.id == EXTRA_ROLES['imageperms']:
            EXTRA_ROLES['imageperms'] = role
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
        #basically Splicer, roles with color and icons
        if role.name in APPROVED_ROLES:
            APPROVED_ROLES[role.name] = role

# def PrepareSecretRoles(roles):  # Keeping this ready.
#     for role in roles:
#         #secret roles
#         if role in roles:
#             FUN_ROLES[role] = list_decoded_entries(role)
#             continue
 
async def MorphTo(usr,role):

    if role in MORPHABLE_ROLES:
        if role == "Gun":
            await EDIT_NICK(usr,random.choice(WORST_GUNS))
        elif role == 'Roingus':
            await EDIT_NICK(usr, 'Roingus')

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
        CHAT_KILLER['last'] = msg.created_at
        
        #wait 2 hours
        await asyncio.sleep(CHAT_KILLER['wait'])
        
        if msg.created_at == CHAT_KILLER['last'] and not EXTRA_ROLES['ckr'] in msg.author.roles:
            #thirdkill = None # Nick - i have removed this, seems to be unused - sleazel #Sleazel - it seems i have used it for something and then forgot to delete - rolo
            CHAT_KILLER['reviveChat'] = True
            NECROMANCY['awarded'] = False
            print("new chat killer")
            await SEND(CHANNELS["general"],msg.author.mention + " do not worry, I can talk with you if no one else will.")
            UPDATE_CKR()
            for member in EXTRA_ROLES['ckr'].members:
                await REMOVE_ROLES(member,EXTRA_ROLES['ckr'])
            await asyncio.sleep(5)
            await ADD_ROLES(msg.author,EXTRA_ROLES['ckr'])
            await asyncio.sleep(1)

            if EXTRA_ROLES['ckr'].name != "Ultimate Chat Killer":
                await EDIT_ROLE(EXTRA_ROLES['ckr'], "Ultimate Chat Killer", "New chat killer. They are not Professionals yet.")
            return

        elif msg.created_at == CHAT_KILLER['last'] and EXTRA_ROLES['ckr'] in msg.author.roles:
            CHAT_KILLER['reviveChat'] = True

            if EXTRA_ROLES['ckr'].name != "Ultimate Chat Killer":
                NECROMANCY['awarded'] = False
                await SEND(CHANNELS["general"], msg.author.mention + " this is infinitely saddening. Nobody wants to talk with you.")
                await asyncio.sleep(1)

                await EDIT_ROLE(EXTRA_ROLES['ckr'], "The Awkward One", "Awkward.")

            if EXTRA_ROLES['ckr'].name == "Ultimate Chat Killer":
                NECROMANCY['awarded'] = False
                await SEND(CHANNELS["general"], msg.author.mention + " I must insist. I am here for you if you wish.")
                await asyncio.sleep(1)

                await EDIT_ROLE(EXTRA_ROLES['ckr'], "Professional Chat Murderer", "Yikes, they have killed the chat again.")
      
    
