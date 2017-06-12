# coding=utf-8

from appJar import gui

import task


class Config(object):
    TICK = "\u2714"
    CROSS = "\u2716"
    validation = {"device": "invalid", "chapter": "invalid", "level": "invalid"}
    level_list = {"全部": "7", "59级以下": "6", "49级以下": "5", "39级以下": "4",
                  "29级以下": "3", "19级以下": "2", "9级以下": "1"}

    def __init__(self):
        self.app = gui("护肝宝", "600x450")
        self.app.setFont(14)
        self.app.setGuiPadding(100, 20)
        self.app.setInPadding(20, 10)
        self.app.setSticky("ew")

    def set_valid(self, name):
        self.app.setMessage(name, self.TICK)
        self.app.setMessageFg(name, "green")
        self.validation[name] = "valid"

    def set_invalid(self, name, message=""):
        self.app.setMessage(name, self.CROSS + message)
        self.app.setMessageFg(name, "red")
        self.validation[name] = "invalid"

    def check_all_data(self):
        for key in self.validation:
            if self.validation[key] == "invalid":
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
        level = self.level_list[self.app.getOptionBox("level")]

        fl = open('config.xml', 'w')
        fl.write('<root>\n')
        fl.write('    <device>' + device + '</device>\n')
        fl.write('    <chapter>' + chapter + '</chapter>\n')
        fl.write('    <level>' + level + '</level>\n')
        fl.write('</root>')
        fl.close()
        self.app.stop()
        task.main()

    def start_config(self):
        self.app.addLabel("title", "请保存默认配置", 0, 0, 3)
        self.app.addLabel("device", "设备类型：", 1, 0)
        self.app.setLabelAlign("device", "right")
        self.app.addOptionBox("device", ["- 空 -", "android", "ios"], 1, 1)
        self.app.addEmptyMessage("device", 1, 2)
        self.app.addLabel("chapter", "常用章节：", 2, 0)
        self.app.setLabelAlign("chapter", "right")
        self.app.addOptionBox("chapter", ["- 空 -",
                                          "18", "17", "16", "15", "14", "13", "12", "11", "10", "9",
                                          "8", "7", "6", "5", "4", "3", "2", "1"], 2, 1)
        self.app.addEmptyMessage("chapter", 2, 2)
        self.app.addLabel("level", "突破等级：", 3, 0)
        self.app.setLabelAlign("level", "right")
        self.app.addOptionBox("level", ["- 空 -", "全部", "59级以下", "49级以下", "39级以下", "29级以下", "19级以下", "9级以下"], 3, 1)
        self.app.addEmptyMessage("level", 3, 2)

        self.app.addButton("确定", self.save_config, 4, 1, 1)
        self.app.disableButton("确定")

        self.set_invalid("device")
        self.set_invalid("chapter")
        self.set_invalid("level")
        self.app.setOptionBoxChangeFunction("device", self.check_device)
        self.app.setOptionBoxChangeFunction("chapter", self.check_target)
        self.app.setOptionBoxChangeFunction("level", self.check_target)

        self.app.go()
