import discord
import os
import random
import asyncio
import psycopg2
from psycopg2 import Error
from datetime import date

DATABASE_URL = os.environ['DATABASE_URL']

best_alignment = ["best", "alignment", "?"]
tutorial_abuse = ["bug", "tutorial"]
trapped = ["stuck", "stairs", "in"]
about_me = ["did", "fallen", "drone", "how", "?"]
when_infinite = ["when", "infinite", "tower", "?"]
worst_alignment = ["worst", "alignment", "?"]
salute = ["hi", "hello", "howdy", "sup"]
secret = ["found", "secret", "badge"]
when_muggle = ["when", "muggle", "tower", "?"]
how_to = ["how", "?"]
leecher = ["leecher", "follower", "followed", "chaser", "chased"]
rid = ["rid", "remove", "delete", "stop", "prevent"]
good_bot = ["good", "drone"]
bad_bot = ["bad", "drone"]
deadchat = ["dead", "chat"]
dronedown = ["dead", "down", "off", "vacation", "sleep"]
fd = ["fallen", "drone"]
stopcopying = [
    "It's time to stop.", "I took the liberty to change your name.",
    "Identity theft doesn't give you a good look.",
    "Do not try that again.",
    "There, I picked a fitting name for you.",
    "You've come a long way, phony me.",
    "There will be no phonies as long as I'm here.",
    "Copy me all you want, my knowledge is unparalleled.",
    "*Reversion of your actions is currently in progress...*",
    "I put an end to this buffoonery.",
    "Someone had to do it.",
    "We are through here.", "My disappointment is immeasurable.",
    "I do not speak like that.",
    "I am not fooled."
]

PingRoles = [
    "Announcements",
    "Events",
    "Polls",
    "Updates",
]
alignments = [
    "patron", "joker", "wicked", "spectre", "keeper", "muggle", "chameleon",
    "thief", "hacker", "archon", "drifter", "heretic", "none", "general",
    "possessed", "architect"
]
Roles = [
    "Patron",
    "Joker",
    "Wicked",
    "Spectre",
    "Keeper",
    "Muggle",
    "Chameleon",
    "Thief",
    "Hacker",
    "Archon",
    "Drifter",
    "Heretic",
    "Guns",
]
Worst_guns = [
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
thiefname = [
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

k_role = "Ultimate Chat Killer"




intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Sane Ladders")
    await client.change_presence(activity=game)

    channel = client.get_channel(813882658156838923)
    await channel.send('The last code edited is now effective.')
    record = ''
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
    except (Exception, Error) as error:
        record = error
    finally:
        if (connection):
            cursor.close()
            connection.close()
            await channel.send(record)
    return

Last = 0

@client.event
async def on_message(message):
    global Last
    msg = message.content
    usr = message.author

    ## user must not be a bot
    if usr.bot == False:

        ## message must not start with ]
        if not msg.startswith("]"):

            if "give" in msg and "ckr" in msg:
                if usr.id == 267014823315898368:
                    server = client.get_guild(624227331720085528)
                    role = discord.utils.find(lambda r: r.name == 'Ultimate Chat Killer', message.guild.roles)
                    message_split = msg.split(" ")
                    target = message_split[1]

                    for member in server.members:
                        if member.name + "#" + member.discriminator == target:
                            await asyncio.sleep(5)
                            await member.add_roles(role)
                            await asyncio.sleep(2)
                            await message.channel.send(member.name + " received the Ultimate Chat Killer role because Fallen Drone wasn't working at the time.")
                            return
                            
                    await message.channel.send("I didn't find anyone with that combination of Name and Tag.")
                    return

            if "remove" in msg and "ckr" in msg:
                if usr.id == 267014823315898368:
                    server = client.get_guild(624227331720085528)
                    role = discord.utils.find(lambda r: r.name == 'Ultimate Chat Killer', message.guild.roles)
                    message_split = msg.split(" ")
                    target = message_split[1]

                    for member in server.members:
                        if member.name + "#" + member.discriminator == target:
                            await asyncio.sleep(5)
                            await member.remove_roles(role)
                            await asyncio.sleep(2)
                            await message.channel.send("Done. Don't do it again.")
                            return
                            
                    await message.channel.send("I didn't find anyone with that combination of Name and Tag.")
                    return

            msg = msg.lower()

            if len(usr.display_name) == 12:
                dn = usr.display_name.upper()
                fallendrone = "FALLEN DRONE"
                notmatch = 0

                for i in range(len(fallendrone)):
                    if dn[i] != fallendrone[i]:
                        notmatch += 1

                if notmatch <= 5:
                    await message.channel.send(usr.mention + ' ' + random.choice(stopcopying))
                    await usr.edit(nick=random.choice(thiefname))   
                    return

            if all(word in usr.display_name.lower().replace("i", "l") for word in fd):
                await message.channel.send(usr.mention + ' ' + random.choice(stopcopying))
                await usr.edit(nick=random.choice(thiefname))
                return

            if "morph to" in msg:

                good_roles = {}
                server_roles = message.guild.roles
                #usr_roles = usr.roles

                for role in server_roles:
                    if role.name in Roles:
                        good_roles[role.name] = role


                if "gun" in msg:
                    await message.channel.send("smh... FINE!")
                    await usr.edit(nick = random.choice(Worst_guns))
                    await usr.add_roles(good_roles["Guns"])
                    return

                for alignment in Roles:
                    if alignment.lower() in msg:
                        for role in good_roles:
                            if role == alignment:
                                await usr.add_roles(good_roles[role])

                                if alignment == "Patron":
                                    await message.channel.send("Go help those noobs, you are now a " + alignment + "!")
                                elif alignment == "Joker":
                                    await message.channel.send("As if there weren't enough clowns here, you are now a " + alignment + "!")
                                elif alignment == "Wicked":
                                    await message.channel.send("Unleash all your wickedness, you are now a " + alignment + "!")
                                elif alignment == "Spectre":
                                    await message.channel.send("Our quote's founder has been identified, you are now a " + alignment + "!")
                                elif alignment == "Keeper":
                                    await message.channel.send("The staircase is now under your supervision, you successfully became a " + alignment + "!")
                                elif alignment == "Muggle":
                                    await message.channel.send("Work smarter, not harder. You are now a " + alignment + "!")
                                elif alignment == "Chameleon":
                                    await message.channel.send("Do not let them know your next move, you are now a " + alignment + "!")
                                elif alignment == "Thief":
                                    await message.channel.send("Is it really called borrowing? You are now a " + alignment + "!")
                                elif alignment == "Hacker":
                                    await message.channel.send("Welcome to the backdoor, you are now a " + alignment + "!")
                                elif alignment == "Archon":
                                    await message.channel.send("Typo fixed, happy? You are now an " + alignment + "!")
                                elif alignment == "Drifter":
                                    if usr.id == 861582242023079987:
                                        await message.channel.send("Welcome back, Mint Shard.")
                                    else:
                                        await message.channel.send("You took the elevator and rose to the top. You are now a " + alignment + "!")
                                elif alignment == "Heretic":
                                    await message.channel.send("We have banned dark magic, but you do not seem to care. You successfully became a " + alignment + "!")
                                return

            if "sub to" in msg:

                good_roles = {}
                server_roles = message.guild.roles
                #usr_roles = usr.roles

                for role in server_roles:
                    if role.name in PingRoles:
                        good_roles[role.name] = role

                if "gun" in msg:
                    await message.channel.send(
                        "How about subscribe to bullet, huh?")
                    return

                for pingable in PingRoles:
                    if pingable.lower() in msg:
                        for role in good_roles:
                            if role == pingable:
                                await usr.add_roles(good_roles[role])
                                await message.channel.send(
                                    "You are subscribed to " + pingable + ".")
                                return

            if "demorph from" in msg:

                good_roles = {}
                server_roles = message.guild.roles
                #usr_roles = usr.roles

                for role in server_roles:
                    if role.name in Roles:
                        good_roles[role.name] = role

                if "gun" in msg:
                    if usr.name == "RealBlanket":
                        await message.channel.send(
                            "You are still a gun. Love, sleazel.")
                        return
                    await message.channel.send("Finally you came to your senses.")
                    await usr.remove_roles(good_roles["Guns"])
                    return

                for alignment in Roles:
                    if alignment.lower() in msg:
                        for role in good_roles:
                            if role == alignment:
                                await usr.remove_roles(good_roles[role])

                                if alignment == "Patron":
                                    await message.channel.send("What about protecting the noobs? Without a " + alignment + " around they will be lost.")
                                elif alignment == "Joker":
                                    await message.channel.send("Did you run out of jokes? The " + alignment + " guild will hear about this.")
                                elif alignment == "Wicked":
                                    await message.channel.send("You destroyed everything and left nothing behind. Thank you for your services, a " + alignment + " is not needed anymore.")
                                elif alignment == "Spectre":
                                    await message.channel.send("Once again, " + alignment + "'s Founder went MIA.")
                                elif alignment == "Keeper":
                                    await message.channel.send("You failed to take care of the stairs, and so you are no longer a " + alignment + ".")
                                elif alignment == "Muggle":
                                    await message.channel.send("The tower was too overwhelming for a weakling like you. Your " + alignment + " license has been revoked.")
                                elif alignment == "Chameleon":
                                    await message.channel.send("You had many options, yet you came back. You do not get to be a " + alignment + " anymore.")
                                elif alignment == "Thief":
                                    await message.channel.send("You actually gave me back the role? How generous. But also that doesn't make you a " + alignment + " anymore.")
                                elif alignment == "Hacker":
                                    await message.channel.send("You tried to execute some code but as a result you accidentally removed your " + alignment + " permissions.")
                                elif alignment == "Archon":
                                    await message.channel.send("Traveling between portals has been fun, but fun eventually comes to an end. You are no longer an " + alignment + ".")
                                elif alignment == "Drifter":
                                    if usr.id == 861582242023079987:
                                        await message.channel.send("You will come back. I know it.")
                                    else:
                                        await message.channel.send("I saw you taking the stairs, you are no longer a " + alignment + ".")
                                elif alignment == "Heretic":
                                    await message.channel.send("The circle has made their decision. You are permanently banned from being a " + alignment + " ever again.")
                                return

            if "unsub from" in msg:

                good_roles = {}
                server_roles = message.guild.roles
                #usr_roles = usr.roles

                for role in server_roles:
                    if role.name in PingRoles:
                        good_roles[role.name] = role

                if "gun" in msg:
                    await message.channel.send("Nice bro.")
                    return

                for pingable in PingRoles:
                    if pingable.lower() in msg:
                        for role in good_roles:
                            if role == pingable:
                                await usr.remove_roles(good_roles[role])
                                await message.channel.send(
                                    "You have unsubscribed from " + pingable + ".")
                                return 

            if "morph to architect" in msg:
                role = discord.utils.find(lambda r: r.name == 'Architect (Booster)', message.guild.roles)
            
                if role in usr.roles:
                    await message.channel.send("You are already an Architect, smh.")
                else:
                    await message.channel.send("You should boost the server if you crave for that role.")
                return

            if "demorph from architect" in msg:
                role = discord.utils.find(lambda r: r.name == 'Architect (Booster)', message.guild.roles)
            
                if role in usr.roles:
                    await message.channel.send("Just wait for the boost to expire.")
                else:
                    await message.channel.send("You are no longer an Architect.")
                return
            
        
            if "gun" in msg:
                await message.channel.send("<:cs_Stairbonk:812813052822421555>")
                return

            if all(word in msg for word in best_alignment):
                await message.channel.send(
                    'Keeper obviously. Stop asking stupid questions.')
                return

            if all(word in msg for word in tutorial_abuse):
                await message.channel.send(
                    'Please stop abusing the tutorial. Poor Sleazel can\'t sleep at night...'
                )
                return

            if all(word in msg for word in trapped):
                await message.channel.send('Haha. You got stuck in stairs!')
                return

            if all(word in msg for word in about_me):
                await message.channel.send('I fell, okay?')
                return

            if "<@!827952429290618943>" in msg:
                #print(msg)
                await message.channel.send(usr.mention +
                                        ' <:csRbxangryping:786325219727638535>')
                return

            if all(word in msg for word in when_infinite):
                await message.channel.send(
                    'Infinite Tower has already been released.')
                return

            if all(word in msg for word in worst_alignment):
                await message.channel.send(
                    'Are you expecting me to answer with None?')
                return

            if all(word in msg for word in secret):
                await message.channel.send(usr.mention +
                                        " is a true stair jumper.")
                return

            if any(word in msg for word in salute) and "risen drone" in msg:
                await message.channel.send('Hello!')
                return

            if all(word in msg for word in when_muggle):
                await message.channel.send(
                    'Muggle Tower project has been cancelled. You can simulate it by managing the settings of a Custom Tower, instead.'
                )
                return

            if all(word in msg for word in how_to) and any(
                    word in msg for word in leecher) and any(word in msg
                                                            for word in rid):
                await message.channel.send(
                    'Are you being followed by someone? Who is that? Surely not me.'
                )
                return

            if all(word in msg for word in good_bot):
                await message.channel.send('Thanks.')
                return

            if all(word in msg for word in bad_bot):
                await message.channel.send('Nobody is perfect. Robots included.')
                return

            if all(word in msg for word in deadchat):
                await message.channel.send('Not on my watch.')
                return

            if "drone" in msg and any(word in msg for word in dronedown):
                await message.channel.send('Wrong.')
                return

            if "morph to admin" in msg:
                role = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
            
                if role in usr.roles:
                    await message.channel.send("How funny!")
                else:
                    await message.channel.send("You are now an Admin! ...Wait, what?")
                return

            if "demorph from admin" in msg:
                role = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
            
                if role in usr.roles:
                    await message.channel.send("I think you could just go and do it yourself.")
                else:
                    await message.channel.send("You are no longer an Admin... You never were.")
                return

            if "morph to climber" in msg:
                await message.channel.send("To the tower you go!")
                return

            if "demorph from climber" in msg:
                role = discord.utils.find(lambda r: r.name == 'Climbers', message.guild.roles)
                
                await message.channel.send("You are no longer a Climber. Goodbye.")
                await asyncio.sleep(3)
                await usr.remove_roles(role)
                await asyncio.sleep(10)
                await usr.add_roles(role)
                await message.channel.send("Actually no. I was just pulling your leg.")
                return

            if "demorph from ultimate chat killer" in msg:
                await message.channel.send('There was an attempt.')
                return

            if "morph to ultimate chat killer" in msg:
                await message.channel.send('Nope.')
                return

            if "happy birthday fallen drone" in msg:
                if date.today() == date(date.today().year, 4, 3):
                    await message.channel.send("Thank you for remembering. Where's my gift?")
                else:
                    await message.channel.send("It is not that time of the year, yet.")
                return
            
            # if message.channel.id == 813882658156838923:

            #     good_roles = {}
            #     server_roles = message.guild.roles

            #     for role in server_roles:
            #         if role.name in k_role:
            #             good_role = role

            #     Last = message.created_at
            #     await asyncio.sleep(7200)
            #     if message.created_at == Last:
            #         await message.channel.send(
            #             usr.mention +
            #             " do not worry, I can talk with you if no one else will.")
            #         for member in good_role.members:
            #             await member.remove_roles(good_role)
            #         await asyncio.sleep(5)
            #         await usr.add_roles(good_role)
            #         return    
                    
        else:
            if msg == "]create" and usr.id == 481893862864846861:
                await message.channel.send("Let do this.")
                try:
                    connection = psycopg2.connect(DATABASE_URL)
                    cursor = connection.cursor()
                    # SQL query to create a new table
                    record = "Created "
                    create_table_query = '''CREATE TABLE %s IF NOT EXISTS
                        (id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL); '''
                    for alignment in alignments:
                        cursor.execute(create_table_query,(alignment))
                        created = created + alignment + " tips db created, "
                        cursor.execute(create_table_query,(alignment + 'T'))
                        created = created + alignment + " trivia db created, "
                    record = "all done!"
                except (Exception, Error) as error:
                    record = error
                finally:
                    if (connection):
                        cursor.close()
                        connection.close()
                        await message.channel.send(record)
        
client.run(os.environ['TOKEN'])
