# coding=utf-8

from base_window import Window


class Pipeline(Window):
    MAX_COLUMN = 6
    TICK = "\u2714"
    CROSS = "\u2716"
    GOING = "\u25B6"

    def __init__(self, status_list):
        super().__init__()
        self.app.setGeom(None)

        self.app.setPadding([10, 0])
        self.times_done = 0
        self.status_list = status_list
        self.set_pipeline()

    def stop_task(self):
        pass

    def set_pipeline(self):

        row = 0
        column = 0
        total = 0
        for name in self.status_list:
            self.app.addLabel(name, name, row, column, 1)
            self.app.setLabelSticky(name, "s")
            self.app.addMessage(name, " ", row + 1, column, 1)
            self.app.setMessageBg(name, "gray")
            self.app.setMessageFg(name, "white")
            self.app.setMessageSticky(name, "n")
            self.app.setMessagePadding(name, [60, 0])
            column += 1
            total = column
            if column >= self.MAX_COLUMN:
                total = self.MAX_COLUMN
                row += 2
                column = 0

        self.app.addLabel("times", "已刷了" + str(self.times_done) + "次", row + 1, total - 2, 2)
        self.app.addButton("停止并返回", self.stop_task, row + 1, 0, 2)
        self.app.setButtonSticky("停止并返回", "")

    def update_pipeline(self, status):
        previous = True
        for name in self.status_list:
            if name == status:
                self.set_in_progress(name)
                previous = False
            else:
                if previous:
                    self.set_done(name)
                else:
                    self.set_ready(name)

    def set_in_progress(self, name):
        self.app.setMessageBg(name, "orange")
        self.app.setMessage(name, self.GOING)

    def set_done(self, name):
        self.app.setMessageBg(name, "green")
        self.app.setMessage(name, self.TICK)

    def set_ready(self, name):
        self.app.setMessageBg(name, "gray")
        self.app.setMessage(name, " ")

    def set_fail(self, name):
        self.app.setMessageBg(name, "red")
        self.app.setMessage(name, self.CROSS)
