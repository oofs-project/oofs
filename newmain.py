from filesystem import DiscordFileSystem

BotChannel = 642818966825336835

DFS = DiscordFileSystem('db.json')

file = DFS.openbin("/jetbrains.exe", mode="wb")
with open('jetbrains-toolbox-1.11.4269.exe', 'rb') as f:
    file.write(f.raw.read())

file.copy()
file.close()
print("wrote")

with open('jetbrains.exe', 'wb') as f:
    f.write(DFS.openbin('/jetbrains.exe').getvalue())
