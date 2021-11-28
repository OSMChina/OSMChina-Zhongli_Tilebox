import os
import platform
import json
from math import sqrt

from src.requester import request_task

global WHITE_LIST
global TILE_SERVER


def UA():
    PROGRAME_NAME = "OSMChina-TileRequest"
    PROGRAME_VERSION = "0.3.0"
    PLATFORM_SYSTEM = platform.system()
    PLATFORM_VERSION = platform.version()
    PLATFORM_MACHINE = platform.machine()
    PLATFORM_PYTHON = platform.python_version()
    UA_BASIC = PROGRAME_NAME + "/" + PROGRAME_VERSION
    UA_EXTEND = "(" \
                + PLATFORM_SYSTEM + " " + PLATFORM_VERSION + "; " \
                + PLATFORM_MACHINE + "; " \
                + ")" \
                + " Python/" + PLATFORM_PYTHON
    return UA_BASIC + " " + UA_EXTEND


headers = {
    "User-Agent": "OSMChina-TileRequest/0.3.0",
    "Cookie": "",
}

def taskGenerator(task:str, zoom: int, tile_name, task_name, x_min=0, x_max=0, y_min=0, y_max=0,
                  grid_pos=(0, 0), MODE="Region", ALLOW_MP=False):
    # INIT
    global WHITE_LIST
    global TILE_SERVER
    headers["User-Agent"] = UA()
    if platform.system() == "Windows":
        WHITE_LIST = json.loads(open('..\\res\\control_list.json').read())[
            'WHITE_LIST']
        TILE_SERVER = json.loads(open('..\\res\\tile_server.json').read())
    else:
        WHITE_LIST = json.loads(
            open('../res/control_list.json').read())['WHITE_LIST']
        TILE_SERVER = json.loads(open('../res/tile_server.json').read())
    # TASK
    if MODE == "Region":
        if zoom == 0:
            print("Error: zoom must be greater than 0 in Region MODE")
        else:
            if x_min == 0 and x_max == 0 and y_min == 0 and y_max == 0:
                x_min = int(input("Please input x_min:"))
                x_max = int(input("Please input x_max:"))
                y_min = int(input("Please input y_min:"))
                y_max = int(input("Please input y_max:"))
            count = (x_max - x_min + 1) * (y_max - y_min + 1)
            print("Total tiles:", count)
            request_task(x_min, x_max, y_min, y_max, zoom,
                         tile_name, task_name, ALLOW_MP)
    elif MODE == "Full":
        if zoom == 0:
            count = 1
            print("Total tiles:", count)
            request_task(0, 0, 0, 0, 0, tile_name, task_name)
        else:
            count = pow(2, zoom * 2)
            print("Total tiles:", count)
            request_task(0, pow(2, zoom) - 1, 0, pow(2, zoom) -
                         1, zoom, tile_name, task_name, ALLOW_MP)
    elif MODE == "Grid":
        def findNearstPow2(x: int):
            for i in range(19):
                if pow(2, i) >= x:
                    return pow(2, i)

        tolerance_zoom = 7
        grid_zoom = int(pow(2, int(zoom - tolerance_zoom + 1))) // 2
        if zoom >= 10:
            grid_zoom = findNearstPow2(
                int(sqrt(int(pow(3, int(zoom - tolerance_zoom + 1))) // 1.5)))
        if grid_zoom <= 0:
            grid_zoom = 0
        if grid_zoom <= 1:
            grid_number = int(pow(2, grid_zoom // 2))
        elif zoom >= 10:
            grid_number = int(pow(2, grid_zoom // 2))
        else:
            grid_number = int(pow(2, grid_zoom))
        if grid_number > 65536:
            grid_number = 65536 * pow(2, findNearstPow2(zoom - tolerance_zoom - 3))
        print("zoom:", zoom)
        print("grid_zoom:", grid_zoom)
        print("grid_number:", grid_number)
        count = pow(2, zoom * 2)
        print("Total tiles:", count)
        print("===")
    else:
        print("Error: MODE Error")


if __name__ == "__main__":
    TASK_MODE = "Debug"
    # Suggested TASK_MODE: Backup, Debug, Development,PressureTest
    os.system("mkdir OSMChina_" + TASK_MODE)
    os.chdir("OSMChina_" + TASK_MODE)
    LOW_ZOOM = 0
    HIGH_ZOOM = 11
    for i in range(LOW_ZOOM, HIGH_ZOOM + 1):
        taskGenerator("requester",i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), MODE="Grid", ALLOW_MP=False)