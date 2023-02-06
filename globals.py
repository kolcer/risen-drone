#DRONE GLOBAL VARIABLES AND CONSTANTS

SERVER_DATA = {
    'server': 624227331720085528,
    'nick': 'BROKEN DRONE',
}

#VARIABLE ARRAYS
LOSERS = []
MG_QUEUE = []
#if game breaks there must be 3 people telling the bot to reset
FIX_BOT = []

#VARIABLE DICTIONARIES
LAST_RIG = {}
RIG_SPAMMERS = {}
SPLICER_FANS = {}
MSG_SENT = {}
ARTISTS = {}
QUIZZERS = {}
QUESTIONS = {} #fill this up on startup from database
NickDictionary = {}
MG_PLAYERS = {}

#CONSTANT ARRAYS
#this is for tips and trivia database
TIPS_KEYS = [
    "patron", "joker", "wicked", "spectre", "keeper", "muggle", "chameleon",
    "thief", "hacker", "archon", "drifter", "heretic", "none", "general",
    "possessed", "architect",
]

IMMUNITY_ROLES = ["Admin", "Murdurators", "Sleazel"]

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

REVIVE_CHAT = [
    "How did you find out about Crazy Stairs?",
    "What's your least favorite Alignment?",
    "How many alignments were there in the game when you started playing?",
    "Whose alignment's power would you rather wield in real life?",
    "Nope. Chat is as dead as my intentions to revive it.",
    "Is Sleazel cool?",
    "What's your favorite feature present in the game?"
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
    "splicer",
]

LIMITED_USE_RIGS = [
    "joker",   
    "thief",
    "spectre",
    "splicer",
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

#CONSTANT DICTIONARIES

#channels where bot is allowed to post  
CHANNELS = {
    "general": 624227331720085536,
    "bot-commands": 750060041289072771,
    "crazy-stairs": 750060054090219760,  
    "bot-testing": 813882658156838923,
}

#bot will react to the webhook emoji, if it finds in a webhook message
#values will be replaced by emoji objects during startup
EMOJIS_TO_REACT = {
    "csPatron": 758081038697103504,
    "csJoker": 758081245157654599,
    "csWicked": 792143453035167754,
    "csSpectre": 1046200431342272512,
    "csMuggle": 758081353932603414,
    "csChameleon": 1046200390678483045,
    "csKeeper": 758081314912993283,
    "csThief": 758081386203840644,
    "csHacker": 758081540063494288,
    "csHeretic": 786323224115281921,
    "csArchon": 786323402172530688,
    "csDrifter": 786323335880507483,
    "csSaviour": 1046199993188483163,
    "csIt": 1046199856793923635,
    "csAnnihilator": 1046199281633206303,
    "csAdmiral": 1043554481759072427,
    "csDabsforlif": 1046199648299266068,
    "csZero": 1046200149413728440,
    "csOutlaw": 1046199909017194576,
    "csExiled": 1046199709036970075,
    "csIlluminati": 1046199796928610386,
    "csStrider": 1046200097723125852,
    "csAether": 1046200040772874363,
    "csUsurper": 1046199582805217341,
    "csSleazelApproves": 791393163343560715,
    "csSecret": 786318938350813215,
    "csPranked": 786317086066343936,
    "csSuperSecret": 987709883010916383,
    "csMegaSecret": 987819430639730699,
}

#this keywords will trigger the bot with a single occurence
# value is the trigger, key is the response!
#it DOES NOT have to be a single word
SINGLE_WORD_TRIGGERS = {
    "<:cs_Stairbonk:812813052822421555>": #MESSAGE SENT
        'gun',                            #REPLY
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
        ["best", "alignment", "?"], 
    "Please stop abusing the tutorial. Poor Sleazel can\'t sleep at night...":
        ['bug', 'tutorial'], 
    "Haha. You got stuck in stairs!":
        ['stuck', 'stairs'],
    "I fell and broke, okay?":
        ['broken', 'drone', 'how', "?"],
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
    "Hm.":
        ["Hm"],
    "You can't hate Sleazel! What has he done to you?":
        ['hate', 'sleazel'],
    "Well, you probably suck too."
        ['sucks', 'sleazel'],
}

#first word is required and any of the pool of rest of the words
MIXED_WORD_TRIGGERS = {
    "Hello!":   [
        'broken drone', 
        ["hi", "hello", "howdy", "sup"],
    ],
    "Wrong.": [
        'drone',
        ["dead", "down", "off", "vacation", "sleep"],
    ],    
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

COOLDOWN_SELECT = {
    "thief": "tsj",
    "spectre": "tsj",
    "joker": "tsj",
    "splicer": "tsj",
    "archon": "ha",
    "heretic": "ha",
    "patron": "patron",
    "wicked": "general",
    "keeper": "general",
    "hacker": "general",
    "drifter": "general",
}

COOLDOWN_DURATION = {
    "patron": 900,    
    "thief": 600,
    "spectre": 600,
    "joker": 600,
    "splicer": 600,
    "archon": 240,    
    "heretic": 60,
    "wicked": 60,    
    "keeper": 20,
    "hacker": 20,
    "drifter": 20,
}

SPLICER_RIG = {
    "user" : None,
    "answer" : None,
    "active" : False,
    "reactionmessage" : None,
    "user-name" : "",
    "rigcaster-name" : "",
}

ACTIVE_RIGS = {
    "joker": False,
    "thief": False,
    "spectre": False,
    "splicer": False,
}

RIG_COOLDOWNS = {
    "general": False,
    "tsj": False,
    "ha": False,
    "patron": False,
}

COOLDOWN_DESCRIPTIONS = {
    "general": "<:csWicked:792143453035167754><:csKeeper:758081314912993283><:csDrifter:786323335880507483><:csHacker:758081540063494288> cooldown: ",
    "tsj": "<:csThief:758081386203840644><:csSpectre:1046200431342272512><:csJoker:758081245157654599><:csSplicer:988948000200069191> cooldown: ", #
    "ha": "<:csHeretic:786323224115281921><:csArchon:786323402172530688> cooldown: ",
    "patron": "<:csPatron:758081038697103504> cooldown: ",
}

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
    "Sleazel-in-game":
        None,
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

LADDERS = {
    'topLevel': 21,
    'maxWait': 30,
    'status': 'off',
    'channel': None,
    'currentPlayer': 0,
    'tick': 0,
    'winDetect': 0,
}

I_SPY = {
    'maxwait': 60,
    'status': None,
    'channel': None,
    'questions': [ 
        "I spy with my little eye something beginning with the letter **S**.",
        "I spy with my little eye something beginning with the letter **M**.",
        "I spy with my little eye something beginning with the letter **E**.",
    ],
    'answers':[
        "stairs",
        "more stairs",
        "even more stairs",
    ],
}

EXTRA_ROLES = {
    'ckr': 951424560685805588,            #chat killer
    'possessed': 988572669521842197,      #via rig
    'admin': 993446701090222160,          #aka Drone Master (not a discord admin)
    'murdurator': 735225462405464125,     #discord server moderator
    'climber': 735410759206568047,        #climber (consider adding manually verified)
}

CHAT_KILLER = {
    'wait': 7200,
    #'thirdKill': None,
    'last': 0,
    'reviveChat': False,
}

RIG_DATA = {
    'rigTracker': 1004326588021743667,
    'rigCaster': None,
    'ghostMsg': "",
}

#create scold dictionary for the scold command
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
