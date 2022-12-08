import random
import asyncio

Last = 0
#chatt killer requires 2 hours of inactivity(in seconds)
CHAT_KILLER_WAIT = 7200
CKR = 951424560685805588

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

#this roles can be assigned via a morph to command
#at 0 index we will put a role object during the login proccess.
#make sure indexes match role name in the server!
MORPHABLE_ROLES = {
    "Patron": [ 
        None,
        "Go help those noobs, you are now a Patron!",
        "What about protecting the noobs? Without a Patron around they will be lost.",
        "You are already assisting the noobs, why would you help them twice?",
        "Nobody has seen you around lately, what are you doing?",
    ],
    "Joker": [ 
        None,
        "As if there weren't enough clowns here, you are now a Joker!",
        "Did you run out of jokes? The Joker guild will hear about this.",
        "Nice joke.",
        "You were not a Joker, but you are a Clown now for sure.",
    ],
    "Wicked": [ 
        None,
        "Unleash all your wickedness, you are now a Wicked!",
        "You destroyed everything and left nothing behind. Thank you for your services, a Wicked is not needed anymore.",
        "You have been destroying the stairs until now...",
        "You are not a Wicked...",
    ],
    "Spectre": [ 
        None,
        "Spectre guild quote's founder has been identified, you are now a Spectre.",
        "Once again, Spectre's Founder went MIA.",
        "We have already found you, or are you planning to leave?",
        "Your soul didn't belong here to begin with.",
    ],
    "Keeper": [ 
        None,
        "The staircase is now under your supervision, you successfully became a Keeper.",
        "You failed to take care of the stairs, and so you are no longer a Keeper.",
        "Do you need help cleaning the stairs?",
        "The stairs do not recognise you anyway.",
    ],
    "Muggle": [ 
        None,
        "Work smarter, not harder. You are now a Muggle!",
        "The tower was too overwhelming for a weakling like you. Your Muggle license has been revoked.",
        "Are you having an identity crisis?",
        "Once a weakling, always a weakling.",
    ],
    "Chameleon": [ 
        None,
        "Do not let them know your next move, you are now a Chameleon!",
        "You had many options, yet you came back. You do not get to be a Chameleon anymore.",
        "You cannot morph to Chameleon via Chameleon, duh.",
        "I know a Chameleon when I see one, and you aren't one.",
    ],
    "Hacker": [ 
        None,
        "Welcome to the backdoor, you are now a Hacker!",
        "You tried to execute some code but as a result you accidentally removed your Hacker permissions.",
        "You are already inside...",
        "You do not seem to be a cheater, no reason to remove your permissions.",
    ],
    "Thief": [ 
        None,
        "Is it really called borrowing? You are now a Thief!",
        "You actually gave me back the role? How generous. But also that doesn't make you a Thief anymore.",
        "The thief guild has already hired you.",
        "The thief guild has never seen you before.",
     ],
    "Archon": [ 
        None,
        "Typo fixed, happy? You are now an Archon!",
        "Traveling between portals has been fun, but fun eventually comes to an end. You are no longer an Archon.",
        "I have already corrected the typo.",
        "Do you want the fun to end twice?",
     ],
     "Drifter": [ 
        None,
        "You took the elevator and rose to the top. You are now a Drifter.",
        "I saw you taking the stairs, you are no longer a Drifter.",
        "Isn't that you traveling on the platforms?",
        "You are still taking the stairs.",
     ],
     "Heretic": [ 
        None,
        "We have banned dark magic, but you do not seem to care. You successfully became a Heretic.",
        "The circle has made their decision. You are permanently banned from being a Heretic ever again.",
        "You cared enough to join again?",
        "You are banned from being a Heretic ever again.",
    ],
     "Guns": [ 
        None,
        "smh, FINE!",
        "Finally you came to your senses.",
        "SMH! FINE!",
        "You are not a gun.",
     ],
}

FUN_ROLES = {
    "Sanctuary Discoverer": None,
    "Splicer": None,
    "Heretic Defier": None,
    "Architect Design": None,
    "Pranked the Creator": None,
    "I was there": None,
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
        "Wait for someone to cast a Heretic Rig.",
        "You are already possessed...",
        "You are not possessed...",
        "Ask someone for mana.",
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
    "Minigames":
        None,
}
IMMUNITY_ROLES = ["Admin", "Murdurators", "Sleazel"]

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

#get up to date ckr members
def UPDATE_CKR(server):
    global CKR
    CKR = server.get_role(CKR.id)

async def EDIT_ROLE(targetrole, newname, motivation):
  await targetrole.edit(name = newname, reason = motivation)

def PrepareRoles(serverRoles):
    for role in serverRoles:
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
        if role.id == CKR:
            CKR = role
            SPECIAL_ROLES["Ultimate"][0] = role
            continue
        #possessed (for the rig)
        if role.id == POSSESSED:
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
               #return

            if role in SPECIAL_ROLES:
                if SPECIAL_ROLES[role][0] in usr.roles:
                    return SPECIAL_ROLES[role][2]
                else:
                    return SPECIAL_ROLES[role][1]
                

async def DemorphFrom(usr,role):     
            if role == "Gun":
                role = "Guns"
                
            # if role in MORPHABLE_ROLES:
            #     await SEND(ch,MORPHABLE_ROLES[role][2])
            #     await REMOVE_ROLES(usr,MORPHABLE_ROLES[role][0])
            #     return

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
        #if lmsg.startswith("sub to"):
            #role = lsplit[2].capitalize()
            if role in PING_ROLES:
                #await SEND(ch,)
                await ADD_ROLES(usr,PING_ROLES[role])
                return "You have subscribed to " + role + "!"

#unsub command (aceppts unsub, desub and any **sub from combination)
async def UnsubFrom(usr,role):       
        #if lmsg.startswith("sub from",2):
            #role = lsplit[2].capitalize()
            if role in PING_ROLES:
                #await SEND(ch,"You have unsubscribed from " + role + "!")
                await REMOVE_ROLES(usr,PING_ROLES[role])
                return "You have unsubscribed from " + role + "!"
               
