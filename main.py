"""OOFS

Usage:
    main.py upload <filename>
    main.py download <filename>
    main.py delete <filename>

Options:
    -h --help   Shows this screen.
    --about     Shows what this is about.
    --version   Shows version.

"""
from docopt import docopt

import discord
from discord import File
from diskcollections.iterables import FileList
import io

import splitter
from database import DBwrapper

import argparse

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
    tosave = io.BytesIO()
    for id in Ids:
        message = await client.get_channel(BotChannel).fetch_message(id)
        await message.attachments[0].save(tosave, seek_begin=False, use_cached=False)
    with open("test-unchunked.jpg", 'wb') as f:
        f.write(tosave.getbuffer())


if __name__ == "__main__":
    arguments = docopt(__doc__, version="OOFS v1.0.0")
    print(arguments)
    client.run(open(".env", "r").read())


