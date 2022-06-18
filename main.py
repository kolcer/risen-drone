import discord

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
    if message.content == "hi":
        await message.channel.send("hi!")
    return

client.run('OTU2MTM4MTA3MjgyMDIyNDQw.G94Fnd.7ho75D5rF4wZa9fDenlRB1WszW-wyzKvhJ2qFw')
