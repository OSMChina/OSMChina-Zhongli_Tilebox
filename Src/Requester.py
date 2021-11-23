import os
import platform
import time
import json
import random
import threading
from math import sqrt

import requests

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


def RandomChar(begin: str, end: str):
    range = int(ord(end) - ord(begin))
    tmp = random.randint(0, range - 1)
    return chr(ord(begin) + tmp)


def fullURL(x: int, y: int, z: int, tile_name):
    # PREFIX
    PROTOCOL_PREFIX_HTTPS = "https://"
    PROTOCOL_PREFIX_HTTP = "http://"
    PROTOCOL_PREFIX_FTP = "ftp://"
    # 开始组装准备
    url = TILE_SERVER[tile_name][0]
    # 检查URL是否合法
    for i in WHITE_LIST:
        if i in url:
            break
    else:
        print("Error: Not OSMChina tile service!")
    # 复杂替换预配置
    protocol_list = TILE_SERVER[tile_name][1]
    if TILE_SERVER[tile_name][2] != "":
        random_list = [TILE_SERVER[tile_name][2].split(
            "-")[0], TILE_SERVER[tile_name][2].split("-")[1]]
    else:
        random_list = ""
    # 组装协议
    if protocol_list[0] == "https":
        url = url.replace("{protocol}", PROTOCOL_PREFIX_HTTPS)
    elif protocol_list[0] == "ftp":
        url = url.replace("{protocol}", PROTOCOL_PREFIX_FTP)
    else:
        url = url.replace("{protocol}", PROTOCOL_PREFIX_HTTP)
    # 组装负载均衡
    if random_list != "":
        url = url.replace("{random}", RandomChar(
            random_list[0], random_list[1]) + ".")
    else:
        url = url.replace("{random}", "")
    # 组装瓦片坐标
    url = url.replace("{x}", str(x))
    url = url.replace("{y}", str(y))
    url = url.replace("{z}", str(z))
    # 组装Retina分辨率 优先最大分辨率
    if TILE_SERVER[tile_name][3][0] != "":
        url = url.replace(
            "{retina}", "@" + TILE_SERVER[tile_name][3][len(TILE_SERVER[tile_name][3]) - 1] + "x")
    else:
        url = url.replace("{retina}", "")
    # 组装APIKEY
    if TILE_SERVER[tile_name][4] != "":
        url = url.replace("{apikey}", TILE_SERVER[tile_name][4])
    else:
        url = url.replace("{apikey}", "")
    return url


class singleTileTask(threading.Thread):
    # DEFAULT
    x = -1
    y = -1
    z = -1
    tile_name = "OSMChina"
    task_name = "singleTileTask"
    threadID = 0

    # INIT
    def __init__(self, x: int, y: int, z: int, tile_name: str, task_name: str, threadID: int):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.tile_name = tile_name
        self.task_name = task_name
        self.threadID = threadID

    def run(self):
        try:
            url = fullURL(self.x, self.y, self.z, self.tile_name)
            img = requests.get(url, headers=headers)
            filename = str(self.y) + ".png"
            with open(filename, "wb") as f:
                f.write(img.content)
            if img.status_code == 200:
                print("[Thread " + str(self.threadID) + "][+] " + url)
            else:
                print("[Thread " + str(self.threadID) + "][-] " + url)
        except Exception as e:
            print(e)
        exit(0)


def atomicTask(x: int, y: int, z: int, tile_name: str):
    url = fullURL(x, y, z, tile_name)
    img = requests.get(url=url, headers=headers)
    filename = str(y) + ".png"
    with open(filename, "wb") as f:
        f.write(img.content)
    print("[Thread 0][*] " + url)


def multipleTask(x_min, x_max, y_min, y_max, z, tile_name, task_name, ALLOW_MP=False):
    x_max += 1
    y_max += 1
    os.mkdir(task_name)
    os.chdir(task_name)

    time_start = time.time()

    # TASKBODY
    for x in range(x_min, x_max):
        os.mkdir(str(x))
        os.chdir(str(x))
        if ALLOW_MP == False:
            for y in range(y_min, y_max):
                atomicTask(x, y, z, tile_name)
        else:
            MAX_CONNECTION = 16
            MIN_CONNECTION = 1
            SEMAPHORE_POOL = threading.BoundedSemaphore(MAX_CONNECTION)
            QUEUE = []
            for i in range(y_min, y_max):
                QUEUE.append(i)
            for y in range(y_min, y_max):
                tmp = singleTileTask(x, y, z, tile_name, task_name, y)
                tmp.start()
                tmp.join()
                delay = 0.05
                time.sleep(delay)
        os.chdir("..")
    os.chdir("..")

    time_end = time.time()
    print("[TIME] " + task_name + ": " + str(time_end - time_start) + "s")


def taskGenerator(zoom: int, tile_name, task_name, x_min=0, x_max=0, y_min=0, y_max=0,
                  grid_pos=(0, 0), MODE="Region", ALLOW_MP=False):
    # INIT
    global WHITE_LIST
    global TILE_SERVER
    headers["User-Agent"] = UA()
    if platform.system() == "Windows":
        WHITE_LIST = json.loads(open('..\\Res\\control_list.json').read())[
            'WHITE_LIST']
        TILE_SERVER = json.loads(open('..\\Res\\tile_server.json').read())
    else:
        WHITE_LIST = json.loads(
            open('../Res/control_list.json').read())['WHITE_LIST']
        TILE_SERVER = json.loads(open('../Res/tile_server.json').read())
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
            multipleTask(x_min, x_max, y_min, y_max, zoom,
                         tile_name, task_name, ALLOW_MP)
    elif MODE == "Full":
        if zoom == 0:
            count = 1
            print("Total tiles:", count)
            multipleTask(0, 0, 0, 0, 0, tile_name, task_name)
        else:
            count = pow(2, zoom * 2)
            print("Total tiles:", count)
            multipleTask(0, pow(2, zoom) - 1, 0, pow(2, zoom) -
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
