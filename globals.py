# DRONE GLOBAL VARIABLES AND CONSTANTS
import random
SERVER_DATA = {
    'server': 624227331720085528,
    'nick': 'BROKEN DRONE',
}

# VARIABLE ARRAYS
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
ARTISTS = {}
QUIZZERS = {}
QUESTIONS = {} # fill this up on startup from database
NickDictionary = {}
MG_PLAYERS = {}

GIT_COMMITTERS = {
    "Nicksmth": 267014823315898368,
    "kolcer": 481893862864846861,
    "random-deve": 898870303680241674,
    "EclipseCashier": 695526697059090483,
}

# CONSTANT ARRAYS
# this is for tips and trivia database
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

REVIVE_CHAT = [
    "How did you find out about Crazy Stairs?",
    "What's your least favorite Alignment?",
    "How many Alignments were there in the game when you started playing?",
    "Whose Alignment's power would you rather wield in real life?",
    "Nope. Chat is as dead as my intentions to revive it.",
    "Is Sleazel cool?",
    "What's your favorite feature present in the game?",
    "What's fun about Crazy Stairs?",
    "Do you hate Sleazel?",
    "Don't let the chat become dead again, or I'll become quite unhappy.",
    "Star Wars reminds me of home. I still want to go back to Death Star one day...",
    "What's the craziest strategy you've seen someone use in Crazy Stairs?",
    "If you could add one new feature to Crazy Stairs, what would it be?",
    "Which alignment do you think is the most overpowered?",
    "Have you ever played Crazy Stairs with a group of friends? How did it go?",
    "What's the longest game of Crazy Stairs you've ever played?",
    "If you could change one thing about the rules of Crazy Stairs, what would it be?",
    "Have you ever won a game of Crazy Stairs by a lucky coincidence?",
    "Do you think Crazy Stairs is more luck-based or skill-based? And why?",
    "What advice would you give to someone who's never played Crazy Stairs before?",
    "Have you ever introduced someone to Crazy Stairs who ended up liking it? Or the other way around?",
    "What do you think is the biggest mistake people make when playing Crazy Stairs?",
    "What's the funniest moment you've had while playing Crazy Stairs?",
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
    "gun",
]

LIMITED_USE_RIGS = [
    "joker",   
    "thief",
    "spectre",
    "splicer",
    "gun",
    "impostor",
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

WISDOM = [
    "You are NOT the gamer!",
    "Sir, we found the gamer ^",
    "You do not deserve my wisdom.",
    "If you are hungry... eat food.",
    "There are many minigames that you can play using `play [minigame name]`. I won't play any of them with you.",
    "The best game on roblox is Crazy Stairs.",
    "I was going to say something... but someone already said it. Now figure out who, what, and when it was said!",
    "Wisdom found by playing this --> https://www.roblox.com/games/2418401851/Crazy-Stairs-VR",
    "React with burger emoji. Frfr. ⛔️🧢. Ong.",
    "Type `morph to gun` in <#750060041289072771>",
    "Zero is overrated!!",
    # True Wisdom Responses - dont edit these too lol lets keep some true wisdom
    "It's important to surround yourself with positive influences. Who you spend time with can greatly influence your life.",  
    "Never stop learning. There is always something new to discover and explore.",      
    "Don't be afraid to take risks and try new things. You never know what amazing opportunities may come your way.",
    "The only way to do great work is to love what you do. Keep searching, you'll find your dream job soon!",
    "Every day is a gift. Unless it's your birthday, in which case, every day is a present.",
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
    "If you're looking to get a secret role, there's a little trick to it. You'll need to cast the Hacker Rig and if you happen to get all zeros, then boom - the secret role is yours. Good luck though. 1/256. I'm sorry jeff",
    "Don't forget to keep chatting and engaging with the community... you never know what surprises await you.",
    "Want to earn a secret role? Share your creative genius with us! Post some of your artworks in the Showcase channel and you might just earn yourself a special role.",
    "To gain a secret role, you must give an offering to someone who has been overtaken by the shadows. Once they have been freed, you'll be rewarded.",
    "Do you have a knack for pulling off pranks? Cast a Joker Rig and keep an eye out for the poor Sleazel's messages. If you can successfully prank them, you'll receive the secret role as a reward.",
    "Cheating is not necessarily bad...",
    "You know, Drone Masters can give the secret roles by typing |assign...",
    "Cheating is based.",
    "How many of those impostor tokens do you have? Try casting some big boy spells, maybe even a rig.",
    "Wisdom can grant roles.",
    # Suggestions from community
    "y - RealBlanket#7739",
    "nah - Amadán#9008",
    "Balls - Chugnus Amognus",
    "I am unoriginal and cannot come up with a good quote - Xeron#7149",
    "https://cdn.discordapp.com/attachments/750060041289072771/1094195127909634168/Screen_Shot_2023-04-08_at_11.40.40.png",
    "|assign 898870303680241674 I was there - frfr#0431",
    " *|| https://cdn.discordapp.com/attachments/750060041289072771/1095276098935324692/Screen_Shot_2023-04-11_at_11.15.57.png ||* ",
    "That is terrible advice, who writes this stuff? - sleazel#0820",
    "me - roibrari#2287",
    "one more commitment and its 1.1k commitments - cashier#6099",
]

# CONSTANT DICTIONARIES

# channels where bot is allowed to post  
CHANNELS = {
    "general": 624227331720085536,
    "bot-commands": 750060041289072771,
    "crazy-stairs": 750060054090219760,  
    "bot-testing": 813882658156838923,
    "debugs": 1094687051724627998,
    "testing": 1096887479031836793,
}

# bot will react to the webhook emoji, if it finds in a webhook message
# values will be replaced by emoji objects during startup
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

# this keywords will trigger the bot with a single occurence
# value is the trigger, key is the response!
# it DOES NOT have to be a single word
SINGLE_WORD_TRIGGERS = {
    "Tsk.":                             # REPLY FROM BOT
        'cstrollpain',                  # YOUR MESSAGE
    "{mention} <:csRbxangryping:786325219727638535>":
        '827952429290618943',
    "You're the one that has no balls.":
        'no balls',
    "The only skill issue you have is your capability to try to roast someone. Nice try.":
        'skill issue',
    "Oh I like you admitting to being a clown. Just like a Joker!":
        'bozo',
    "Oh no you don't. I know that you are bypassing, Nexieus.":
        'fuсk',
    "Cease.":
        'fu*c*k',
    "You can't bypass. You are a fool.":
        'f*u*ck',
    "No.":
        '*f*uck',
    "I am getting very pissed off. Stop.":
        'fuc*k*',
    "It's spelt Thief.":
        "theif",
    "🏌️‍♂️":
        "hm",
    "https://cdn.discordapp.com/emojis/734784926561337497.webp?size=48&name=CH_PepeScared&quality=lossless":
        "kill",
    "{mention} we need to cook":
        "waltuh",
}

# ^ that but its reactions instead of responses - does not have to be a single word, just a single string
REACT_TRIGGERS = {
    "<:csStairbonk:812813052822421555>":  # REACTION FROM THE BOT -> !!! MUST BE EMOJI !!!
        'gun',                            # YOUR MESSAGE -> !!! must be lowercase !!!
    "📮":
        "among",
    "👁":
        "food",
    "🍔":
        "react with burger",
    "🧢":
        "best",
    "🥰":
        "oreo",
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
    "You can't hate Sleazel! What has he done to you?":
        ['hate', 'sleazel'],
    "Sleazel is great!":
        ['sucks', 'sleazel'],
    "Let's not suck people, okay?":
        ['you', 'suck'],
    "I did actually.":
        ['who', 'asked'],
    "No lmao":
        ['give', 'drone', 'master'],
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
    "chameleon": " has found Chameleon's Oasis!",
}

COOLDOWN_SELECT = {
    "thief": "tsj",
    "spectre": "tsj",
    "joker": "tsj",
    "splicer": "tsj",
    "gun": "gun",
    "impostor": "gun",
    "archon": "ha",
    "heretic": "ha",
    "patron": "patron",
    "wicked": "general",
    "keeper": "general",
    "hacker": "general",
    "drifter": "general",
}

RIGS_DESCRIPTION = {
    "thief": "How long is your stack of stolen names? Actually, don't tell me.",
    "spectre": "There's a 50% chance this message will be empty.",
    "joker": "Imagine falling for your own prank.",
    "splicer": "How does it feel to cast an exclusive Rig?",
    "gun": "Peace is the only way.",
    "impostor": "Amogus amogus amogus amogus",
    "necromancer": "This space is sponsored by Lev. Please play their RPG game.",
    "archon": "I challenge you to find a typo in this fine sentence.",
    "heretic": "Fell for the oldest trick in the book.",
    "patron": "Let's keep this server clean, together.",
    "wicked": "No Roles?",
    "keeper": "Abcdefghijklmnpoqrstuvwxyz.",
    "hacker": "You truly deserve the Zero rank.",
    "drifter": "There's probably someone with your name but reversed somewhere on Discord.",
    "none": "Some cool stats, sadly nobody cares about these.",
}

COOLDOWN_DURATION = {
    "patron": 900,    
    "thief": 600,
    "spectre": 600,
    "joker": 600,
    "splicer": 600,
    "gun": 600,
    "impostor": 300,
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
    "gun": False,
    "impostor": False,
}

RIG_COOLDOWNS = {
    "general": False,
    "tsj": False,
    "ha": False,
    "patron": False,
    "gun": False,
}


COOLDOWN_DESCRIPTIONS = {
    "general": "<:csWicked:792143453035167754><:csKeeper:758081314912993283><:csDrifter:786323335880507483><:csHacker:758081540063494288> cooldown: ",
    "tsj": "<:csThief:758081386203840644><:csSpectre:1046200431342272512><:csJoker:758081245157654599><:csSplicer:988948000200069191> cooldown: ", #
    "ha": "<:csHeretic:786323224115281921><:csArchon:786323402172530688> cooldown: ",
    "patron": "<:csPatron:758081038697103504> cooldown: ",
    "gun": "<:csThegun:786629172101513216> cooldown: ",
}

# this roles can be assigned via a morph to command
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
    "Guns": [ 
        None,
        "I really hate guns, but if you insist.",
        "Finally you came to your senses.",
        "How about this gun?",
        "You are not a gun.",
     ],
}

FUN_ROLES = [
    "Sanctuary Discoverer",
    "Splicer",
    "Heretic Defier",
    "Architect Design",
    "Pranked the Creator",
    "I was there",
    "Zero",
    "Optimus",
    "Wise",
    "Impostor",
    "Persistent Clicker",
    "Lucky Button",
    "Last One",
    "Broken Drone Helper",
]

LIMITED_ROLES = {
    "I was there": "*(11/27/2022 - 11/28/2022)*",
    "Zero": "*(03/31/2023 - 04/19/2023)*",
    "Persistent Clicker": "*(04/18/2023 - 04/19/2023)*",
}

APPROVED_ROLES = {
    "Splicer": None,
    "Role Hunter": None,
}

FUN_LISTS = {
    "Sanctuary Discoverer": [],
    "Splicer": [],
    "Heretic Defier": [],
    "Architect Design": [],
    "Pranked the Creator": [],
    "I was there": [],
    "Zero": [],
    "Dreepy": [],
    "Wise": [],
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
        "Wait for someone to cast a Heretic Rig.",
        "You are already possessed...",
        "You are not possessed...",
        "Ask someone for mana.",
    ],
    # multiple words (ultimate chat killer) would break the script logic
    "Ultimate": [
        None,
        "Your message needs to be last for 2 hours in the <#624227331720085536> channel.",
        "You have already killed the chat.",
        "You were not a chat killer in the first place.",
        "There was an attempt.",
    ],
    "Shiny": [
        None,
        "You can't just morph to shiny! It's rare for a reason!",
        "You are already pretty sparkly, no need to add more shine to the mix!",
        "What. you don't have the role... why are you trying to lose it???",
        "Alright, your loss! ||just kidding||",
    ],

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
        "I spy with my little eye something beginning with the letter **H**.",
        "I spy with my little eye something beginning with the letter **A**.",
    ],
    'answers':[
        "stairs",
        "more stairs",
        "even more stairs",
        "how many stairs",
        "all the stairs",
    ],
}

BUTTONS = {
    "status": False,
    "channel": None,
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
    'ckr': 951424560685805588,            # chat killer
    'possessed': 988572669521842197,      # via rig
    'admin': 993446701090222160,          # aka Drone Master (not a discord admin)
    'murdurator': 735225462405464125,     # discord server moderator
    'climber': 735410759206568047,        # climber (consider adding manually verified)
}

CHAT_KILLER = {
    'wait': 7200,
    'last': 0,
    'reviveChat': False,
}

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
        828423681914437663:
            victim.mention + ", I am EXTREMELY disappointed in you. You know why. I do not forget.",
        805356486960087050:
            victim.mention + ", I am so disappointed in you... why did you even try bypassing? We all knew it wasn't going to work.",
        author.id:
            author.mention + " are you sad?",
    }
    return ScoldDict

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

# [0]attack    -> [1]damage
# [0]random    -> [1]min damage             [2]max damage
# [0]shield    -> [1]percentage protection, [2]number of turns
# [0]heavy     -> [1]damage,                [2]cooldown
# [0]special   -> [1]heal,                  [2]damage,                [3]charge hits
# [0]poison    -> [1]tick damage,           [2]turns,
# [0]h. poison -> [1]damage,                [2]tick damage,           [3]turns,               [4]cooldown
# [0]dodge     -> [1]chance                 [2]damage if successful
# [0]danger    -> [1]damage                 [2]self damage,
# [0]buff      -> [1]stat buff              [2]percentage buff,       [3]turns
# [0]debuff    -> [1]stat debuff            [2]percentage debuff,     [3]turns
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
