import discord
from discord import File
from diskcollections.iterables import FileList

import splitter
from database import DBwrapper

BotChannel = 642818966825336835
db = DBwrapper("db.json")


client = discord.Client()


async def upload(filename, VirtualPath):
    chunks = splitter.chunk(filename, 1000000)
    db.addFile(VirtualPath, [], [])
    i = 0
    for chunk in chunks:
        i += 1
        m = await client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i)))
        db.addChunk(VirtualPath, m.id)

@client.event
async def on_ready():
    flist = FileList()
    Ids = db.getChunks("/test.JPG")  # List of message IDs
    for id in Ids:
        message = client.get_channel(BotChannel).get_message(id)
        print(message)


client.run(open(".env", "r").read())