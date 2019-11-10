import discord
from discord import File
import os
from database import DBwrapper
import splitter

db = DBwrapper("db.json")


client = discord.Client()

@client.event
async def on_ready():
    chunks = splitter.chunk('test.JPG', 1000000)
    db.addFile('/test.JPG', [], [])
    i = 0
    for chunk in chunks:
        i += 1
        m = await client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i)))
        db.addChunk('/test.JPG', m.id)

client.run(open(".env", "r").read())