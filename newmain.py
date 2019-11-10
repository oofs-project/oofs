from filesystem import DiscordFileSystem

# BotChannel = 642818966825336835 does nothing

DFS = DiscordFileSystem('db.json')

file = DFS.openbin("/100MB.zip", mode="wb")
with open('100MB.zip', 'rb') as f:
    file.write(f.raw.read())

file.copy()
file.close()
print("wrote")

with open('100MB.1.zip', 'wb') as f:
    f.write(DFS.openbin('/100MB.zip').getvalue())
print("finish")
