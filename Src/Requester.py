import os
import random
import requests

import threading
import time

WHITE_LIST = [
    "osmchina.org"
]

TILE_SERVER = {
    "OSMChina": ["{protocol}{random}tile.osmchina.org/{z}/{x}/{y}{retina}.png{apikey}",
                 ["https", "http"],  # {protocol}
                 "",  # {random}
                 [""],  # {retina}
                 ""  # {apikey}
                 ],
    "Teacestrack": ["{protocol}{random}tile.tracestrack.org/{z}/{x}/{y}{retina}.png{apikey}",
                    ["https", "http"],  # {protocol}
                    "a-c",  # {random}
                    ["1.0", "1.5", "2.0"],  # {retina}
                    "?apikey=9f8f8f8f-9f8f-9f8f-9f8f-9f8f8f8f8f8"  # {apikey}
                    ]
}

headers = {
    "User-Agent": "OSMChina-TileRequest/0.3.0",
    "Cookie": "",
}


def RandomChar(begin: str, end: str):
    Range = int(ord(end) - ord(begin))
    tmp = random.randint(0, Range - 1)
    return chr(ord(begin) + tmp)


def fullURL(x: int, y: int, z: int, tile_name):
    # PREFIX
    PROTOCOL_PREFIX_HTTPS = "https://"
    PROTOCOL_PREFIX_HTTP = "http://"
    PROTOCOL_PREFIX_FTP = "ftp://"
    # ��ʼ��װ׼��
    URL = TILE_SERVER[tile_name][0]
    # ���URL�Ƿ�Ϸ�
    for i in WHITE_LIST:
        if i in URL:
            break
    else:
        print("Error: Not OSMChina tile service!")
    # �����滻Ԥ����
    Protocol_list = TILE_SERVER[tile_name][1]
    if TILE_SERVER[tile_name][2] != "":
        Random_list = [TILE_SERVER[tile_name][2].split("-")[0], TILE_SERVER[tile_name][2].split("-")[1]]
    else:
        Random_list = ""
    # ��װЭ��
    if Protocol_list[0] == "https":
        URL = URL.replace("{protocol}", PROTOCOL_PREFIX_HTTPS)
    elif Protocol_list[0] == "ftp":
        URL = URL.replace("{protocol}", PROTOCOL_PREFIX_FTP)
    else:
        URL = URL.replace("{protocol}", PROTOCOL_PREFIX_HTTP)
    # ��װ���ؾ���
    if Random_list != "":
        URL = URL.replace("{random}", RandomChar(Random_list[0], Random_list[1]) + ".")
    else:
        URL = URL.replace("{random}", "")
    # ��װ��Ƭ����
    URL = URL.replace("{x}", str(x))
    URL = URL.replace("{y}", str(y))
    URL = URL.replace("{z}", str(z))
    # ��װRetina�ֱ��� �������ֱ���
    if TILE_SERVER[tile_name][3][0] != "":
        URL = URL.replace("{retina}", "@" + TILE_SERVER[tile_name][3][len(TILE_SERVER[tile_name][3]) - 1] + "x")
    else:
        URL = URL.replace("{retina}", "")
    # ��װAPIKEY
    if TILE_SERVER[tile_name][4] != "":
        URL = URL.replace("{apikey}", TILE_SERVER[tile_name][4])
    else:
        URL = URL.replace("{apikey}", "")
    return URL


class singleTileTask(threading.Thread):
    # DEFAULT
    x = -1
    y = -1
    z = -1
    tile_name = "OSMChina"
    threadID = 0

    # INIT
    def __init__(self, x: int, y: int, z: int, tile_name: str, threadID: int):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.tile_name = tile_name
        self.threadID = threadID

    def run(self):
        # ��ʼ���� �������ȫ��copilot�ɵĺ���
        try:
            URL = fullURL(self.x, self.y, self.z, self.tile_name)
            IMG = requests.get(URL, headers=headers)
            filename = str(self.y) + ".png"
            with open(filename, "wb") as f:
                f.write(IMG.content)
            if IMG.status_code == 200:
                print("[Thread " + str(self.threadID) + "][+] " + URL)
            else:
                print("[Thread " + str(self.threadID) + "][-] " + URL)
        except Exception as e:
            print(e)
        exit(0)


def atomicTask(x: int, y: int, z: int, tile_name: str):
    TaskURL = fullURL(x, y, z, tile_name)
    img = requests.get(url=TaskURL, headers=headers)
    filename = str(y) + ".png"
    with open(filename, "wb") as f:
        f.write(img.content)
    print("[Thread 0][*] " + TaskURL)


def multipleTask(x_min, x_max, y_min, y_max, z, tile_name, task_name, ALLOW_MP=False):
    x_max += 1
    y_max += 1
    os.system("mkdir " + task_name)
    os.chdir(task_name)

    TIME_START = time.time()

    # TASKBODY
    for x in range(x_min, x_max):
        os.system("mkdir " + str(x))
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
                tmp = singleTileTask(x, y, z, tile_name, y)
                tmp.start()
                tmp.join()
        os.chdir("..")
    os.chdir("..")

    TIME_END = time.time()
    print("[TIME] " + task_name + ": " + str(TIME_END - TIME_START) + "s")


def taskGenerator(zoom, tile_name, task_name, x_min=0, x_max=0, y_min=0, y_max=0, MODE="Region", ALLOW_MP=False):
    if MODE == "Region":
        if zoom == 0:
            print("Error: zoom must be greater than 0 in Region MODE")
        else:
            if x_min == 0 and x_max == 0 and y_min == 0 and y_max == 0:
                x_min = int(input("Please input x_min:"))
                x_max = int(input("Please input x_max:"))
                y_min = int(input("Please input y_min:"))
                y_max = int(input("Please input y_max:"))
            Count = (x_max - x_min + 1) * (y_max - y_min + 1)
            print("Total tiles:", Count)
            multipleTask(x_min, x_max, y_min, y_max, zoom, tile_name, task_name, ALLOW_MP)
    elif MODE == "Full":
        if zoom == 0:
            Count = 1
            print("Total tiles:", Count)
            multipleTask(0, 0, 0, 0, 0, tile_name, task_name)
        else:
            Count = pow(2, zoom * 2)
            print("Total tiles:", Count)
            multipleTask(0, pow(2, zoom) - 1, 0, pow(2, zoom) - 1, zoom, tile_name, task_name, ALLOW_MP)
    else:
        print("Error: MODE Error")
