from filesystem import DiscordFileSystem

BotChannel = 642818966825336835

DFS = DiscordFileSystem('db.json')
with open('testdownload.jpg', 'wb') as f:
    f.write(DFS.download('/test.JPG').getvalue())

