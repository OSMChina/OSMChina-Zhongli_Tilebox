import os
import random
import threading
import time

import requests

from config import TILE_SERVER
from config import WHITE_LIST

def no_proxy():
    domain="osmchina.org"
    # If meet with this Error like this:
    # requests.exceptions.SSLError: HTTPSConnectionPool(host='https://domain', port=443): Max retries exceeded with url:
    # (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:997)')))
    os.environ['NO_PROXY']= domain


def get_random_char(begin: str, end: str):
    char_range = int(ord(end) - ord(begin))
    tmp = random.randint(0, char_range - 1)
    return chr(ord(begin) + tmp)


def url_generator(x: int, y: int, z: int, tile_name: str):
    # URL
    url = TILE_SERVER[tile_name]["url"]
    # URL_WHITE_LIST
    for i in WHITE_LIST:
        if i in url:
            break
    else:
        print("Error: Not OSMChina tile service!")
    # PARAMETER
    parameter = TILE_SERVER[tile_name]["parameter"]
    # {protocol} - Mandatory
    if parameter["protocol"][0] == "https":
        url = url.format(protocol="https://")
    elif parameter["protocol"][0] == "ftp":
        url = url.format(protocol="ftp://")
    else:
        url = url.format(protocol="http://")
    # {random} - Optional
    if "random" in parameter:
        random_list = [
            parameter["random"].split("-")[0],
            parameter["random"].split("-")[1],
        ]
        url = url.format(
            random=get_random_char(random_list[0], random_list[1]) + "."
        )
    else:
        pass
    # {retina} - Optional
    if "retina" in parameter:
        # Highest resolution prefer
        url = url.format(
            retina="@" + parameter["retina"][len(parameter["retina"]) - 1] + "x",
        )
    # {apikey} - Optional
    if "apikey" in parameter:
        url = url.format(apikey=parameter["apikey"])
    # {x} - Mandatory
    url = url.format(x=str(x))
    # {y} - Mandatory
    url = url.format(y=str(y))
    # {z} - Mandatory
    url = url.format(z=str(z))
    return url


def status_rebuilder(z: int,task_name:str):
    # INIT
    status_matrix = [[-1] * pow(2, z) for i in range(pow(2, z))]
    # FIND
    try:
        os.chdir(task_name)
    except FileNotFoundError:
        # ??????????????????????????????0
        os.mkdir(task_name)
        os.chdir(task_name)
        for i in range(pow(2, z)):
            for j in range(pow(2, z)):
                status_matrix[i][j] = 0
        # SAVE(EMPTY)
        status_file = open(task_name + ".status", "w")
        for i in range(pow(2, z)):
            for j in range(pow(2, z)):
                status_file.write(str(status_matrix[i][j]) + " ")
            status_file.write("\n")
        status_file.close()
        os.chdir("..")
        return
    for x in range(pow(2,z)):
        if os.path.exists(str(x)):
            os.chdir(str(x))
        else:
            # ?????????x??????????????????0
            for i in range(pow(2,z)):
                status_matrix[x][i] = 0
            continue
        for y in range(pow(2,z)):
            if os.path.exists(str(y) + ".png"):
                status_matrix[x][y] = 1
            else:
                # ?????????????????????????????????0
                status_matrix[x][y] = 0
        os.chdir("..")
    # SAVE
    status_file = open(task_name + ".status", "w")
    for i in range(pow(2, z)):
        for j in range(pow(2, z)):
            status_file.write(str(status_matrix[i][j]) + " ")
        status_file.write("\n")
    status_file.close()
    os.chdir("..")
    return





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
            url = url_generator(self.x, self.y, self.z, self.tile_name)
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


def requester_action_single(
    x: int, y: int, z: int, tile_name: str, headers: dict
):
    url = url_generator(x, y, z, tile_name)
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
    try:
        os.mkdir(task_name)
    except FileExistsError:
        pass
    os.chdir(task_name)

    time_start = time.time()

    # TASK_STATUS
    if z > 0:
        # import status
        # temp=Status("-1")
        status_matrix = [[-1] * pow(2, z) for i in range(pow(2, z))]
        # status_matrix=[[temp] * pow(2, z) for i in range( pow(2, z))]
    else:
        status_matrix = [[-1]]
    if os.path.exists(task_name + ".status") is not True:
        status_file = open(task_name + ".status", "w")
        for i in range(pow(2, z)):
            for j in range(pow(2, z)):
                status_file.write(str(status_matrix[i][j]) + " ")
            status_file.write("\n")
    else:
        status_file = open(task_name + ".status", "r")
        for i in range(pow(2, z)):
            status_line = status_file.readline().split(" ")
            for j in range(pow(2, z)):
                status_matrix[i][j] = int(status_line[j])

    # TASK_BODY
    for x in range(x_min, x_max):
        try:
            os.mkdir(str(x))
        except FileExistsError:
            pass
        os.chdir(str(x))
        for y in range(y_min, y_max):
            if allow_multi_processor is False:
                if status_matrix[x][y] == 1:
                    continue
                else:
                    requester_action_single(x, y, z, tile_name, headers)
            else:
                # MAX_CONNECTION = 16
                # MIN_CONNECTION = 1
                # SEMAPHORE_POOL = threading.BoundedSemaphore(MAX_CONNECTION)
                # QUEUE = []
                # for i in range(y_min, y_max):
                #     QUEUE.append(i)
                if status_matrix[x][y] == 1:
                    continue
                else:
                    tmp = Requester_Action_Thread(
                        x, y, z, tile_name, thread_id=y, headers=headers
                    )
                    tmp.start()
                    tmp.join()
                    delay = 0.05
                    time.sleep(delay)
            # ???????????????????????????????????????????????????
            if status_matrix[x][y] != 1:
                status_matrix[x][y] = 1
        os.chdir("..")

        # ?????????IO????????????x??????????????????????????????status
        # ????????????????????????
        status_file.close()
        status_file = open(task_name + ".status", "w")
        for i in range(pow(2, z)):
            for j in range(pow(2, z)):
                status_file.write(str(status_matrix[i][j]) + " ")
            status_file.write("\n")
        status_file.close()

    os.chdir("..")

    time_end = time.time()
    print(
        "[TIME] " + task_name + ": " + str(time_end - time_start) + "s" + "\n"
    )
