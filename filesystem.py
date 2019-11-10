import fs.errors
from fs.base import FS
from fs.info import Info

from DatabaseWrapper import DBwrapper

import encdec


class DiscordFileSystem(FS):
    def __init__(self, pathToDB):
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
        encdec.decodeFile()

    def remove(self, path):
        pass

    def removedir(self, path):
        pass

    def setinfo(self, path, info):
        pass
