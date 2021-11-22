import os
import time
import threading

from Src.Requester import taskGenerator

if __name__ == "__main__":
    TASK_MODE = "Development"
    # Suggested TASK_MODE: Backup, Debug, Development,PressureTest
    os.system("mkdir OSMChina_" + TASK_MODE)
    os.chdir("OSMChina_" + TASK_MODE)
    LOW_ZOOM = 8
    HIGH_ZOOM = 8
    for i in range(LOW_ZOOM, HIGH_ZOOM + 1):
        # 尝试拆分为若干个不同的子任务，可以考虑在main函数或者taskGenerator中考虑引入Grid这样的模式，局部全覆盖，并且会提示建议的Grid划分，或者可以指定下载第几个Grid
        # HEADER可以改进为更丰富的UA，并且数据可以预分离出来在json里面
        taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), x_min=0,x_max=63,y_min=0,y_max=63,MODE="Region", ALLOW_MP=True)
        # taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), x_min=64,x_max=127,y_min=0,y_max=63,MODE="Region", ALLOW_MP=True)
        #　taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), x_min=128,x_max=191,y_min=0,y_max=63,MODE="Region", ALLOW_MP=True)
