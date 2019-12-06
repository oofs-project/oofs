"""OOFS

Usage:
    main.py upload <filename>
    main.py download <filename>
    main.py delete <filename>

Options:
    -h --help   Shows this screen.
    --about     Shows what this is about.
    --version   Shows version.

"""
from docopt import docopt
import os

# BotChannel = 642818966825336835 does nothing


if __name__ == "__main__":
    arguments = docopt(__doc__, version="OOFS v1.0.0")
    print(arguments.items())
    for key, value in arguments.items(): 
        if arguments["upload"]:
            from filesystem import DiscordFileSystem
            DFS = DiscordFileSystem('db.json')
            file = DFS.openbin("/dfs."+arguments["<filename>"], mode="wb")
            with open(arguments["<filename>"], 'rb') as f:
                file.write(f.raw.read())
            file.copy()
            file.close()
            print("wrote")
            f = open(arguments["<filename>"], 'r+')
            f.truncate(0) # need '0' when using r+    
            os._exit(0)
        if arguments["download"]:
            from filesystem import DiscordFileSystem
            DFS = DiscordFileSystem('db.json')
            with open(arguments["<filename>"], 'wb') as f:
                f.write(DFS.openbin("/dfs."+arguments["<filename>"]).getvalue())
            print("finish")
            os._exit(0)
        

