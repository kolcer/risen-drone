import discord
import os

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


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Sane Ladders")
    await client.change_presence(activity=game)
    return

@client.event
async def on_message(message):
    msg = message.content
    usr = message.author

    if usr.bot == False:

        if not msg.startswith(">"):

            msg = msg.lower()
            if "morph to" in msg:

                good_roles = {}
                server_roles = message.guild.roles
                #usr_roles = usr.roles

                for role in server_roles:
                    if role.name in Roles:
                        good_roles[role.name] = role

                if "gun" in msg:
                    await message.channel.send("smh... FINE!")
                    await usr.edit(nick=random.choice(Worst_guns))
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
        
        
        
        if any(word in msg for word in salute) and "risen drone" in msg:
            await message.channel.send('Hello!')
            return

        if "rip" in msg:
            await message.channel.send("rest in peace.")
            return

        if "morph to architect" in msg:
          role = discord.utils.find(lambda r: r.name == 'Architect (Booster)', message.guild.roles)
          
          if role in usr.roles:
            await message.channel.send("You are already an Architect, smh.")
          else:
            await message.channel.send("You should boost the server if you crave for that role.")
          return


client.run(os.environ['TOKEN'])
