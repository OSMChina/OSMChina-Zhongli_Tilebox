import os
import random
import threading
import time

import requests

from src.main import TILE_SERVER
from src.main import WHITE_LIST


def get_random_char(begin: str, end: str):
    char_range = int(ord(end) - ord(begin))
    tmp = random.randint(0, char_range - 1)
    return chr(ord(begin) + tmp)


def full_url(x: int, y: int, z: int, tile_name):
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
        random_list = [
            TILE_SERVER[tile_name][2].split("-")[0],
            TILE_SERVER[tile_name][2].split("-")[1],
        ]
    else:
        random_list = ""
    # 组装协议
    if protocol_list[0] == "https":
        url = url.replace("{protocol}", "https://")
    elif protocol_list[0] == "ftp":
        url = url.replace("{protocol}", "http://")
    else:
        url = url.replace("{protocol}", "ftp://")
    # 组装负载均衡
    if random_list != "":
        url = url.replace(
            "{random}", get_random_char(random_list[0], random_list[1]) + "."
        )
    else:
        url = url.replace("{random}", "")
    # 组装瓦片坐标
    url = url.replace("{x}", str(x))
    url = url.replace("{y}", str(y))
    url = url.replace("{z}", str(z))
    # 组装Retina分辨率 优先最大分辨率
    if TILE_SERVER[tile_name][3][0] != "":
        url = url.replace(
            "{retina}",
            "@"
            + TILE_SERVER[tile_name][3][len(TILE_SERVER[tile_name][3]) - 1]
            + "x",
        )
    else:
        url = url.replace("{retina}", "")
    # 组装APIKEY
    if TILE_SERVER[tile_name][4] != "":
        url = url.replace("{apikey}", TILE_SERVER[tile_name][4])
    else:
        url = url.replace("{apikey}", "")
    return url


class Requester_Action_Thread(threading.Thread):
    # DEFAULT
    x = -1
    y = -1
    z = -1
    tile_name = "OSMChina"
    thread_id = 0
    headers = {}

    # INIT
    def __init__(
        self,
        x: int,
        y: int,
        z: int,
        tile_name: str,
        thread_id: int,
        headers: dict,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.tile_name = tile_name
        self.thread_id = thread_id
        self.headers = headers

    def run(self):
        try:
            url = full_url(self.x, self.y, self.z, self.tile_name)
            img = requests.get(url, headers=self.headers)
            filename = str(self.y) + ".png"
            with open(filename, "wb") as f:
                f.write(img.content)
            if img.status_code == 200:
                print("[Thread " + str(self.thread_id) + "][+] " + url)
            else:
                print("[Thread " + str(self.thread_id) + "][-] " + url)
        except Exception as e:
            print(e)
        exit(0)


def requester_action_single(x: int, y: int, z: int, headers, tile_name: str):
    url = full_url(x, y, z, tile_name)
    img = requests.get(url=url, headers=headers)
    filename = str(y) + ".png"
    with open(filename, "wb") as f:
        f.write(img.content)
    print("[Thread 0][*] " + url)


def requester_task(
    x_min,
    x_max,
    y_min,
    y_max,
    z,
    tile_name,
    task_name,
    headers,
    allow_multi_processor=False,
):
    x_max += 1
    y_max += 1
    os.mkdir(task_name)
    os.chdir(task_name)

    time_start = time.time()

    # TASK_BODY
    for x in range(x_min, x_max):
        os.mkdir(str(x))
        os.chdir(str(x))
        if allow_multi_processor is False:
            for y in range(y_min, y_max):
                requester_action_single(x, y, z, tile_name, headers)
        else:
            # MAX_CONNECTION = 16
            # MIN_CONNECTION = 1
            # SEMAPHORE_POOL = threading.BoundedSemaphore(MAX_CONNECTION)
            # QUEUE = []
            # for i in range(y_min, y_max):
            #     QUEUE.append(i)
            for y in range(y_min, y_max):
                tmp = Requester_Action_Thread(
                    x, y, z, tile_name, thread_id=y, headers=headers
                )
                tmp.start()
                tmp.join()
                delay = 0.05
                time.sleep(delay)
        os.chdir("..")
    os.chdir("..")

    time_end = time.time()
    print("[TIME] " + task_name + ": " + str(time_end - time_start) + "s")