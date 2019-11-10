import discord
from discord import File
import os
from database import DBwrapper
import splitter

db = DBwrapper("db.json")


client = discord.Client()

@client.event
async def on_ready():
    splitter.chunk('test.JPG', 1000000)
    db.addFile('/test.JPG', [], [])

    for filename in os.listdir('chunks/'):
        m = await client.guilds[0].text_channels[0].send(file=File(open(os.path.join('chunks/', filename), 'rb')))
        db.addChunk('/test.JPG', m.id)

client.run(open(".env", "r").read())