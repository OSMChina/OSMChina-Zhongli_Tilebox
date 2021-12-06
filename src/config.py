import platform
import json

global WHITE_LIST
global TILE_SERVER
if platform.system() == "Windows":
    WHITE_LIST = json.loads(open("..\\res\\control_list.json").read())[
        "WHITE_LIST"
    ]
    TILE_SERVER = json.loads(open("..\\res\\tile_server.json").read())
else:
    WHITE_LIST = json.loads(open("../res/control_list.json").read())[
        "WHITE_LIST"
    ]
    TILE_SERVER = json.loads(open("../res/tile_server.json").read())