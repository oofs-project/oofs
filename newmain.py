from filesystem import DiscordFileSystem

BotChannel = 642818966825336835

DFS = DiscordFileSystem('db.json')

file = DFS.openbin("/1g.bin", mode="wb")
with open('1GB.bin', 'rb') as f:
    file.write(f.raw.read())

file.copy()
file.close()
print("wrote")

with open('1GB discorded.bin', 'wb') as f:
    f.write(DFS.openbin('/1g.bin').getvalue())
print("finish")
