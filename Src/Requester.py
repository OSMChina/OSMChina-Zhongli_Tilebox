import os
import platform
import random
import threading
import time

import requests



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


def request_task(x_min, x_max, y_min, y_max, z, tile_name, task_name, ALLOW_MP=False):
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