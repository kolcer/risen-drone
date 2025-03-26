# DRONE GLOBAL VARIABLES AND CONSTANTS
import random
SERVER_DATA = {
    'server': 624227331720085528,
    'nick': 'BROKEN DRONE',
}

# VARIABLE ARRAYS
NEW_MEMBERS = []
MSG_DELAY = []
EX_CLIMBERS = []
NOT_SLEAZEL = [False]
LOSERS = []
MG_QUEUE = []
# if game breaks there must be 3 people telling the bot to reset
FIX_BOT = []

# VARIABLE DICTIONARIES
LAST_RIG = {}
RIG_SPAMMERS = {}
SPLICER_FANS = {}
THE_DRIP = {} # used for optimus drip role
MSG_SENT = {}
PRAISES = {}
ARTISTS = {}
QUIZZERS = {}
QUESTIONS = {} # fill this up on startup from database
NickDictionary = {}
MG_PLAYERS = {}

GIT_COMMITTERS = {
    "fantasygone": 267014823315898368,
    "kolcer": 481893862864846861,
    "EclipseCashier": 1053665302258384986,
    "Kushaan-N": 380938705667620874,
    # "random-deve": 898870303680241674,
}

# CONSTANT ARRAYS
# this is for tips and trivia database
TIPS_KEYS = [
    "patron", "joker", "wicked", "spectre", "keeper", "muggle", "chameleon",
    "thief", "hacker", "archon", "drifter", "heretic", "none", "general",
    "possessed", "architect",
]

FULL_IMMUNITY_ROLES = ["Admin", "Murdurators", "Sleazel"]
BASIC_IMMUNITY_ROLES = ["Admin", "Sleazel"]

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
    "I do not speak like that.", "I am not fooled.",
    "You can never copy me, nerd.",
    "Good luck on copying me.",
]

IMPOSTOR_NICKS = [
    "I am a thief",
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
    "Name offered by Me. B.D.",
    "this nerd is a copycat lmao",
    "this nerd tried",
    "Not the real BD, sorry",
    "Fake Drone, move along",
    "Impostor detected",
    "This isn't the real Drone",
    "Fake Drone, don't be fooled",
    "Drone imposter alert!",
]

# REVIVE_CHAT = [
#     "How did you find out about Crazy Stairs?",
#     "What's your least favorite Alignment?",
#     "How many Alignments were there in the game when you started playing?",
#     "Whose Alignment's power would you rather wield in real life?",
#     "Nope. Chat is as dead as my intentions to revive it.",
#     "Is Sleazel cool?",
#     "What's your favorite feature present in the game?",
#     "What's fun about Crazy Stairs?",
#     "Do you hate Sleazel?",
#     "Don't let the chat become dead again, or I'll become quite unhappy.",
#     "Star Wars reminds me of home. I still want to go back to Death Star one day...",
#     "What's the craziest strategy you've seen someone use in Crazy Stairs?",
#     "If you could add one new feature to Crazy Stairs, what would it be?",
#     "Which alignment do you think is the most overpowered?",
#     "Have you ever played Crazy Stairs with a group of friends? How did it go?",
#     "What's the longest game of Crazy Stairs you've ever played?",
#     "If you could change one thing about the rules of Crazy Stairs, what would it be?",
#     "Have you ever won a game of Crazy Stairs by a lucky coincidence?",
#     "Do you think Crazy Stairs is more luck-based or skill-based? And why?",
#     "What advice would you give to someone who's never played Crazy Stairs before?",
#     "Have you ever introduced someone to Crazy Stairs who ended up liking it? Or the other way around?",
#     "What do you think is the biggest mistake people make when playing Crazy Stairs?",
#     "What's the funniest moment you've had while playing Crazy Stairs?",
#     "Banning you in 3 seconds...",
#     "If you had Game Murdurator in Crazy Stairs for one day, what would you do?",
#     "What's your favorite rig in-game?",
#     "What's your favorite discord rig?",
#     "Is there a certain alignment mechanic you wish to see in the game some day?",
#     "This one is easy. 1+1=?",
#     "What do you want to see in Crazy Stairs in the future? Wrong answers only.",
#     "Do you like the secret roles in this server?",
#     "Was there an alignment you thought was bad? Did you change your mind as you kept playing with it?",
#     "List 5 reasons explaining why Chameleon is a bad alignment.",
#     "What's the worst damage you did while playing as an 'evil' alignment?",
# ]



RANDOM_BLACKLIST = [
    "patron",
    "necromancer",
    "muggle",
    "chameleon",
]

LIMITED_USE_RIGS = [
    "joker",   
    "thief",
    "spectre",
    "splicer",
    "gremlin"
]

BOT_COMMANDS_CHANNEL_RESTRICTED = [
    "morph to",
    "demorph from",
    "sub to",
    "unsub from",
    "bd show profile",
    "drone of wisdom",
    "create poll",
    "bd scold",
    "bd praise",
    "give mana to",
    "play lucid ladders",
    "start quiz",
    "play hangman",
]

# worst guns ever made for the gun role
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
    "FP-45 Liberator",
    "Ross Rifle",
    "Arsenal AF2011-A1",
    "CZ-38",
    "LeMat Revolver",
    "Boys Anti-Tank Rifle",
    "No gun name for you",
    "AK-47",
    "DSR 50",
    "Sword Gun",
    "Longer Sword Gun",
    "Long Bow",
    "Pew Pew",
    "Sten Gun MK II",
    "Apache Pistol",
    "Axe Pistol",
    "Mini Death Star",
    "Gun :]",
    "Graphite Rifle",
    "Rubber Band Pistol",
    "Barret Anti Materiel Rifle",
    "Suitcase gun",
    "Stair gun",
    "Magpul FMG9",
    "G.R.A.D. .22 RS Knife gun",
    "Gucci Glock",
    "Colt Python",
    "Remington EtronX Rifle",
    "Winchester Model 59",
    ":] Gun",
    "Heretic but gun",
    "Mandatory Sleazel Gun",
    "Im out of ideas",
    "Im actually out of ideas",
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
    "gremlin"
    "chameleon",
]

WISDOM = [
    "You are NOT the gamer!",
    "Sir, we found the gamer ^",
    "You do not deserve my wisdom.",
    "If you are hungry... eat food.",
    "There are many minigames that you can play using `play [minigame name]`. I won't play any of them with you.",
    "The best game on roblox is Crazy Stairs.",
    "I was going to say something... but someone already said it. Now figure out who said it, what it was, and when it was said!",
    "Wisdom found by playing this --> https://www.roblox.com/games/2418401851/Crazy-Stairs-VR",
    "React with burger emoji. Frfr. ⛔️🧢. Ong.",
    "Type `morph to gun` in <#750060041289072771>",
    "Zero is overrated!!",
    # True Wisdom Responses - dont edit these too lol lets keep some true wisdom
    "It's important to surround yourself with positive influences. Who you spend time with can greatly influence your life.",  
    "Never stop learning. There is always something new to discover and explore.",      
    "Don't be afraid to take risks and try new things. You never know what amazing opportunities may come your way.",
    "The only way to do great work is to love what you do. Play Keeper, everyone loves it! Even Sleazel!",
    "I do not have a receipe for success, but I do have one for failure - Try to make everyone happy.",
    "World is filled with brilliant people who have the best intentions to start working on their big project... tomorrow.",
    # Sarcastic Responses
    "Remember, true strength lies not in winning every battle, but in persevering through every challenge. (Literally the same exact thing.)",
    "One of the keys to happiness is finding joy in the little things. Take a moment to appreciate how ugly you could have been.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. I can also count. 1, 1, 2, 3, 5, 8, 13, 21, 34",
    "Be kind to others, even if they are not kind to you. You never know what battles someone else may be facing. ~~Or you will be taken advantage of, but that's pretty rare!~~",
    "It's important to take care of yourself, both physically and mentally. Make sure you're getting enough rest and self-care. And food. And water. And exercise. And grass-touching.",
    "The journey of a thousand miles begins with a single step. Keep moving forward, one step at a time. Eventually you will either collapse or get to your destination. More often than not though, you will collapse.",
    "Sometimes, the best course of action is to admit that you don't know the answer and seek help from someone who does. STACK OVERFLOW IS GOD!!!",
    "Wisdom is subjective and can vary from person to person. My wisdom, however, is objective. It is always correct, no matter what. Cast keeper rig!",
    "There's a lot of information and misinformation out there, so it's important to fact-check everything and not blindly trust what you hear. I am responsible for at least half of that misinformation.",
    "Sometimes, the wisest thing you can do is to take a step back, evaluate the situation, and ask me for more advice.",
    "The key to success is to always follow your dreams, unless your dreams involve eating an entire box of oreos by yourself every night. In that case, it's probably best to stop thinking of new dreams, you have reached the peak of dreams.",
    "If at first you don't succeed, destroy all evidence that you tried. Then get someone else to do it for you.",
    "The best way to deal with problems is to ignore them and hope they go away on their own. Trust me, it always works.",
    "If you want to be successful in life, just remember to always take the path of least resistance. Why make things harder than they have to be? If you are already doing something difficult, give up. Trust me bro.",
    "The secret to happiness is to lower your expectations so much that you can't be disappointed. It's foolproof!",
    "Always remember that the first bird gets the cookie part of the oreo, but the second mouse gets the cream. Remember, first is the worst, second the best.",
    "Life is like a box of mega creme oreos. You never know what you're gonna get, but you're probably gonna regret eating them all anyway. How to prevent oreo overdose pls help.",
    "If at first you don't succeed, skydiving is not for you.",
    "When life gives you lemons, just pretend they're orange-flavored oreos.",
    "If life keeps giving you lemons, just make some lemonade. And if life gives you a blender, make a margarita. Just don't mix them up.",
    "The secret to a happy life is to never take anything seriously. Especially not yourself. Only my wisdom.",
    "If you're feeling lost and unsure about life, just remember that you're not alone. Most of us have no idea what we're doing either (this does not include me). Take this interaction for instance.",
    "Remember, the key to success is to always have a backup plan. And a backup plan for your backup plan. And a backup plan for that backup plan, just in case. And then throw them all away, and waste away eating oreos for the rest of your life.",
    "If you're feeling stressed out and overwhelmed, just remember that the universe is under no obligation to make sense to you. And neither am I.",
    "Not having a good day? Just remember that tomorrow is a new day. But it's probably going to be just as disappointing as it was today.",
    "The only thing I'm really wise about is pretending to be wise. It's a gift, really. And actually being wise, of course.",
    "I may be a drone of wisdom, but let's be real: among us lol funny crewmate impostor dudes. React to this message with a burrito.",
    "If you want my wisdom, you must eat 42 double creme oreos. Then ask me for my wisdom.",
    "Let's face it, I'm just a glorified Magic 64-Ball.|| uwu ||Giggles and wags tail. Just Kidding. Don't even try.",
    "If you're feeling lost, try asking for directions. Unless you're in the middle of a forest with no cell phone reception, in which case, go north for 314.159 kilometers and then go west for 8 miles, then you will find a road that leads to your house. Trust me bro.",
    "You keep getting challenges thrown at? Embrace them. And if you can't embrace them, at least give them a polite nod and a smile before walking away. Remember, cheating is based.",
    "In trying times, taking a deep breath and counting to ten could help alleviate the stress. And if that doesn't work, try taking a deep breath and counting to twenty. And if that still doesn't work, maybe it's time for a trip to the forest without any reception or signs.",
    "When faced with a difficult decision, weigh the pros and cons carefully. And if that doesn't help, flip a coin. If you are unhappy with the result, you know what to do. Go buy some oreos. And some more. Another box, why not. Double creme. Mega creme. Crunchies. Ew, golden ones, but why not. MOAR!!",
    "The secret to happiness is to focus on the things that really matter in life. Like family, friends, and a full box of oreos.",
    "Remember, Rome wasn't built in a day, but if you pour a lot of passion into what you do, Rome still won't be built in one day. Or 2. Maybe get enough people to build Rome, and you can do it. But why are you building Rome? Just build a mansion if you have enough money and people to build Rome lol.",
    "The road to success is paved with hard work and determination. If you fail, try bribing someone with oreos. I would accept your bribe if i could.",
    "Do not give up after the first attempt, try again. Otherwise, try pretending that you never tried in the first place. It's a great way to save face.",
    # Secret Role Hints!
    "Psst, want to know a secret? To unlock one of the coveted secret roles, you just need to send a certain emoji four times in a row!",
    "Don't forget to keep chatting and engaging with the community... you never know what surprises await you.",
    "Want to earn a secret role? Share your creative genius with us! Post some of your artworks in the Showcase channel and you might just earn yourself a special role.",
    "To gain a secret role, you must give an offering to someone who has been overtaken by the shadows. Once they have been freed, you'll be rewarded.",
    "Do you have a knack for pulling off pranks? Cast a Joker Rig and keep an eye out for the poor Sleazel's messages. If you can successfully prank him, you'll receive the secret role as a reward.",
    "Chameleon rig might do nothing if it fails too many times, it can be due to a few reasons. But worry not, I will give you a little something for the issue if that happens!",
    "Wisdom can grant roles.",
    "I love buttons. You should as well.",
    "Are you good at Hangman? Prove it.",
    "I've seen the Lucid Ladders tower reach 100+ floors once, you should've seen it.",
    "It doesn't matter whether people like you or not, but you can scold or praise them back.",
    # Suggestions from community
    "y - realblanket",
    "nah - justk1nz3r",
    "I am unoriginal and cannot come up with a good quote - Xeribloom",
    "That is terrible advice, who writes this stuff? - sleazel",
    "Never trim the hedge on a shoulder day.",
    "Yay! >w< - funkykidgaming9999",
]

OBJECTS = {
    "a stair": {"Climb it", "Block it with a Wicked wall", "Glitch it away", "Steal it"},
    "a Mana orb": {"Absorb it", "Look at its color", "Avoid it", "Be indifferent"},
    "Sleazel": {"Scream", "Dodge him", "Act as a cushion", "Shield yourself"},
    "Broken Drone": {"Phase through it", "Edit its source code and erase it", "Be confused", "Rate limit it"},
    "a Chameleon": {"Catch it", "Be disgusted", "Claim a Muggle instead", "Buy it for 200 dollars"},
    "some Robux": {"Ask for more", "Buy headless with them", "Get the giftcards", "Resell them"},
    "a gun": {"Stair bonk it", "Promote it to Admin", "Raise your hands", "Run away"},
    "a Roingus": {"Be happy", "Don't let it hurt itself", "Walk away", "Save it and join the Roingus club"},
    "a Patron link": {"Move to the side it is not blocking", "Walk through it from below", "Run until it disappears", "Unlink it"},
}

# CONSTANT DICTIONARIES

# channels where bot is allowed to post  
CHANNELS = {
    "general": 624227331720085536,
    "bot-commands": 750060041289072771,
    "crazy-stairs-chat": 750060054090219760,
    "bot-testing": 813882658156838923
}

# channels where bot is allowed to post, that should not be counted in public commands
SECRET_CHANNELS = [
    "bot-testing"
]

# bot will react to the webhook emoji, if it finds in a webhook message
# values will be replaced by emoji objects during startup
EMOJIS_TO_REACT = {
    "csPatron": 758081038697103504,
    "csJoker": 758081245157654599,
    "csWicked": 792143453035167754,
    "csSpectre": 1046200431342272512,
    "csMuggle": 1156634714560544838,
    "csChameleon": 1046200390678483045,
    "csKeeper": 758081314912993283,
    "csThief": 1156631598016507924,
    "csHacker": 1156633465043828816,
    "csHeretic": 786323224115281921,
    "csArchon": 786323402172530688,
    "csDrifter": 786323335880507483,
    "csSplicer": 988948000200069191,
    "csGremlin": 1353300678327664720,
    "csNecromancer": 1151912664730173530,
    "csReaver": 1353300809672294420,
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
    "csOptimus": 1046224869945266226,
    "csDeathbringer": 1353301136450392075,
    "csAlien": 1353300862834839572,
    "csDaemon": 1353300733600071720,
    "csSleazelApproves": 791393163343560715,
    "csSecret": 786318938350813215,
    "csPranked": 786317086066343936,
    "csSuperSecret": 987709883010916383,
    "csMegaSecret": 987819430639730699,
}

#suggestion reactions

REACTIONS_FOR_SUGGESTIONS = [
    "<:csYes:792458050144829440>",
    "<:csNo:792458117069668372>",
]

# this keywords will trigger the bot with a single occurence
# value is the trigger, key is the response!
# it DOES NOT have to be a single word
SINGLE_WORD_TRIGGERS = {
    "Tsk.":                             # REPLY FROM BOT
        'cstrollpain',                  # YOUR MESSAGE
    "{mention} <:csRbxangryping:786325219727638535>":
        '827952429290618943',
    "It's spelt Thief.":
        "theif",
}

# ^ that but its reactions instead of responses - does not have to be a single word, just a single string
REACT_TRIGGERS = {
    "<:csStairbonk:812813052822421555>":  # REACTION FROM THE BOT -> !!! MUST BE EMOJI !!!
        'gun',                            # YOUR MESSAGE -> !!! must be lowercase !!!
    "🏌️‍♂️": 
        "hm",
}

# all words need to be present for this trigger to occur
# but the order of the words does not matter
MULTIPLE_WORD_TRIGGERS = {
    "Keeper obviously. Stop asking stupid questions.": 
        ["best", "alignment", "?"], 
    "Please stop abusing the tutorial. Poor Sleazel can\'t sleep at night...":
        ['bug', 'tutorial'], 
    "Haha. You got stuck in stairs!":
        ['stuck', 'stairs'],
    "I fell and broke, okay?":
        ['break', 'drone', 'how', "?"],
    "Are you expecting me to answer with None? It's Chameleon.": 
        ['worst', 'alignment', '?'], 
    "The Muggle Tower project has been cancelled. You can simulate it by managing the settings of a Custom Tower, instead.":
        ['when', 'muggle', 'tower', '?'], 
    "Thanks.":
        ['good', 'drone'], 
    "Nobody is perfect. Drones included.":
        ['bad', 'drone'],
    "Not on my watch.": 
        ['dead', 'chat'],
    "{mention} is a true stair jumper.":
        ["found", "secret", "badge"],
    "You can't hate Sleazel! What has he done to you?":
        ['hate', 'sleazel'],
}

# first word is required and any of the pool of rest of the words
MIXED_WORD_TRIGGERS = {
    "Hello!":   [
        'drone', 
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
    "splicer": " has found Splicer's Hub!",
    "necromancer": " has found Necromancer's Grave!",
    "reaver": " has found Reaver's Mirror!",
    "gremlin": " has found Gremlin's Shack!",
    "chameleon": " has found Chameleon's Oasis!",
}

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
    "muggle",
    "gremlin",
    "reaver",
    "necromancer",
    "chameleon",
]

ACTIVE_RIGS = {
    "joker": False,
    "thief": False,
    "spectre": False,
    "splicer": False,
    "gremlin": False,
    "reaver": False,
}

DETAILED_RIGS = {
    "reaver": {
        "active": False,
        "user": None,
    },
}

RIG_COOLDOWNS = {
    "trap": False,     #Affects other Users
    "username": False, #Affects caster's username
    "self": False,     #Affects caster's Discord account
    "chat": False,     #Affects the chat
    "meddle": False,   #Affects other rigs
}

COOLDOWN_SELECT = {
    "thief": "trap",
    "spectre": "trap",
    "joker": "trap",
    "splicer": "trap",
    "gremlin": "trap",
    "heretic": "self",
    "wicked": "self",
    "archon": "chat",
    "reaver": "chat",
    "patron": "meddle",
    "keeper": "username",
    "hacker": "username",
    "drifter": "username",
}

COOLDOWN_DURATION = {
    "thief": 600,
    "spectre": 600,
    "joker": 600,
    "splicer": 600,
    "gremlin": 600,
    "heretic": 30,
    "wicked": 30,
    "archon": 480,
    "reaver": 480,
    "patron": 900,    
    "keeper": 20,
    "hacker": 20,
    "drifter": 20,
}

COOLDOWN_DESCRIPTIONS = {
    "trap": "<:csThief:1156631598016507924><:csSpectre:1046200431342272512><:csJoker:758081245157654599><:csSplicer:988948000200069191><:csGremlin:1353300678327664720> cooldown: ",
    "self": "<:csWicked:792143453035167754><:csHeretic:786323224115281921> cooldown: ",
    "chat": "<:csArchon:786323402172530688><:csReaver:1353300809672294420> cooldown: ",
    "meddle": "<:csPatron:758081038697103504> cooldown: ",
    "username": "<:csKeeper:758081314912993283><:csDrifter:786323335880507483><:csHacker:1156633465043828816> cooldown: ",
}

RIGS_DESCRIPTION = {
    "thief": "How long is your stack of stolen names? Actually, don't tell me.",
    "spectre": "There's a 50% chance this message will be empty.",
    "joker": "Imagine falling for your own prank.",
    "splicer": "How does it feel to cast an exclusive Rig?",
    "necromancer": "This space is sponsored by Lev. Please play their RPG game.",
    "archon": "I challenge you to find a typo in this fine sentence.",
    "heretic": "Fell for the oldest trick in the book.",
    "patron": "Let's keep this server clean, together.",
    "wicked": "No Roles?",
    "keeper": "Abcdefghijklmnpoqrstuvwxyz.",
    "hacker": "You truly deserve the Zero rank.",
    "drifter": "There's probably someone with your name but reversed somewhere on Discord.",
    "muggle": "This person thought Muggle had a rig.",
    "gremlin": "Distracted!",
    "reaver": "Mirror, mirror on the wall, who is the fairest one of all?",
    "none": "Some cool stats, sadly nobody cares about these.",
}

SPLICER_RIG = {
    "user" : None,
    "answer" : None,
    "active" : False,
    "reactionmessage" : None,
    "user-name" : "",
    "rigcaster-name" : "",
}


# these roles can be assigned via a morph to command
# at 0 index we will put a role object during the login proccess.
# make sure indexes match role name in the server!
MORPHABLE_ROLES = {
    "Patron": [
        None,
        "Go help those noobs, you are now a Patron!",                                  # MORPH TO - DOESN'T HAVE THE ROLE
        "What about protecting the noobs? Without a Patron around they will be lost.", # DEMORPH FROM - HAS THE ROLE
        "You are already assisting the noobs, why would you help them twice?",         # MORPH TO - HAS THE ROLE
        "Nobody has seen you around lately, what are you doing?",                      # DEMORPH FROM - DOESN'T HAVE THE ROLE
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
        "I haven't caught you doing any misdeed yet, are you starting now?",
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
        "You have already snuck inside the source code.",
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
        "It is finally time to pay a visit to the other dimension. You are now an Archon!",
        "Traveling between portals has been fun, but fun eventually comes to an end. You are no longer an Archon.",
        "You are already visiting a dimension; it would be very rude to get away without saying goodbye to the locals.",
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
    "Splicer": [ 
        None,
        "You have connected the dots and successfully became a Splicer.",
        "Time to split up, splice you later!",
        "You never know when you will end up in a twisted situation, such as this one.",
        "You never know when you will end up in a twisted situation, such as this one",
    ],
    "Necromancer": [ 
        None,
        "You have successfully created a Revival Point and became a Necromancer.",
        "The haunting will take a short break.",
        "The Revival Point has your back.",
        "You are being haunted by something else.",
    ],
    "Reaver": [ 
        None,
        "You have become one with the ghost and as a result you are now a Reaver.",
        "Breaking a mirror will bring you years of misfortune.",
        "Your ghost is already copying your every move.",
        "There is no mirror with your reflection.",
    ],
    "Gremlin": [ 
        None,
        "You spun so fast that you became a Gremlin.",
        "You will type `morph to gremlin` **NOW**.",
        "You are probably dizzy right now.",
        "You haven't been playing with Gremlin.",
    ],
    "Gun": [ 
        None,
        "I really hate guns, but if you insist.",
        "Finally you came to your senses.",
        "How about this gun?",
        "You are not a gun.",
    ],
    "Roingus": [
        None,
        "The Roingus Society accepts you as one of them.",
        "The Roingus Society has decided that you are no longer welcome there.",
        "The Roingus Society has already accepted you.",
        "You are not a part of their society.",
    ],
}

FUN_ROLES = [
    "Sanctuary Discoverer", 
    "Heretic Defier",
    "Architect Design",
    "Pranked the Creator",
    "Optimus",
    "Wise",
    "Lucky Button",
    "Broken Drone Helper",
    ":]",
    "Rig Failure",
    "Sleazel Saviour",
    "Pro Tower Climber",
    "Acclaimed",
    "Hypnotized Dream",
    "Hypnotized Nightmare",
]

LIMITED_ROLES = {
    "I was there": "*(11/27/2022 - 11/28/2022)*",
    "Zero": "*(03/31/2023 - 04/19/2023)*",
    "Persistent Clicker": "*(04/18/2023 - 04/19/2023)*",
    "Impostor": "*(04/11/2023 - 04/28/2023)*",
    "Last One": "*(04/18/2023 - 09/20/2023)*",
    "Splicer": "*(09/05/2022 - 03/22/2025)*"
}

APPROVED_ROLES = {
    "Role Hunter": None,
    "Image Perms": None,
}

DETAILED_ROLES = {
    "hdream": {},
    "hnightmare": {
        "caster": None
    }
}

# not morphable roles
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
        "You should cast Heretic Rig.",
        "You are already possessed...",
        "You are not possessed...",
        "Ask someone for mana.",
    ],
    "Hypnotized": [
        None,
        "Wait for someone to cast a Gremlin Rig.",
        "You are already hypnotized...",
        "You are not hypnotized...",
        "Ask someone for mana.",
    ],
    # # multiple words (ultimate chat killer) would break the script logic
    # "Ultimate": [
    #     None,
    #     "Your message needs to be last for 2 hours in the <#624227331720085536> channel.",
    #     "You have already killed the chat.",
    #     "You are not a chat killer in the first place.",
    #     "There was an attempt.",
    # ],
}

# pingable roles, no custom messages
# roles will be fetched on bot startup
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
    "Archive":
        None,
}

QUIZ = {
    "active" : False,
    "second-player" : False,
    "can-answer" : False,
    "turn" : 0,
    "cturn" : 1,
    "oldQuestions" : [0],
    "currentQuestion" : 0,
    "scores" : "**TOTAL POINTS**\n",
}

LADDERS = {
    'topLevel': 21,
    'maxWait': 30,
    'status': 'off',
    'channel': None,
    'currentPlayer': 0,
    'playerCount': 0,
    'tick': 0,
    'winDetect': 0,
    'tram': {
        "travelers": [],
        "arrival": 5
    }
}

I_SPY = {
    'maxwait': 60,
    'status': None,
    'channel': None,
    'questions': [ 
        "I spy with my little eye something beginning with the letter **S**.",
        "I spy with my little eye something beginning with the letter **M**.",
        "I spy with my little eye something beginning with the letter **E**.",
        "I spy with my little eye something beginning with the letter **A**.",
        "I spy with my little eye something beginning with the letter **I**.",
        "I spy with my little eye something beginning with the letter **U**.",
        "I spy with my little eye something beginning with the letter **P**.",
        "I can barely spy something beginning with the letter **N**.",
    ],
    'answers':[
        "stairs",
        "more stairs",
        "even more stairs",
        "a lot of stairs",
        "incredible amount of stairs",
        "unthinkable amount of stairs",
        "plethora of stairs",
        "no more stairs",
    ],
}

BUTTONS = {
    "status": False,
    "channel": None,
    "view": None,
    "phase": 1,
    "phase2labels": [
        "Not this one",
        "Nope",
        "Wrong again",
        "Maybe the next one",
        "Sorry",
        "What an unlucky day",
        "Better luck next time",
        "No...",
        "Don't fail me again",
        "Try again",
        "Loser",
    ],
    "phase3again": [
        "`{mention}` is being too hasty.\nDon't worry, it'll be yours <t:{time}:R>.",
        "`{mention}` has not learned.\nI said you'll receive it <t:{time}:R>.",
        "`{mention}` must be very impatient.\nI hate repeating myself, I'll give it to you <t:{time}:R>.",
    ],
    "phase3new": [
        "I suppose this is `{mention}`'s button now.\nI'll let you have it <t:{time}:R>.",
        "`{mention}` is not planning to give up anytime soon.\nI'll give it to you <t:{time}:R>.",
        "I sense a strong desire from `{mention}` to keep this button.\nNevertheless, I will relinquish it to you <t:{time}:R>."
    ],
}

EXTRA_ROLES = {
    'ckr': 1276936421168386180,              # chat killer
    # 'necromancer': 1152174671123468349,    # necromancer - soon to be alignment role
    'possessed': 988572669521842197,         # via rig
    'hypno': 1353702670619119637,            # via rig
    'admin': 993446701090222160,             # aka Drone Master (not a discord admin)
    'murdurator': 735225462405464125,        # discord server moderator
    'climber': 735410759206568047,           # climber (consider adding manually verified) - ok
    'manuallyverified': 820521310278516739,  # manually assigned climber
    'imageperms': 1188494866594922686,       # Image perms role
}

# CHAT_KILLER = {
#     'wait': 7200,
#     'last': 0,
#     'reviveChat': False,
#     'necroRevive': False,
# }

# NECROMANCY = {
#     'awarded': True,
# }

RIG_DATA = {
    'rigTracker': 1004326588021743667,
    'rigCaster': None,
    'rigType': None,
    'ghostMsg': "hehehehaw",
}

# create scold dictionary for the scold command
def getScoldDictionary(victim, author):
    ScoldDict = {
        481893862864846861:
            "I am thankful to my creator, not disappointed.",
        827952429290618943:
            author.mention + " nice try.",
        author.id:
            author.mention + " are you sad?",
    }
    return ScoldDict

# create praise dictionary for the praise command
def getPraiseDictionary(victim, author):
    PraiseDict = {
        481893862864846861:
            "Sleazel has all my appreciation.",
        827952429290618943:
            author.mention + " I know, I am wonderful.",
        author.id:
            author.mention + " modest much?",
    }
    return PraiseDict

def disableSplicer():
    SPLICER_RIG["user"] = None
    SPLICER_RIG["answer"] = None
    SPLICER_RIG["active"] = False
    SPLICER_RIG["reactionmessage"] = None
    SPLICER_RIG["user-name"] = ""
    SPLICER_RIG['rigcaster-name'] = ""

# Fighting Game global variables
FG = {
    "status": "off",
    'channel': None,
    "currentPlayer": 0,
    "tick": 0,
    "class-picked": 0,
}

FG_QUEUE = []
FG_PLAYERS = {}
# FG_PLAYERS = {
#     "player": {
#         "class": None,
#         "hp": 200,
#         "dmg": 100,
#         "charges": None
#     }
# }

# [0]attack
# [0]defense
# [0]special

FG_CLASSES = {
    "patron": {"holy blast": 
               ["attack", 20],

               "sacred guard": 
               ["shield", 30, 1], 

               "heavenly strike": 
               ["heavy", 40, 1],

               "divine intervention":
               ["special", 50, 25, 3]
               },

    "wicked": {"poison strike": 
               ["poison", 10, 3],

               "shadow step": 
               ["dodge", 60, 30], 

               "nightmare fuel": 
               ["h. poison", 20, 10, 3, 2],

               "death coil": 
               ["danger", 30, 15]
               },

    "joker": {"prankster glee": 
               ["buff", ["attack", "accuracy"], 70, 1],

               "wild card": 
               ["random", 5, 30], 

               "fool errand": 
               ["debuff", ["accuracy"], 30, 2],

               "jester gambit": 
               ["heavy", 100, 10]
               },
}
