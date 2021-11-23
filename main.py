import os

from Src.Requester import taskGenerator

if __name__ == "__main__":
    TASK_MODE = "Debug"
    # Suggested TASK_MODE: Backup, Debug, Development,PressureTest
    os.system("mkdir OSMChina_" + TASK_MODE)
    os.chdir("OSMChina_" + TASK_MODE)
    LOW_ZOOM = 0
    HIGH_ZOOM = 11
    for i in range(LOW_ZOOM, HIGH_ZOOM + 1):
        taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), MODE="Grid", ALLOW_MP=False)