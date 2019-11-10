from tinydb import TinyDB, Query


class DBwrapper(object):
    def __init__(self, filename):
        self.db = TinyDB(filename)

    def getFileAtPath(self, path):
        File = Query()
        file = self.db.get(File.path == path)
        return file

    def pathExist(self, path):
        File = Query()
        exists = self.db.contains(File.path == path)
        return exists

    def getFilesInFolder(self, path):
        Files = Query()
        files = self.db.search(Files.parent == path)
        return files

    def addFile(self, path, info, chunks=[]):
        parent = ''.join(path[1:].split('/')[:-1])
        document = {'path': path, 'parent': parent, 'info': info, "chunks": chunks}
        if not self.pathExist(path):
            self.db.insert(document)
            return True
        else:
            return False

    def removeChunks(self, path):
        file = self.getFileAtPath(path)
        file['chunks'] = []
        self.db.write_back([file])
        return True
    def addChunk(self, path, chunk):
        file = self.getFileAtPath(path)
        file['chunks'].append(chunk)
        self.db.write_back([file])
        return True

    def getChunks(self, path):
        file = self.getFileAtPath(path)
        return file['chunks']

    def getInfo(self, path):
        file = self.getFileAtPath(path)
        return file['info']

    def setInfo(self, path, info):
        file = self.getFileAtPath(path)
        file['info'] = info
        self.db.write_back([file])
        return True
