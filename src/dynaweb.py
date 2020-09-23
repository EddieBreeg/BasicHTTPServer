from os import sys
from pathlib import Path
from os import path, makedirs
from dynawebUtils.Server import Server
from http.server import HTTPServer
import json

global workingDir
workingDir = Path().absolute()

if sys.argv[1] == "new":
    projName = sys.argv[2]
    fullPath = path.join(workingDir, projName)
    if path.exists(fullPath):
        raise FileExistsError("Target location already exists")
    makedirs(fullPath)
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
    print(workingDir)
    try:
        addr = json.load(open(path.join(workingDir, "settings.json")))
    except FileNotFoundError:
        print("Not in a project directory, aborting.")
        exit()

    addr = (addr['host'], addr['port'])
    server = HTTPServer(addr, Server)
    print("Server started on {0}:{1}".format(
        addr[0],
        addr[1]
    ))
    server.serve_forever()
