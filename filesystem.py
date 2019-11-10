import asyncio
import io
import threading
import time

import discord
import fs.errors
from discord import File
from fs.base import FS
from fs.info import Info

import splitter
from database import DBwrapper


class tempFile(io.BytesIO):
    def __init__(self, DFS, bytes, path):
        super().__init__(bytes)
        self.path = path
        self.DFS = DFS

    def copy(self) -> None:
        print("Closing")
        chunks = splitter.chunkBytes(self.getvalue(), 8000000)
        print(chunks)
        if not self.DFS.DB.pathExist(self.path):
            self.DFS.DB.addFile(self.path, [], [])
        self.DFS.DB.removeChunks(self.path)
        i = 0
        len(chunks)
        for chunk in chunks:
            print(str((i / len(chunks)) * 100) + f"% done. {i} out of {len(chunks)}")

            i += 1
            print("Uploading chunk " + str(i))
            m = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i))),
                DiscordFileSystem.client.loop).result()
            self.DFS.DB.addChunk(self.path, m.id)



async def start():
    await DiscordFileSystem.client.start(open(".env", "r").read())


def run_it_forever(loop):
    loop.run_forever()

class DiscordFileSystem(FS):
    client = discord.Client()

    loop = asyncio.get_event_loop()
    loop.create_task(start())
    thread = threading.Thread(target=run_it_forever, args=(loop,))
    thread.start()
    BotChannel = 642818966825336835

    def upload2(self, filename, VirtualPath):
        chunks = splitter.chunk(filename, 8000000)
        self.DB.addFile(VirtualPath, [], [])
        i = 0
        for chunk in chunks:
            i += 1
            print("Uploading chunk " + str(i))
            m = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i))),
                DiscordFileSystem.client.loop).result()
            self.DB.addChunk(VirtualPath, m.id)

    def download2(self, VirtualPath):
        if self.DB.pathExist(path=VirtualPath):
            Ids = self.DB.getChunks(VirtualPath)  # List of message IDs
        else:
            Ids = []
        tosave = io.BytesIO()
        for id2 in Ids:
            print("ran")
            message = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.get_channel(DiscordFileSystem.BotChannel).fetch_message(id2),
                self.client.loop).result()
            asyncio.run_coroutine_threadsafe(message.attachments[0].save(tosave, seek_begin=False, use_cached=False),
                                             self.client.loop).result()
            print(message)
        return tosave

    def __init__(self, pathToDB):

        while not DiscordFileSystem.client.is_ready():
            time.sleep(1)
        print("Started!")
        self.DB = DBwrapper(pathToDB)
        super().__init__()

    def getinfo(self, path, namespaces=['basic']):
        info = Info(self.DB.getInfo(path))
        return info


    def listdir(self, path):
        info = self.DB.getInfo(path)
        if not info.get('basic', 'id_dir'):
            raise fs.errors.DirectoryExpected
        if not self.DB.pathExist(path):
            raise fs.errors.ResourceNotFound

        FileDocs = self.DB.getFilesInFolder(path)
        files = []
        for i in FileDocs:
            if i['path'][0] == "/":
                i['path'] = i['path'][1:]
            if i['path'][-1] == "/":
                i['path'][-1] = i['path'][-2]
            name = i['path'].split("/")[-1]
            files.append(name)
        return files


    def makedir(self, path, permissions=None, recreate=False):
        pass

    def openbin(self, path, mode="r", buffering=-1, **options):
        bytes = self.download2(path)
        return tempFile(self, bytes.getvalue(), path)

    def remove(self, path):
        pass

    def removedir(self, path):
        pass

    def setinfo(self, path, info):
        self.DB.setInfo(path, info)
