import discord
import os
from boto.s3.connection import S3Connection

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

TOKEN = S3Connection(os.environ['TOKEN'])
client.run(TOKEN)
