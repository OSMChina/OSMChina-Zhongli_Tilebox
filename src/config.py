import os
import json

# global WHITE_LIST
# global TILE_SERVER

pwd = os.path.dirname(os.path.realpath(__file__))
path_control_list = os.path.join(pwd, "..", "res", "control_list.json")
path_tile_server = os.path.join(pwd, "..", "res", "tile_server.json")
WHITE_LIST = json.loads(open(path_control_list).read())["WHITE_LIST"]
TILE_SERVER = json.loads(open(path_tile_server).read())
