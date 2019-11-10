from filesystem import DiscordFileSystem

BotChannel = 642818966825336835

DFS = DiscordFileSystem('db.json')

file = DFS.openbin("/city-skyline.bin", mode="wb")
with open('IGG-Cities.Skylines.Industries.iso', 'rb') as f:
    file.write(f.raw.read())

file.copy()
file.close()
print("wrote")

with open('cityskyline.bin', 'wb') as f:
    f.write(DFS.openbin('/city-skyline.bin').getvalue())
print("finish")
