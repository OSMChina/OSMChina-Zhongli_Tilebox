import os
import platform

from Zhongli_Tilebox.requester import requester_task
from Zhongli_Tilebox.requester import status_rebuilder
from Zhongli_Tilebox.combiner import combiner_task
from Zhongli_Tilebox.viewer import viewer_task

headers = {
    "User-Agent": "OSMChina-TileRequest/0.3.0",
    "Cookie": "",
}


def useragent_generator():
    PROGRAMME_NAME = "OSMChina-TileRequest"
    PROGRAMME_VERSION = "0.3.0"
    PLATFORM_SYSTEM = platform.system()
    PLATFORM_VERSION = platform.version()
    PLATFORM_MACHINE = platform.machine()
    PLATFORM_PYTHON = platform.python_version()
    UA_BASIC = PROGRAMME_NAME + "/" + PROGRAMME_VERSION
    UA_EXTEND = (
        "("
        + PLATFORM_SYSTEM
        + " "
        + PLATFORM_VERSION
        + "; "
        + PLATFORM_MACHINE
        + "; "
        + ")"
        + " Python/"
        + PLATFORM_PYTHON
    )
    return UA_BASIC + " " + UA_EXTEND


def task_generator(
    task: str,
    zoom: int,
    tile_name: str,
    task_name: str,
    x_min=0,
    x_max=0,
    y_min=0,
    y_max=0,
    grid_pos_x=0,
    grid_pos_y=0,
    mode="Region",
    allow_multi_processor=False,
):
    # INIT
    headers["User-Agent"] = useragent_generator()
    # TASK_CHOISE
    if task == "requester":
        # REQUESTER_TASK
        if mode == "Region":
            if zoom == 0:
                count = 1
                print("Total tiles:", count)
                requester_task(
                    x_min=0,
                    x_max=0,
                    y_min=0,
                    y_max=0,
                    z=0,
                    tile_name=tile_name,
                    task_name=task_name,
                    headers=headers,
                    allow_multi_processor=allow_multi_processor,
                )
            else:
                if x_min == 0 and x_max == 0 and y_min == 0 and y_max == 0:
                    x_min = int(input("Please input x_min:"))
                    x_max = int(input("Please input x_max:"))
                    y_min = int(input("Please input y_min:"))
                    y_max = int(input("Please input y_max:"))
                count = (x_max - x_min + 1) * (y_max - y_min + 1)
                print("Total tiles:", count)
                requester_task(
                    x_min=x_min,
                    x_max=x_max,
                    y_min=y_min,
                    y_max=y_max,
                    z=zoom,
                    tile_name=tile_name,
                    task_name=task_name,
                    headers=headers,
                    allow_multi_processor=allow_multi_processor,
                )
        elif mode == "Full":
            if zoom == 0:
                count = 1
                print("Total tiles:", count)
                requester_task(
                    x_min=0,
                    x_max=0,
                    y_min=0,
                    y_max=0,
                    z=0,
                    tile_name=tile_name,
                    task_name=task_name,
                    headers=headers,
                    allow_multi_processor=allow_multi_processor,
                )
            else:
                count = pow(2, zoom * 2)
                print("Total tiles:", count)
                requester_task(
                    x_min=0,
                    x_max=pow(2, zoom) - 1,
                    y_min=0,
                    y_max=pow(2, zoom) - 1,
                    z=zoom,
                    tile_name=tile_name,
                    task_name=task_name,
                    headers=headers,
                    allow_multi_processor=allow_multi_processor,
                )
        elif mode == "Grid":
            full_length = pow(2, zoom)
            full_count = pow(2, zoom * 2)
            print(grid_pos_x, grid_pos_y)
        else:
            print("Error: mode Error")
    elif task == "combiner":
        combiner_task()
    elif task == "viewer":
        viewer_task()
    elif task == "rebuild_status":
        status_rebuilder(
            z=zoom,
            task_name=task_name,
        )
    else:
        print("Task Error!")
        return


if __name__ == "__main__":
    TASK_MODE = "Debug"
    # Suggested TASK_MODE: Backup, Debug, Development,PressureTest
    try:
        os.mkdir("OSMChina_" + TASK_MODE)
    except FileExistsError:
        pass
    os.chdir("OSMChina_" + TASK_MODE)
    LOW_ZOOM = 0
    HIGH_ZOOM = 11
    for i in range(LOW_ZOOM, HIGH_ZOOM + 1):
        task_generator(
            task="requester",
            zoom=i,
            tile_name="OSMChina",
            task_name="OSMChina_" + TASK_MODE + "_" + str(i),
            mode="Full",
            allow_multi_processor=False,
        )
