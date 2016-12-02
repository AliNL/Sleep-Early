# coding=utf-8
import time
from support import log


@log("继续")
def continue_(task, times=4):
    for t in range(times):
        task.d.click(*task.position['screen_bottom'])
        time.sleep(1.5)
    return True
