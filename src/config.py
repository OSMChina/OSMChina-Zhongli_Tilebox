import os
import platform
import json

global WHITE_LIST
global TILE_SERVER
pwd=os.path.dirname(os.path.realpath(__file__))
path_control_list=os.path.join(pwd,"..","res","control_list.json")
if platform.system() == "Windows":
    WHITE_LIST = json.loads(open(path_control_list).read())[
        "WHITE_LIST"
    ]
    TILE_SERVER = json.loads(open("..\\res\\tile_server.json").read())
else:
    WHITE_LIST = json.loads(open("../res/control_list.json").read())[
        "WHITE_LIST"
    ]
    TILE_SERVER = json.loads(open("../res/tile_server.json").read())