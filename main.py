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

    if usr.id != 956138107282022440:

        if "hi" in msg:
            await message.channel.send("hi!")
            return

        if "rip" in msg:
            await message.channel.send("rest in peace.")
            return


client.run(os.environ['TOKEN'])
