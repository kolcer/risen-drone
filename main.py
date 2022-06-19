import discord
import os

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

    if "hi" in msg:
        await message.channel.send("hi!")
        return

    if "morph to architect" in msg:
        role = discord.utils.find(lambda r: r.name == 'Architect (Booster)', message.guild.roles)
          
        if role in usr.roles:
            await message.channel.send("You are already an Architect, smh.")
        else:
            await message.channel.send("You should boost the server if you crave for that role.")
        return

client.run(os.environ['TOKEN'])
