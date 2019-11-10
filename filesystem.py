import asyncio
import io
import threading
import time
from tempfile import SpooledTemporaryFile

import discord
import fs.errors
from discord import File
from fs.base import FS
from fs.info import Info

import splitter
from database import DBwrapper


class ModifiedTemp(SpooledTemporaryFile):
    def __init__(self, DFS, realpath, max_size=0, mode='w+b', buffering=-1,
                 encoding=None, newline=None,
                 suffix=None, prefix=None, dir=None):
        super().__init__(self, max_size, mode, buffering,
                         encoding, newline,
                         suffix, prefix, dir)
        self._file = DFS.download(realpath)
        self.DFS = DFS
        self.realpath = realpath

    def __exit__(self, exc_type, exc_val, exc_tb):
        chunks = splitter.chunkBytes(self._file.read(), 1000000)
        if not self.DFS.DB.pathExist(self.realpath):
            self.DFS.DB.addFile(self.realpath, [], [])
        self.DFS.DB.removeChunks(self.realpath)
        i = 0
        for chunk in chunks:
            i += 1
            m = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i))),
                DiscordFileSystem.client.loop).result()
            self.DB.addChunk(self.realpath, m.id)
        self._file.close()

    def close(self):
        chunks = splitter.chunkBytes(self._file.read(), 1000000)
        if not self.DFS.DB.pathExist(self.realpath):
            self.DFS.DB.addFile(self.realpath, [], [])
        self.DFS.DB.removeChunks(self.realpath)
        i = 0
        for chunk in chunks:
            i += 1
            m = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i))),
                DiscordFileSystem.client.loop).result()
            self.DB.addChunk(self.realpath, m.id)
        self._file.close()


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

    def upload(self, filename, VirtualPath):
        chunks = splitter.chunk(filename, 1000000)
        self.DB.addFile(VirtualPath, [], [])
        i = 0
        for chunk in chunks:
            i += 1
            m = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.guilds[0].text_channels[0].send(file=File(chunk, filename=str(i))),
                DiscordFileSystem.client.loop).result()
            self.DB.addChunk(VirtualPath, m.id)

    def download(self, VirtualPath):
        Ids = self.DB.getChunks(VirtualPath)  # List of message IDs
        tosave = io.BytesIO()
        for id in Ids:
            message = asyncio.run_coroutine_threadsafe(
                DiscordFileSystem.client.get_channel(DiscordFileSystem.BotChannel).fetch_message(id),
                DiscordFileSystem.client.loop).result()
            asyncio.run_coroutine_threadsafe(message.attachments[0].save(tosave, seek_begin=False, use_cached=False),
                                             DiscordFileSystem.client.loop).result()
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
        return ModifiedTemp(self, path, 0, mode, buffering)

    def remove(self, path):
        pass

    def removedir(self, path):
        pass

    def setinfo(self, path, info):
        self.DB.setInfo(path, info)
