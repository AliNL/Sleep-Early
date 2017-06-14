# coding=utf-8
import time

from pages.base_window import Window


class Pipeline(Window):
    MAX_COLUMN = 6
    READY = "images/Gray_pipeline.gif"
    GOING = "images/Yellow_pipeline.gif"
    PENDING = "images/Blue_pipeline.gif"
    FAIL = "images/Red_pipeline.gif"
    PASS = "images/Green_pipeline.gif"

    def __init__(self, status_list):
        super().__init__()
        self.app.setResizable(canResize=False)
        self.app.setPadding([10, 0])
        self.app.setInPadding([1, 1])
        self.app.setSticky("nsew")
        self.app.setStretch("none")
        self.times_done = 0
        self.status_list = status_list
        self.status = {}
        self.task_running = None
        self.current = status_list[0]
        self.task = None

    def run_task(self):
        pass

    def kill(self):
        self.task.d = None

    def stop_task(self, btn):
        self.app.stop()
        self.kill()
        from pages.task_choose import TaskChoose
        TaskChoose().choose_task()

    def set_pipeline(self, task_running):
        self.task_running = task_running
        row = 0
        column = 0
        total = 0
        for name in self.status_list:
            if column >= self.MAX_COLUMN:
                total = self.MAX_COLUMN
                row += 3
                column = 0
            self.app.addLabel(name + "Label", name, row, column, 1)
            self.app.addImage(name, self.READY, row + 1, column, 1)
            self.app.addLabel(name, "", row + 2, column, 1)
            column += 1
        if total == 0:
            total = column
        self.app.addLabel("times", "已刷了" + str(self.times_done) + "次", row + 3, total - 2, 2)
        self.app.addButton("停止并返回", self.stop_task, row + 3, 0, 2)
        self.app.setButtonSticky("停止并返回", "")
        self.app.registerEvent(self.update_pipeline)
        self.app.setPollTime(500)
        self.app.go()

    def update_pipeline(self):
        self.app.setLabel("times", "已刷了" + str(self.times_done) + "次")
        if not self.task_running.isAlive():
            self.set_status(self.current, "fail")
            return
        for name in self.status:
            self.set_status(name, self.status[name])

    def set_status(self, name, value):
        if isinstance(value, int):
            if value == 0:
                self.app.setImage(name, self.READY)
                self.app.setLabel(name, "")
            elif time.time() + 1 < value:
                self.app.setImage(name, self.PENDING)
                pending = str(int(value - time.time()))
                self.app.setLabel(name, pending + " 秒后")
            elif time.time() - 1 > value:
                self.current = name
                self.app.setImage(name, self.GOING)
                pending = str(int(60 - time.time() + value))
                self.app.setLabel(name, "剩余 " + pending + " 秒")
            else:
                self.status[name] = 0
        elif value == "going":
            self.current = name
            self.app.setImage(name, self.GOING)
            self.app.setLabel(name, "")
        elif value == "ready":
            self.app.setImage(name, self.READY)
            self.app.setLabel(name, "")
        elif value == "pass":
            self.app.setImage(name, self.PASS)
            self.app.setLabel(name, "")
        elif value == "fail":
            self.app.setImage(name, self.FAIL)
            self.app.setLabel(name, "任务出错")
        else:
            self.app.setImage(name, self.PENDING)
            self.app.setLabel(name, "")
