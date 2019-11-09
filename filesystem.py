from fs.base import FS


class DiscordFileSystem(FS):
    def __init__(self):
        super().__init__()
        pass

    def getinfo(self, path, namespaces=None):
        pass

    def listdir(self, path):
        pass

    def makedir(self, path, permissions=None, recreate=False):
        pass

    def openbin(self, path, mode="r", buffering=-1, **options):
        pass

    def remove(self, path):
        pass

    def removedir(self, path):
        pass

    def setinfo(self, path, info):
        pass
