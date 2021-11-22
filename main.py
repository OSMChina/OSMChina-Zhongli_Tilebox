import os

from Src.Requester import taskGenerator

if __name__ == "__main__":
    TASK_MODE = "Debug"
    # Suggested TASK_MODE: Backup, Debug, Development,PressureTest
    os.system("mkdir OSMChina_" + TASK_MODE)
    os.chdir("OSMChina_" + TASK_MODE)
    LOW_ZOOM = 8
    HIGH_ZOOM = 8
    for i in range(LOW_ZOOM, HIGH_ZOOM + 1):
        taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), MODE="Full", ALLOW_MP=True)
        # # ���Բ��Ϊ���ɸ���ͬ�������񣬿��Կ�����main��������taskGenerator�п�������Grid������ģʽ���ֲ�ȫ���ǣ����һ���ʾ�����Grid���֣����߿���ָ�����صڼ���Grid
        # taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), x_min=27, x_max=27, y_min=0, y_max=63,
        #               MODE="Region", ALLOW_MP=True)
        # taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), x_min=64,x_max=127,y_min=0,y_max=63,MODE="Region", ALLOW_MP=True)
        # taskGenerator(i, "OSMChina", "OSMChina_" + TASK_MODE + "_" + str(i), x_min=128,x_max=191,y_min=0,y_max=63,MODE="Region", ALLOW_MP=True)