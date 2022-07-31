### IMPORTS ###

import discord
import os
import random
import asyncio
import redis
from datetime import date
import time
from difflib import SequenceMatcher

## CONSTANTS ##

#chatt killer requires 2 hours of inactivity(in seconds)
CHAT_KILLER_WAIT = 7200
#player that reaches this level first will win the mini game
MINI_GAME_TOP_LEVEL = 21
MINI_GAME_MAX_WAIT = 30

#ids will be replaced with objects on startup
SERVER = 624227331720085528

#fallen drone name (to prevent impostors)
FALLEN_DRONE_NICK = "FALLEN DRONE"

#special roles
#roles that bot can assing to, but not by a regular user commannd
#values replaced by roles on startup
CKR = 951424560685805588
POSSESSED = 988572669521842197
MURDURATOR = "Murdurators"
CLIMBER = "Climbers"

#this is for administrating tips and trivia database
ADMIN = 993446701090222160

#channels where bot is allowed to post 
CHANNELS = {
    "general": 624227331720085536,
    "bot-commands": 750060041289072771,
    "crazy-stairs": 750060054090219760,  
    "bot-testing": 813882658156838923,
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
       "Our quote's founder has been identified, you are now a Spectre.",
       "Once again, Spectre's Founder went MIA.",
    ],
    "Keeper": [ 
       None,
       "The staircase is now under your supervision, you successfully became a Keeper.",
       "You failed to take care of the stairs, and so you are no longer a Keeper.",
    ],
    "Muggle": [ 
       None,
       "Work smarter, not harder. You are now a Muggle!",
       "The tower was too overwhelming for a weakling like you. Your Muggle license has been revoked.",
    ],
    "Chameleon": [ 
       None,
       "Do not let them know your next move, you are now a Chameleon!",
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
        "I saw you taking the stairs, you are no longer a Drifter.",
     ],
     "Heretic": [ 
        None,
        "We have banned dark magic, but you do not seem to care. You successfully became a Heretic.",
        "The circle has made their decision. You are permanently banned from being a Heretic ever again.",
    ],
     "Guns": [ 
        None,
        "smh, FINE!",
        "Finally you came to your senses.",
     ],
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
}
IMMUNITY_ROLES = ["Admin", "Murdurators", "Sleazel"]

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
    "It needs to be earned, sorry.":
        'morph to ultimate chat killer',
    "Tsk.":
        'cstrollpain',
    "{mention} <:csRbxangryping:786325219727638535>":
        '827952429290618943',
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
    "{mention} is a true stair jumper.":
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

IMPOSTOR_WARNINGS = [
    "It's time to stop.", "I took the liberty to change your name.",
    "Identity theft doesn't give you a good look.", "Do not try that again.",
    "There, I picked a fitting name for you.",
    "You've come a long way, phony me.",
    "There will be no phonies as long as I'm here.",
    "Copy me all you want, my knowledge is unparalleled.",
    "*Reversion of your actions is currently in progress...*",
    "I put an end to this buffoonery.", "Someone had to do it.",
    "We are through here.", "My disappointment is immeasurable.",
    "I do not speak like that.", "I am not fooled."
]

IMPOSTOR_NICKS = [
    "i am a thief",
    "my plan, foiled!",
    "unoriginal display name",
    "there was an attempt",
    "original display name",
    "funny name",
    "pin of shame",
    "could be better",
    "could be worse",
    "good job",
    "your prize",
    "Name offered by Me. F.D.",
]

RIG_LIST = [
    "thief",
    "spectre",
    "joker",
    "archon",
    "heretic",
    "patron",
    "wicked",
    "keeper",
    "hacker",
    "drifter",
]

COOLDOWN_SELECT = {
    "thief": "tsj",
    "spectre": "tsj",
    "joker": "tsj",
    "archon": "ha",
    "heretic": "ha",
    "patron": "patron",
    "wicked": "general",
    "keeper": "general",
    "hacker": "general",
    "drifter": "general",
}

SANCTUARY = {
    "muggle": " has found Muggle's Home!",
    "thief": " has found Thief's Guild!",
    "spectre": " has found Spectre's Nether!",
    "joker": " has found Joker's Circus!",
    "archon": " has found Archon's Study!",
    "heretic": " has found Heretic's Nexus!",
    "patron": " has found Patron's Haven!",
    "wicked": " has found Wicked's Chamber!",
    "keeper": " has found Muggle's Base!",
    "hacker": " has found Hacker's Backdoor!",
    "drifter": " has found Drifter's Shelter!",
    "chameleon": " has found Chameleon's Oasis!",
}

COOLDOWN_DURATION = {
    "patron": 900,    
    "thief": 600,
    "spectre": 600,
    "joker": 600,
    "archon": 120,    
    "heretic": 60,
    "wicked": 60,    
    "keeper": 20,
    "hacker": 20,
    "drifter": 20,
}

LIMITED_USE_RIGS = [
    "joker",   
    "thief",
    "spectre",
]

REVIVE_CHAT = [
    "How did you find out about Crazy Stairs?",
    "What's your least favorite Alignment?",
    "How many alignments were there in the game when you started playing?",
    "Whose alignment's power would you rather wield in real life?",
    "Nope. Chat is as dead as my intentions to revive it.",
    "Is Sleazel cool?",
    "What's your favorite feature present in the game?"
]

COOLDOWN_DESCRIPTIONS = {
    "general": "General cooldown: ",
    "tsj": "Thief, Spectre, and Joker cooldown: ",
    "ha": "Heretic and Archon cooldown: ",
    "patron": "Patron cooldown: ",
}

QUIZ = {
    "active" : False,
    "second-player" : False,
    "can-answer" : False,
    "turn" : 0,
    "cturn" : 1,
    "rolls" : [0],
    "rng" : 0,
    "scores" : "**TOTAL POINTS**\n"
}

QUIZZERS = {}
LOSERS = []

QUESTIONS = {
  1: [
    "Which game am I playing right now?",
    ["Crazy Stairs", "Lucid Ladders", "Sleazel's Revenge", "Adopt Me!"],
    "sleazel's revenge",
    " got it right, but that was pretty easy. Let's move on now.",
    "There was no way for you to get this wrong yet you surprise me!",
  ],

  2: [
    "What's the maximum amount of Mana one player can have?",
    ["22", "Infinite", "20", "10"],
    "infinite",
    " guessed it. (or maybe knew it...)",
    "Wrong answer.",
  ],

  3: [
    "How many Alignments are there in the game?",
    ["13", "12", "11", "9"],
    "12",
    " won this one, on to the next one we go.",
    "No.",
  ],

  4: [
    "How did I become Fallen Drone?",
    ["I asked Sleazel", "I fell", "Someone pushed me causing my fall", "I aged"],
    "i fell",
    " knows me all too well.",
    "Wrong.",
  ],

  5: [
    "When did I join this Discord Server?",
    ["04/03/2021", "07/01/2022", "03/04/2021", "9/29/2018"],
    "04/03/2021",
    " is correct.",
    "I forgive you.",
  ],

  6: [
    "Originally, how did the Final Orb work?",
    ["Same as now", "It stood still in a room at the top floor", "Same as now but it stood still", "It was moving in a room at the top floor"],
    "it stood still in a room at the top floor",
    " guessed it. (or maybe knew it...)",
    "Wrong answer.",
  ],

  7: [
    "Which was the latest Badge added in Crazy Stairs?",
    ["Super Secret Badge", "Mega Secret Badge", "Architect's Design", "Possessed Fate"],
    "mega secret badge",
    " won this one, on to the next one we go.",
    "Wrong, you haven't been paying attention.",
  ],

  8: [
    "How much Mana do players actually have when Infinite Mana is active?",
    ["100", "Infinite", "50", "1000"],
    "100",
    " is a genius.",
    "Wrong.",
  ],

  9: [
    "Which of these names Sleazel has never used in Discord?",
    ["Sleazy Guy", "Malcolm", "Sleaz", "Archon"],
    "sleazy guy",
    " has been stalking Sleazel.",
    "Better luck next time.",
  ],

  10: [
    "How were the Drones originally referred as?",
    ["Keepers", "Drones", "Overseers", "Guardians"],
    "keepers",
    " was paying attention during class.",
    "Not correct.",
  ],

  11: [
    "How was the first Admin of this Discord Server called?",
    ["bash1234567888", "wheredidthesungo", "LizzyTheAdventurer", "jeff"],
    "bash1234567888",
    " has been here for too long.",
    "The answer provided doesn't match the correct one.",
  ],

  12: [
    "Which one of the following was NOT part of the Original Trinity?",
    ["Patron", "Joker", "Thief", "Wicked"],
    "thief",
    " is indeed correct.",
    "Better luck next time.",
  ],

  13: [
    "How many Drones are there in each Crazy Stairs server?",
    ["9", "8", "7", "10"],
    "9",
    " is not wrong, even though I'm more than a mere Drone.",
    "You tried, and failed.",
  ],

  14: [
    "How many intersecations does each Drone handle?",
    ["3", "2", "1", "4"],
    "3",
    " checked the General Trivia.",
    "Nope.",
  ],

  15: [
    "How much does it cost (Robux) to refill your Mana in Crazy Stairs?",
    ["10", "15", "No such feature in the game", "20"],
    "10",
    " has refilled their Mana once, or tried to.",
    "Totally wrong.",
  ],

  16: [
    "Which Mana orb gives 3 Mana?",
    ["Yellow", "Blue", "Green", "Red"],
    "yellow",
    " somehow knew the answer.",
    "Have you ever played the game?",
  ],

  17: [
    "How many Climbs are required to unlock the last rank of an alignment?",
    ["50", "25", "60", "30"],
    "50",
    " is correct.",
    "Incorrect.",
  ],

  18: [
    "Which one of the following is NOT a way to get unpossessed?",
    ["Trigger a Chameleon Rig", "Reset", "Receive Mana from another player", "Trigger a Patron Rig"],
    "Receive Mana from another player",
    " somehow knew the answer.",
    "Have you ever played the game?",
  ],

  19: [
    "Whose alignment's icon does the lobby's shape resemble?",
    ["Hacker", "Patron", "Wicked", "Thief"],
    "hacker",
    " answered correctly.",
    "Try zooming out every now and then.",
  ],

  20: [
    "Which alignment does NOT get a switch upon ranking up?",
    ["Wicked", "Archon", "Joker", "Heretic"],
    "Heretic",
    " guessed the correct answer.",
    "You gotta rank up your alignments.",
  ],
}

MG_SPELLS = [
    "none",
    "muggle",
    "patron",
    "joker",
    "wicked",
    "spectre",
    "keeper",
    "thief",
    "hacker",
    "archon",
    "drifter",
    "heretic",
    "chameleon",
]

### GLOBAL VARIABLES ###

# for chat killer role, time when the last message was sent
# (seconds from unix epoch)
Last = 0
rigCaster = None
ghostMsg = ""
thirdkill = None
revivechat = False

ACTIVE_RIGS = {
    "joker": False,
    "thief": False,
    "spectre": False,
}

RIG_COOLDOWNS = {
    "general": False,
    "tsj": False,
    "ha": False,
    "patron": False,
}

RIG_SPAMMERS = {}
NickDictionary = {}

MG_STATUS = "off"
MG_CHANNEL = None
MG_CURRENT_PLR = 0
MG_TICK = 0
MG_WIN_DETECT = 0
MG_PLAYERS = {}
MG_QUEUE = []
#if game breaks there must be 3 people telling the bot to reset
FIX_BOT = []


### INITIAL SETUP ###

# This allows us to know if user has updated their presence
# Mosty for the gun role nick change prevention
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Set up the data base
db = redis.from_url(os.environ.get("REDIS_URL"))

### PRIVATE SYNC FUNTIONS ###

def add_entry(key, new_entry):
    db.rpush(key,new_entry)

def delete_entry(key, index):
    db.lset(key,index,"_del_")
    db.lrem(key,1,"_del_")

def list_entries(key):
    result = db.lrange(key,0,-1)
    return result

def show_random_entry(key):
    index = random.randint(0,db.llen(key)-1)
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")

def get_amount_of_entries(key):
    return db.llen(key)

def show_specific_entry(key,index):
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")
    
async def CLOSE_EVENT():
  print("entered")
  await asyncio.sleep(30)
  print("30 sec passed")
  if QUIZ["turn"] == QUIZ["cturn"] and QUIZ["active"]:
    print("same turns has been going on for 30 seconds")
    QUIZ["turn"] = 0
    QUIZ["cturn"] = -5
    QUIZ["active"] = False
    QUIZ["second-player"] = False
    QUIZ["can-answer"] = False
    QUIZ["rolls"].clear()
    QUIZ["scores"] = "**TOTAL POINTS**\n"
    QUIZZERS.clear()
    LOSERS.clear()
    return True

  print("not the same turn")
  QUIZ["cturn"] += 1
  return False

def FORCE_CLOSE_EVENT():
  QUIZ["turn"] = 0
  QUIZ["cturn"] = -5
  QUIZ["active"] = False
  QUIZ["second-player"] = False
  QUIZ["can-answer"] = False
  QUIZ["rolls"].clear()
  QUIZ["scores"] = "**TOTAL POINTS**\n"
  QUIZZERS.clear()
  LOSERS.clear()
  return

def showScores():
    for i in QUIZZERS:
        QUIZ["scores"] += str(i.nick) + "'s points: " + str(QUIZZERS[i]) + "\n"
    return QUIZ["scores"]

async def nextQuestion(ch):
    usefulkeys = list(QUESTIONS.keys())
    QUIZ["rng"] = random.choice(usefulkeys)
    while QUIZ["rng"] in QUIZ["rolls"]:
        QUIZ["rng"] = random.choice(usefulkeys)

    QUIZ["rolls"].append(QUIZ["rng"])
    answers = ""
    qnum = "*Question no. " + str(QUIZ["turn"]) + "*\n"
    await SEND(ch, qnum + ":question: " + QUESTIONS[QUIZ["rng"]][0])

    random.shuffle(QUESTIONS[QUIZ["rng"]][1])   
    for i in QUESTIONS[QUIZ["rng"]][1]:
        answers += ":arrow_forward: `" + i + "` \n"

    await SEND(ch, answers)
    QUIZ["can-answer"] = True
    
    return

def getScoldDictionary(victim, author):
    ScoldDict = {
        481893862864846861:
            "I am thankful to my creator, not disappointed.",
        827952429290618943:
            author.mention + " nice try.",
        828423681914437663:
            victim.mention + ", I am EXTREMELY disappointed in you. You know why. I do not forget.",
        author.id:
            author.mention + " you do not need Me to be disappointed in yourself.",
    }
    return ScoldDict

def rigImmunity(usr1, usr2):
    for roles in usr1.roles:
        if roles.name in IMMUNITY_ROLES:
            return True
    if usr1 == usr2:
        return True
    return False

def MG_RESET():
    global MG_STATUS
    global MG_CHANNEL 
    global MG_CURRENT_PLR 
    global MG_WIN_DETECT
    
    MG_PLAYERS.clear()
    MG_QUEUE.clear()
    MG_STATUS = "off"
    MG_CHANNEL = None
    MG_CURRENT_PLR = 0
    MG_WIN_DETECT = 0
    
def MG_SHOW_STATS():

    global MG_WIN_DETECT
    
    toSend = "\nCurrent placements:\n"
    for plr, place in MG_PLAYERS.items():
        toSend += "**" + plr.name + "**: " + str(place) + " floor\n"
        if place > MG_WIN_DETECT:
            MG_WIN_DETECT = place
    toSend += "-------------\n"
    return toSend

def MG_NEXT_PLAYER():
    global MG_CURRENT_PLR
    MG_CURRENT_PLR += 1
    if MG_CURRENT_PLR > len(MG_QUEUE) - 1:
        MG_CURRENT_PLR = 0
      

def MG_SHOW_WINNERS():
    winners = []
    for i, v in MG_PLAYERS.items():
        if v >= MINI_GAME_TOP_LEVEL:
            winners.append(i)
                        
    toSend = winners[0].mention
    if len(winners) > 1:
        for i in range(1,len(winners)):
            toSend += " and " + winners[i].mention
    
    return toSend + " won LUCID LADDERS!"                    
    
def MG_ACTION(plr, action):
    
    global MG_CURRENT_PLR 
     
    #all players always advance 1 level per round
    for i in MG_PLAYERS.keys():
        MG_PLAYERS[i] += 1
        
    toSend = "All players advance 1 level.\n**" + plr.name + "** has played " + action + ". They "
    
    match action:
        case "none":
            toSend += "are chilling this round."
            
        case "muggle":
            chances = random.randint(0, 2)
            if chances == 2:
                MG_PLAYERS[plr] -= 1
                toSend += "got stuck and had to go down 1 level!"
            else:
                MG_PLAYERS[plr] += 1
                toSend += "did a stairjump trick, and advanced 1 extra level!"
                
        case "patron":
            ourLevel = MG_PLAYERS[plr]
            for i, v in MG_PLAYERS.items():
                if v <= ourLevel:
                    MG_PLAYERS[i] += 1
            toSend += "advanced 1 extra level with all other players below them."
                
        case "joker":
            victim = random.choice(MG_QUEUE)
            if victim != plr:
                toSend += "pranked " + victim.display_name + " - causing them to fell 2 levels down!"
                MG_PLAYERS[victim] -= 2
            else:
                toSend += "pranked themselves, and fell 1 level down."
                MG_PLAYERS[victim] -= 1
        
        case "wicked":
            ourLevel = MG_PLAYERS[plr]
            for i, v in MG_PLAYERS.items():
                if v > ourLevel:
                    MG_PLAYERS[i] -= 1
            toSend += "purged the stairs and above players fell one level."
            
        case "spectre":
            chances = random.randint(-1, 2)
            MG_PLAYERS[plr] += chances
            if chances == -1:
                toSend += "had a teleportation accident and lost one level!"
            elif chances == 0:
                toSend += "did not get any advantage."
            elif chances == 1:
                toSend += "teleported one extra level up."
            elif chances == 2:
                toSend += "teleported two extra levels up."
         
        case "keeper":
            toSend += "caused bottom player to advance an extra level and top player to go down!"
            top = None
            bottom = None
            topl = -99999999
            bottoml = 9999999
            for i, v in MG_PLAYERS.items():
               if v < bottoml:
                    bottom = i
                    bottoml = v
               if v > topl:
                    top = i
                    topl = v
            MG_PLAYERS[top] -=1
            MG_PLAYERS[bottom] += 1
            
        case "thief":
            victim = random.choice(MG_QUEUE)
            if victim != plr:
                toSend += "have stolen " + victim.display_name + " place!"
                cache = MG_PLAYERS[victim]
                MG_PLAYERS[victim] = MG_PLAYERS[plr]
                MG_PLAYERS[plr] = cache
            else:
                toSend += "have been caught stealing, and had to flee one level down!"
                MG_PLAYERS[plr] -= 1
            
        case "hacker":
            chances = random.randint(0, 3)
            if chances == 0:
                toSend += "have been kicked from the game for hacking!"
                
                cp = MG_QUEUE[MG_CURRENT_PLR]
                del MG_PLAYERS[plr]
                MG_QUEUE.remove(plr)
                MG_CURRENT_PLR = MG_QUEUE.index(cp)
                if len(MG_QUEUE) == 1:
                    MG_PLAYERS[cp] = MINI_GAME_TOP_LEVEL
                
            elif chances == 1:
                toSend += "have been frozen by a Murdurator and lost one level!"
                MG_PLAYERS[plr] -= 1
            elif chances == 2:
                toSend += "have had an unsuccessful hack, but was not detected!"
            else:
                toSend += "have hacked the game!"
                for i in MG_PLAYERS.keys():
                    MG_PLAYERS[i] -= 1
                MG_PLAYERS[plr] = MINI_GAME_TOP_LEVEL
                
        case "archon":
            toSend += "cast Split Event and caused players to either lost or gain a extra level."
            for i in MG_PLAYERS.keys():
                chances = random.randint(0,1)
                if chances == 0 or i == plr:
                    MG_PLAYERS[i] += 1
                else:
                    MG_PLAYERS[i] -= 1
        
        case "drifter":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "took the elevator, but it was broken - a level was lost"
                MG_PLAYERS[plr] -= 1
            else:
                toSend += "took the elevator, and advanced 2 extra levels!"
                MG_PLAYERS[plr] += 2
                
        case "heretic":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "performed a dark ritual and swapped first and last players!"
                top = None
                bottom = None
                topl = -99999999
                bottoml = 9999999
                for i, v in MG_PLAYERS.items():
                    if v < bottoml:
                        bottom = i
                        bottoml = v
                    if v > topl:
                        top = i
                        topl = v
                cache = MG_PLAYERS[top]
                MG_PLAYERS[top] = MG_PLAYERS[bottom]
                MG_PLAYERS[bottom] = cache
            else:
                toSend += "failed to perform a dark ritual and got stranded - a level was lost."
                MG_PLAYERS[plr] -= 1
                
    return toSend

### RATE LIMITED FUNCTIONS ###

def GET_CHANNEL(id):
    return client.get_channel(id)

def GET_EMOJI(id):
    return client.get_emoji(id)

#get up to date ckr members
def UPDATE_CKR():
    global CKR
    CKR = SERVER.get_role(CKR.id)

### PRIVATE ASYNC FUNCTIONS ###
async def SEND(channel,message):
    if message == None or message == "":
        #cannot send empty message
        return
    return await channel.send(message)

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
    
#add reaction    
async def ADD_REACTION(msg,reaction):
    await msg.add_reaction(reaction)

#edit message
async def EDIT_MESSAGE(msg, con):
    await msg.edit(content=con)
    
async def DELETE(message):
  await message.delete()

async def EDIT_ROLE(targetrole, newname, motivation):
  await targetrole.edit(name = newname, reason = motivation)

async def NEW_ROLE(colorpick, rolename):
  await SERVER.create_role(name = rolename, color = discord.Colour(int("0x" + str(colorpick))))

### END OF RATE LIMITED FUNCTIONS ###

#below function can also cause rate limts, but
#they are using only above functions so we do not need 
#to worry about these ones

#print tips
async def PRINT_ENTRIES(channel,key):
    entries = list_entries(key)
    combined_string = ""
    for i in range(len(entries)):
        new_string = combined_string + str(i) + ") " + entries[i].decode("utf-8") + "\n"
        if len(new_string) > 2000:
            await SEND(channel,combined_string)
            combined_string = str(i) + ") " + entries[i].decode("utf-8") + "\n"
        else:
            combined_string = new_string
    await SEND(channel,combined_string)

#chat killer functions
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

            if CKR.name != "Definitive Ultimate Chat Killer":
                await EDIT_ROLE(CKR, "Definitive Ultimate Chat Killer", "This user has killed the chat twice in a row.")
            return
                


### RIGS ###

async def Rig(rigType, ch, usr):
   
    if RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]]:
        await SEND(ch, "Ultimate spells are in cooldown.")
        return
        
    spamCount = 0
    if usr in RIG_SPAMMERS:
        spamCount = RIG_SPAMMERS[usr]
    
    if rigType in LIMITED_USE_RIGS:
        if spamCount == 3:
            await SEND(ch, "You've been using these commands too often.")
            return
        else:
            spamCount += 1
            RIG_SPAMMERS[usr] = spamCount
            
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = True
    global rigCaster
    
    messageAppend = "."
    match rigType:
        
        case "heretic":
            if MURDURATOR in usr.roles:
                await SEND(ch, "You cast Heretic Rig but thanks to your Unbeliever rank, you didn't get possessed.")
                RIG_COOLDOWNS["ha"] = False
                return
            #for member in SERVER.members:
               # if POSSESSED in member.roles:
                   # await SEND(ch, "Another ultimate spell is in progress. Please wait.")
                   # RIG_COOLDOWNS["ha"] = False
                   # return
            await ADD_ROLES(usr, POSSESSED)
            await asyncio.sleep(1)
            await SEND(ch,"You cast Heretic Rig but forgot to unlock Unbeliever rank first and ended up getting Possessed..."
                       "\nMaybe someone could give you some Mana?")
            await asyncio.sleep(60)
            await REMOVE_ROLES(usr, POSSESSED)
            
        case "wicked":
            role_list = []
            for role in usr.roles:
                if role.name in MORPHABLE_ROLES or role.name in PING_ROLES:
                    role_list.append(role)
            #TODO: Rolo, check if we can use REMOVE_ROLES() function here...
            await usr.remove_roles(*role_list)       
            await SEND(ch, "You cast Wicked Rig but forgot to unlock Devil rank first and ended up purging all your roles!")
         
        case "drifter":
            im = usr.display_name[::-1]
            await EDIT_NICK(usr, im)
            await SEND(ch, "You cast Drifter Rig but forgot to unlock Voyager rank first and now your name is reversed...")
            
        case "archon":
            if ch.name not in CHANNELS:
                await SEND(ch, "Impossible to create a Split here. This channel is restricted.")
                RIG_COOLDOWNS["ha"] = False
                return
            ch2 = ch
            while ch2 == ch or ch2.name == "bot-testing":
                ch2 = random.choice(list(CHANNELS.values()))
            firstmsg = await SEND(ch, "You cast Archon Rig and created a Split in another channel!")
            await SEND(ch, "https://media.giphy.com/media/LUjKnselKZBc5Zb4t4/giphy.gif")
            await asyncio.sleep(3)
            secondmsg = await SEND(ch2, usr.mention + " has just created a Split in this channel! They come from "
                + ch.mention + ". " + firstmsg.jump_url)
            await SEND(ch2, "https://media.giphy.com/media/QM1yEJoR1Z7oKAGg4Y/giphy.gif")
            await asyncio.sleep(3)
            await EDIT_MESSAGE(firstmsg, firstmsg.content + " " + secondmsg.jump_url)           
        
        case "hacker":
            im = ""
            for i in range(8):
                temp = str(random.randint(0, 1))
                im += temp
            await SEND(ch, "You cast Hacker Rig an- anddd##dddddddd############")
            await asyncio.sleep(3)
            await EDIT_NICK(usr, im)
            if usr.display_name == '11111111' or usr.display_name == '00000000':
                await SEND(ch, "That's some luck right there.")
            
        case "keeper":
            im = ''.join(sorted(usr.display_name))
            await EDIT_NICK(usr, im)
            await asyncio.sleep(1)
            await SEND(ch, "You cast Keeper Rig and now your name is alphabetically ordered!")
        
        case "patron":
            rigActive = False
            for active in ACTIVE_RIGS.values():
                if active:
                    rigActive = True
                    break
            if not rigActive:
                await SEND(ch, "It would be useless casting this spell now.")
                RIG_COOLDOWNS["patron"] = False
                return
            await SEND(ch, "You cast Patron Rig and restored the Server!")
            for rig in ACTIVE_RIGS.keys():
                ACTIVE_RIGS[rig] = False
                
        case ("joker"|"thief"|"spectre"):
            ACTIVE_RIGS[rigType] = True
            rigCaster = usr
            if rigType == "joker":
                await SEND(ch, usr.mention + " just cast Joker Rig. Someone will be in for a treat.")
            elif rigType == "thief":
                await SEND(ch, usr.mention + " just cast Thief Rig! Watch out everyone.")
            else:
                await SEND(ch, usr.mention + " just cast Spectre Rig! Careful.")
                
          
            
    await asyncio.sleep(COOLDOWN_DURATION[rigType])

    if rigType in LIMITED_USE_RIGS and ACTIVE_RIGS[rigType] == True:
        ACTIVE_RIGS[rigType] = False
        messageAppend = ", and the current Rig effect has worn off."
    RIG_COOLDOWNS[COOLDOWN_SELECT[rigType]] = False

    await SEND(ch, rigType.capitalize() + " Rig cooldown is over" + messageAppend)
    
    #reset spam count
    await asyncio.sleep(3600)
    if usr in RIG_SPAMMERS and spamCount == RIG_SPAMMERS[usr]:
        del RIG_SPAMMERS[usr]
   
async def necromancer(message):
  global ghostedMsg
  
  if ghostMsg != "":
    await SEND(message, ghostMsg)
  else:
    await SEND(message, "*but nobody came...*")


    
async def MG_LOOP(toSend):
    
    global MG_TICK
    MG_TICK = time.time()
    ourTick = MG_TICK
    
    while True:
        
        toSend += MG_SHOW_STATS()
        if MG_WIN_DETECT >= MINI_GAME_TOP_LEVEL or len(MG_QUEUE) < 2:
            toSend += MG_SHOW_WINNERS()
            await SEND(MG_CHANNEL, toSend)
            MG_RESET()
            return
        else:
            toSend += "**" + MG_QUEUE[MG_CURRENT_PLR].name + "** turn! Choose Your alignment!"
            await SEND(MG_CHANNEL, toSend)
        
        await asyncio.sleep(MINI_GAME_MAX_WAIT)
        
        if MG_TICK != ourTick:
            return
        
        cp = MG_QUEUE[MG_CURRENT_PLR]
        MG_NEXT_PLAYER()
        toSend = MG_ACTION(cp,"none")
        
         
    
### PUBLIC (ON EVENT) FUNCTIONS ###
    
#drone start up, prepare roles here
@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Sleazel's Revenge")
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
    global MURDURATOR
    global CLIMBER
    global ADMIN
    for role in SERVER.roles:
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
            
    #prepare emojis reactions
    for i, v in EMOJIS_TO_REACT.items():
        EMOJIS_TO_REACT[i] = GET_EMOJI(v)
    
    #send ready to the test channel
    await SEND(CHANNELS["bot-testing"],'The last edited code is now effective.')

#member update, prevent changing gun nick to anything other than the gun name
@client.event
async def on_member_update(before, after):
    
    #nick has not changed
    if before.nick == after.nick:
        return
    
    #for thief rig
    if before in NickDictionary and after.nick != NickDictionary[before]:
      await EDIT_NICK(after, NickDictionary[before])
      return
 
    #is user a gun?
    if not MORPHABLE_ROLES["Guns"][0] in before.roles:
        return
    
    #ignore if user nick after change is a gun name
    if after.nick in WORST_GUNS:
        return

    await EDIT_NICK(after, random.choice(WORST_GUNS))
    return

#on new member join
@client.event
async def on_member_join(member):
    await SEND(CHANNELS["general"],
        "Welcome to Crazy Stairs Discord Server!"
        "\nUnlike other Jokers around here, I am a real bot."
        "\nPlease read the <#750056989207429143>, to avoid misunderstandings."
        "\nHave fun, and remember: It's okay to be a little crazy.")

#saves last deleted message for necromancer rig to show
@client.event
async def on_message_delete(message):
  global ghostMsg
  ghostMsg = "*" + str(message.author.nick) + " last words lie here...*"
    
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
                await ADD_REACTION(message,v)
                return
        return

    randomchance = random.randint(0,1000)
    eligible = 0
    rolename = ""

    if randomchance == 0:
        for role in usr.roles:
            if role.name.lower() in SANCTUARY:
                eligible = eligible + 1                
                if eligible == 1:
                    rolename = role.name.lower()

        
        if eligible == 1:
            await SEND(CHANNELS["bot-commands"], usr.mention + SANCTUARY[rolename] + " (1/1000 chance)")
    
    #this will avoid old activatig with old bot
    if msg.startswith(">"):
        return
    
    #mini game
    global MG_STATUS
    global MG_CHANNEL 
    global MG_CURRENT_PLR 
    global MG_TICK
    global FIX_BOT
    
    if msg.lower() == "reset bot" and usr not in FIX_BOT:
        if ADMIN in usr.roles:
            await SEND(ch, "All Games have been resetted.")
            FIX_BOT.clear()
            FORCE_CLOSE_EVENT()
            MG_RESET()
            return

        FIX_BOT.append(usr)
        if len(FIX_BOT) == 1:
            await SEND(ch, "One User wants me to reset. 2 more people are required for it to take effect.")
        elif len(FIX_BOT) == 2:
            await SEND(ch, "Two Users want me to reset. 1 more person is required for it to take effect.")
        else:
            await SEND(ch, "All Games have been resetted.")
            FIX_BOT.clear()
            FORCE_CLOSE_EVENT()
            MG_RESET()


        await asyncio.sleep(60)
        if len(FIX_BOT) != 0:
            await SEND(ch, "Games have not been resetted due to lack of users asking to.")
            FIX_BOT.clear()
        return

    #mini game in progress
    if MG_STATUS != "off" and usr in MG_QUEUE and ch == MG_CHANNEL:
        
        lmsg = msg.lower()
        
        if MG_STATUS == "gather" and lmsg == "begin" and usr == MG_QUEUE[0]:
            
            if len(MG_QUEUE) < 2:
                await SEND(MG_CHANNEL, "Not enough players for the Lucid Ladders to begin!")
                return
            
            MG_STATUS = "on"
            await MG_LOOP("Lucid Ladders have begun!")            
            
            return
        
        elif MG_STATUS == "on" and lmsg in MG_SPELLS and MG_QUEUE[MG_CURRENT_PLR] == usr:
            spell = lmsg
            while spell == "chameleon":
                spell = random.choice(MG_SPELLS)
            MG_NEXT_PLAYER()
            await MG_LOOP(MG_ACTION(usr,spell))
       
    #normal non-admin usage.
    elif not msg.startswith("|"):
        
        ## lowercase the message for some commands to use
        lmsg = msg.lower()
        ## split the message to 3 strings for some commands to use
        ## no need to have more than 4 strings
        lsplit = lmsg.split(" ",3) 
        
        #create chat killer task
        #this should run regardless if the message was intercepted
        #by some other command
        ckr_task = asyncio.create_task(WAIT_FOR_CHAT_KILLER(message))
 
        #fallen drone impostor prevention
        compare = SequenceMatcher(None, usr.display_name.upper(), FALLEN_DRONE_NICK)
        if compare.ratio() > 0.5:
            await SEND(ch, usr.mention + ' ' + random.choice(IMPOSTOR_WARNINGS))
            await EDIT_NICK(usr,random.choice(IMPOSTOR_NICKS))
            return

        #start the quiz
        if ch == CHANNELS["bot-commands"] and lmsg == "fallen drone start quiz" and not QUIZ["active"] and not QUIZ["second-player"]:
            #add user to the quiz users with 0 points.
            QUIZZERS[usr] = 0

            #activates the quiz, activates looking for second player.
            QUIZ["active"] = True
            QUIZ["second-player"] = True
            await SEND(ch, usr.mention + " just started the Crazy Stairs Quiz!\nType 'join quiz' to begin with the questions. (BETA)")

            #if no one joins within 10 seconds, event is forced closed.
            await asyncio.sleep(10)
            if QUIZ["second-player"] == True:
                await SEND(ch, "Nobody joined in time. Event is concluded.")
                FORCE_CLOSE_EVENT()
            return

        #join an ongoing quiz
        if ch == CHANNELS["bot-commands"] and lmsg == "join quiz" and QUIZ["second-player"] and usr not in QUIZZERS:
            #disables looking for second player
            QUIZ["second-player"] = False
            #adds the new user to the quiz users
            QUIZZERS[usr] = 0
            #preparation to announce the two players
            users = list(QUIZZERS.keys())
            quizzerson = users[0].mention + " and " + users[1].mention + " have joined the Quiz. Questions are to follow. Good luck."
            await SEND(ch, quizzerson)
            #turn started from 0, now it begins
            QUIZ["turn"] += 1
            QUIZ["cturn"] = 1
            #prevents other people from talking while there is a quiz. avoids suggestions.
            #(this command cannot be used outside of bot-commands)
            await asyncio.sleep(2)
            await SEND(ch, "Beyond this point, any message sent from non-participating Users will be deleted.")
            #proceeds with the next(first in this case) question
            await asyncio.sleep(2)
            await nextQuestion(ch)
            #after starting, check if the round has been going on for more than 30 seconds.
            #if positive, close the event and send the message
            if await CLOSE_EVENT():
                await SEND(ch, "Event is concluded because both parts couldn't answer my very simple question.")
            return

        if ch == CHANNELS["bot-commands"] and QUIZ["active"] and not QUIZ["second-player"] and QUIZ["can-answer"]:
            if usr not in QUIZZERS:
                await DELETE(message)
                return
            
            #if one of the two wants to stop they can feel free to
            if lmsg == "stop quiz":
                await SEND(ch, showScores() + usr.mention + " stopped the Quiz. Event is over.")
                FORCE_CLOSE_EVENT()
                return

            #each user gets one try at guessing the answer.
            #if you lost your attempt, wait for the other user to guess (or fail... concluding the event)
            if usr in LOSERS:
                await SEND(ch, "You have wasted your chance. Let the other User play now.")
                return

            #if the answer is not correct enter here
            if lmsg != QUESTIONS[QUIZ["rng"]][2].lower():
                #message is not correct but user is not in the LOSERS yet (otherwise code would have stopped before)
                #then a loser they become.
                if usr not in LOSERS:
                    LOSERS.append(usr)

                #no return here. after adding a user, checks if both users are losers
                #if they are, the event gets forced closed.
                if len(LOSERS) == 2:
                    await SEND(ch, showScores() + "Both players have not answered the question correctly. Event is over.")
                    FORCE_CLOSE_EVENT()
                    return

                #if it is the first user to get the answer wrong, then show fallen's disappointment.
                await SEND(ch, QUESTIONS[QUIZ["rng"]][4])
                return

            #go here instead if the answer it not incorrect (which means it is correct indeed)
            #show fallen's approval to the guessing user.
            QUIZ["can-answer"] = False
            finalmsg = ""
            if QUIZ["turn"] + 1 > len(QUESTIONS):
              finalmsg = QUESTIONS[QUIZ["rng"]][3]
            else:
              finalmsg = QUESTIONS[QUIZ["rng"]][3] + "\nBoth Players can now answer the next question."
            await SEND(ch, usr.mention + finalmsg)
            #the user who misguessed the answered gets a second chance (might it be the second or third depending on the round tho-)
            LOSERS.clear()
            #guesser gains 1 point
            QUIZZERS[usr] += 1
            #to the next turn we go (unless we want the same question to repeat itself)
            QUIZ["turn"] += 1
            await asyncio.sleep(5)

            #go here if there are no more questions
            if QUIZ["turn"] > len(QUESTIONS):
                highscore = -1
                for i in QUIZZERS:
                    if QUIZZERS[i] > highscore:
                        winner = i
                        highscore = QUIZZERS[i]
                    elif QUIZZERS[i] == highscore:
                        await SEND(ch, showScores() + "That's a tie. But we do not like ties. Play again.")
                        FORCE_CLOSE_EVENT()
                        return

                #and the winner is (not you)
                await SEND(ch, showScores() + winner.mention + " correctly answered most of the questions and won the Event. Felicitations.")
                FORCE_CLOSE_EVENT()
                return

            #if there are more questions go here
            #after going to the next round check if the next round lasts more than 30 seconds
            await nextQuestion(ch)
            if await CLOSE_EVENT():
                await SEND(ch, showScores() + "Event is concluded because both parts couldn't answer my very simple question.")
            return      

        #start mini game
        if lmsg == "play lucid ladders":
            if MG_STATUS != "off":
                await SEND(ch, "A game is already in progress. Please wait for it to finish.")
                return
            else:
                MG_STATUS = "gather"
                MG_PLAYERS[usr] = 0
                MG_QUEUE.append(usr)
                MG_CURRENT_PLR = 0
                MG_CHANNEL = ch
                MG_TICK = time.time()
                ourTick = MG_TICK
                await SEND(ch, usr.name + " has started new Lucid Ladders game! Type 'join' to join!\n" + usr.name + " - type 'begin' to start!")
                await asyncio.sleep(60)
                if MG_STATUS == "gather" and ourTick == MG_TICK:
                    await SEND(ch, "Lucid Ladders have been cancelled due to inactivity.")
                    MG_RESET()
                return
        
        #join mini game
        if lmsg == "join" and MG_STATUS == "gather" and MG_CHANNEL == ch:
            if usr in MG_PLAYERS:
                await SEND(ch, "You have already joined the mini game!")
                return
            else:
                MG_PLAYERS[usr] = 0
                MG_QUEUE.append(usr)
                toSend = usr.name + " has joined Lucid Ladders!\nCurrent players:\n"
                for plr in MG_QUEUE:
                    toSend += plr.name + "\n"
                await SEND(ch, toSend)
                return

        ## All Rigs in one
        if lsplit[0] == "cast" and lsplit[2] == "rig":
            rigPick = lsplit[1]
            if rigPick == "chameleon":
                cd = False
                for active in RIG_COOLDOWNS.values():
                    if active:
                        cd = True
                        break
                if cd:
                    cdList = ""
                    for i, v in RIG_COOLDOWNS.items():
                        cdList += COOLDOWN_DESCRIPTIONS[i]
                        if v:
                            cdList += ":x: \n"
                        else:
                            cdList += ":white_check_mark: \n"
                    await SEND(ch, " All cooldowns must be over for this Rig to take place. \n" + cdList)
                    return

                await SEND(ch, "*drum roll*")
                await asyncio.sleep(4)
                await Rig(random.choice(RIG_LIST),ch,usr)
                return
            if rigPick not in RIG_LIST and rigPick != "necromancer":
                await SEND(ch, rigPick + " is not a valid Rig. Try again.")
                return

            if rigPick == "necromancer":
              await necromancer(ch)
              return

            await Rig(rigPick,ch,usr)
            return
        
        ## thief rig active
        if ACTIVE_RIGS["thief"]:
          
            if ch.name not in CHANNELS or len(rigCaster.display_name + ", " + usr.display_name) > 32 or not CLIMBER in usr.roles or rigImmunity(usr, rigCaster):
                return
                          
            ACTIVE_RIGS["thief"] = False
            victim = usr.display_name

            NickDictionary[usr] = "N/A"
            await EDIT_NICK(usr, "N/A")

            await asyncio.sleep(1)
          
            if rigCaster in NickDictionary:
              NickDictionary[rigCaster] = rigCaster.display_name + ", " + victim
              await EDIT_NICK(rigCaster, NickDictionary[rigCaster])
              await SEND(ch, rigCaster.mention + " has just stolen your name!")
              return
              
            await EDIT_NICK(rigCaster, rigCaster.display_name + ", " + victim)
            await SEND(ch, rigCaster.mention + " has just stolen your name!")
          
            await asyncio.sleep(1800)
            del NickDictionary[usr]
            return

        ## Spectre Rig Active
        if ACTIVE_RIGS["spectre"]:
            
            if ch.name not in CHANNELS or rigImmunity(usr, rigCaster) or not CLIMBER in usr.roles:
                return
            ACTIVE_RIGS["spectre"] = False

            chances = random.randint(0, 1)

            if chances == 1:
                await SEND(ch, rigCaster.mention + " has made your Message disappear with a 50% chance!")
                await DELETE(message)
                return

            await SEND(ch, rigCaster.mention + " has NOT made your Message disappear with a 50% chance.")
            return

        ## Joker Rig Active
        if ACTIVE_RIGS["joker"]:
            
            if ch.name not in CHANNELS or not CLIMBER in usr.roles or msg.startswith("https"):
                return
            ACTIVE_RIGS["joker"] = False

            msgcontent = message.content

            await DELETE(message)
            await asyncio.sleep(2)

            await SEND(ch, str(msgcontent) + " -" + ":nerd::clown:")
          
            return

        ## Give Mana command
        if msg.lower().startswith("give mana to "):
            global POSSESSED
            role = POSSESSED
            split_message = msg.split(" ", 3)
            target = split_message[3].lower()
            for member in SERVER.members:
                if member.name.lower() + "#" + member.discriminator == target:
                    if role in member.roles:
                        await SEND(message.channel,
                            member.display_name +
                            " has received some Mana and is no longer Possessed!"
                        )
                        await asyncio.sleep(3)
                       # await member.remove_roles(role)
                        await REMOVE_ROLES(member, role)
                    else:
                        await SEND(message.channel,
                            member.display_name +
                            " received your Mana, but they do not seem to need it."
                        )
                    return
            await SEND(message.channel,
                "Who are you trying to share your Mana with?")
            return

                 
        ## Scold command
        if lmsg.startswith("fallen drone scold "):
            finalmsg = None
            for member in SERVER.members:
                if member.name.lower() + "#" + member.discriminator == lsplit[3]:
                    ScoldDict = getScoldDictionary(member, usr)
                    # Scold someone in the Dictionary (User itself included)
                    if member.id in ScoldDict:
                        finalmsg = ScoldDict[member.id]
                    # Scolding a Bot
                    elif member.bot:
                        finalmsg = "I love my bot friends."
                    # Scolding an User that is in the Server
                    else:
                        finalmsg = member.display_name + ", I am very disappointed in you."
                    await SEND(ch,finalmsg)
                    return
            # Scolding an User that is NOT in the Server
            await SEND(ch, usr.mention + " I am disappointed, you couldn't even give me a correct name.")
            return

        ## Revive Chat Command
        if "revive" in lmsg and "chat" in lmsg and len(lmsg.split(" ")) < 4:
            global revivechat
            #chat has to be dead, duh
            if not revivechat:
                await SEND(ch, "This chat is very much alive, I am afraid.")
                return

            #only chat killers can use the command
            if not CKR in message.author.roles:
                await SEND(ch, "It is not your fault.")
                return

            await SEND(ch, "Reedeming yourself? Alright.")
            await asyncio.sleep(2)
            await SEND(ch, random.choice(REVIVE_CHAT))
            revivechat = False
            return

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
            if role in SPECIAL_ROLES:
                if SPECIAL_ROLES[role][0] in usr.roles:
                    await SEND(ch,SPECIAL_ROLES[role][2])
                else:
                    await SEND(ch,SPECIAL_ROLES[role][1])
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
            if role in SPECIAL_ROLES:
                if SPECIAL_ROLES[role][0] in usr.roles:
                    await SEND(ch,SPECIAL_ROLES[role][4])
                else:
                    await SEND(ch,SPECIAL_ROLES[role][3])
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
                    await SEND(ch,show_random_entry(lsplit[0]))
                    return
            elif lsplit[1] == "trivia":
                if lsplit[0] in TIPS_KEYS:
                    key = lsplit[0] + "T"
                    await SEND(ch,show_random_entry(key))
                    return

        #single word trigger
        for i, v in SINGLE_WORD_TRIGGERS.items():
            if v in lmsg:
                if "{mention}" in i:
                    i = i.format(mention=usr.mention)
                await SEND(ch,i)
                return
        
        #multiple word trigger
        for i, v in MULTIPLE_WORD_TRIGGERS.items():
            if all(word in lmsg for word in v):
                if "{mention}" in i:
                    i = i.format(mention=usr.mention)
                await SEND(ch,i)
                return
       
        #mixed word trigger
        for i, v in MIXED_WORD_TRIGGERS.items():
            if v[0] in lmsg:
                if any(word in lmsg for word in v[1]):
                    await SEND(ch,i)
                    return
      

               
    ## admin command
    else:

        #check for admin
        if not ADMIN in usr.roles:
            await SEND(ch,"You are not allowed to use this command.")
            return

        #deterimine the key (this is an alignment name in most cases)
        split = msg.lower().split(" ", 2)
        msgback = msg.split(" ", 2)[2]

        #have the bot say whatever you say
        if msg.startswith("makesay", 1):
            await SEND(CHANNELS[split[1]], msgback)
            return

        #create a new role with name and color
        if msg.startswith("nr", 1):
            try:
                await NEW_ROLE(split[1], split[2])
            except Exception as e:
                await SEND(ch, e)
                return

            await SEND(ch, "Worked.")
            return
    
        #give ckr
        if msg.startswith("ckr to ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split[2]:
                    await SEND(ch, "I gave the Chat Killer Role to " + split[2])
                    await asyncio.sleep(1)
                    await ADD_ROLES(mem,CKR)
                    break
            return  

        #remove ckr
        if msg.startswith("ckr from ", 1):
            for mem in SERVER.members:
               if mem.name.lower() + "#" + mem.discriminator == split[2]:
                    await SEND(ch, "I took the Chat Killer Role away from " + split[2])
                    await asyncio.sleep(1)
                    await REMOVE_ROLES(mem,CKR)
                    break
            return   

        #quiz
        if msg.startswith("quiz",1):
            if split[1] == "new":
                qSplit = split[2].split("|")
                if len(qSplit) != 7:
                    await SEND(ch,"Question does not have the required 7 sections.")
                else:
                    add_entry("quiz",split[2])
                    await SEND(ch,"Successfully added new quiz question")

            elif split[1] == "amount":
                await SEND(ch,"There are " + str(get_amount_of_entries("quiz")) + " questions in the database.")        

            elif split[1] == "print":
                question = show_specific_entry("quiz",int(split[2]))
                qSplit = question.split("|")
                toSend = "Q:\n" + qSplit[0] + "\nCorrect Answer:\n" + qSplit[1]
                toSend += "\nA2:\n" + qSplit[2] + "\nA3:\n" + qSplit[3] + "\nA4:\n" + qSplit[4]
                toSend += "\nGood response:\n" + qSplit[5] + "\nBad response:\n" + qSplit[6]
                await SEND(ch,toSend)

            elif split[1] == "delete":
                delete_entry("quiz",int(split[2]))
                await SEND(ch,"Question at index " + split[2] + " has been deleted." )

            return

        key = split[1]
        if not key in TIPS_KEYS:
            await SEND(ch,"Invalid alignment.")
            return
           
        #tip or trivia?
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
            add_entry(key,split[2])
            await SEND(ch,"New " + split[1] + " " + tot + " added.")
            return

        #list tips
        if msg.startswith("l",1):
            await SEND(ch,split[1] + " " + tot + "(s):")
            await PRINT_ENTRIES(ch, key)
            return
            
        #delete tipp
        if msg.startswith("d",1):
            delete_entry(key,int(split[2]))
            await SEND(ch,split[1] + " " + tot + "(s):")
            await PRINT_ENTRIES(ch, key)
            return
               
### RUN THE BOT ###
client.run(os.environ['TOKEN'])
