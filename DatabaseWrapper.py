from tinydb import TinyDB, Query


class DBwrapper(object):
    def __init__(self, filename):
        self.db = TinyDB(filename)

    def getFileAtPath(self, path):
        File = Query()
        file = self.db.search(File.path == path)
        return file[0]

    def addFile(self, path, info, chunks=[]):
        document = {'path': path, 'info': info, "chunks": chunks}
        self.db.insert(document)
        return True

    def addChunk(self, path, chunk):
        file = self.getFileAtPath(path)
        file['chunks'].append(chunk)
        self.db.writeback([file])
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
        self.db.writeback([file])
        return True
