# coding=utf-8

from base_window import Window
from task import TaskChoose


class Config(Window):
    TICK = "\u2714"
    CROSS = "\u2716"
    VALIDATION = {"device": "invalid", "chapter": "invalid", "level": "invalid"}
    LEVEL_LIST = {"全部": "7", "59级以下": "6", "49级以下": "5", "39级以下": "4",
                  "29级以下": "3", "19级以下": "2", "9级以下": "1"}

    def set_valid(self, name):
        self.app.setMessage(name, self.TICK)
        self.app.setMessageFg(name, "green")
        self.VALIDATION[name] = "valid"

    def set_invalid(self, name, message=""):
        self.app.setMessage(name, self.CROSS + message)
        self.app.setMessageFg(name, "red")
        self.VALIDATION[name] = "invalid"

    def check_all_data(self):
        for key in self.VALIDATION:
            if self.VALIDATION[key] == "invalid":
                return
        self.app.enableButton("确定")

    def check_device(self, name):
        if self.app.getOptionBox(name) == "android":
            self.set_valid(name)
        elif self.app.getOptionBox(name) == "ios":
            if self.app.GET_PLATFORM() == self.app.MAC:
                self.set_valid(name)
            else:
                self.set_invalid(name, " Windows 无法连接 ios")
        self.check_all_data()

    def check_target(self, name):
        self.set_valid(name)
        self.check_all_data()

    def save_config(self, btn):
        device = self.app.getOptionBox("device")
        chapter = self.app.getOptionBox("chapter")
        level = self.LEVEL_LIST[self.app.getOptionBox("level")]

        fl = open('config.xml', 'w')
        fl.write('<root>\n')
        fl.write('    <device>' + device + '</device>\n')
        fl.write('    <chapter>' + chapter + '</chapter>\n')
        fl.write('    <level>' + level + '</level>\n')
        fl.write('</root>')
        fl.close()
        self.app.stop()
        TaskChoose().choose_task()

    def start_config(self):
        self.app.addLabel("title", "请保存默认配置", 0, 0, 3)
        self.app.addLabel("device", "设备类型：", 1, 0)
        self.app.setLabelAlign("device", "right")
        self.app.addOptionBox("device", ["- 空 -", "android", "ios"], 1, 1)
        self.app.setOptionBoxAlign("device", "left")
        self.app.addEmptyMessage("device", 1, 2)
        self.app.setMessageAlign("device", "left")
        self.app.addLabel("chapter", "常用章节：", 2, 0)
        self.app.setLabelAlign("chapter", "right")
        self.app.addOptionBox("chapter", ["- 空 -",
                                          "18", "17", "16", "15", "14", "13", "12", "11", "10", "9",
                                          "8", "7", "6", "5", "4", "3", "2", "1"], 2, 1)
        self.app.setOptionBoxAlign("chapter", "left")
        self.app.addEmptyMessage("chapter", 2, 2)
        self.app.setMessageAlign("chapter", "left")
        self.app.addLabel("level", "突破等级：", 3, 0)
        self.app.setLabelAlign("level", "right")
        self.app.addOptionBox("level", ["- 空 -", "全部", "59级以下", "49级以下", "39级以下", "29级以下", "19级以下", "9级以下"], 3, 1)
        self.app.setOptionBoxAlign("level", "left")
        self.app.addEmptyMessage("level", 3, 2)
        self.app.setMessageAlign("level", "left")
        self.app.addButton("确定", self.save_config, 4, 0, 3)
        self.app.setButtonSticky("确定", "")
        self.app.disableButton("确定")

        self.set_invalid("device")
        self.set_invalid("chapter")
        self.set_invalid("level")
        self.app.setOptionBoxChangeFunction("device", self.check_device)
        self.app.setOptionBoxChangeFunction("chapter", self.check_target)
        self.app.setOptionBoxChangeFunction("level", self.check_target)

        self.app.go()
