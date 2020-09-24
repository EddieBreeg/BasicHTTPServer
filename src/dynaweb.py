from os import sys
from pathlib import Path
from os import path, makedirs
from utils.Server import Server
from http.server import HTTPServer
import json

# getting the directory the module has been called from
workingDir = Path().absolute()

if sys.argv[1] == "new":
    # creation of a new project
    projName = sys.argv[2]
    fullPath = path.join(workingDir, projName)
    if path.exists(fullPath):
        raise FileExistsError("Target location already exists")
    makedirs(fullPath)
    # generating the default settings
    defaults = """{
    "port": 1337,
    "host": "localhost",
    "static_dirs": ["static"],
    "media_dirs": ["media"]
}
"""
    with open(path.join(fullPath, "settings.json"), "w") as settingsFile:
        settingsFile.write(defaults)

elif sys.argv[1] == "run":
    # running the server
    try:
        settings = json.load(open(path.join(workingDir, "settings.json")))
    except FileNotFoundError:
        print("Not in a project directory, aborting.")
        exit()

    # defining the address
    if (l := len(sys.argv)) == 2:
        addr = (settings['host'], settings['port'])
    elif l == 3:
        addr = (sys.argv[2], settings['port'])
    else:
        addr = (sys.argv[2], int(sys.argv[3]))
    
    # creating the server
    server = HTTPServer(addr, Server)
    print("Server started on {0}:{1}".format(
        addr[0],
        addr[1]
    ))
    server.serve_forever()
