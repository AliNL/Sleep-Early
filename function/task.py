# coding=utf-8
import atx
import wda
from steps import *


class Task(object):
    def launch(self):
        try:
            driver = atx.connect()
        except Exception:
            fl = open('session_id_ios')
            sid = fl.read()
            fl.close()
            driver = atx.connect('http://localhost:8100')
            driver._session = wda.Session('http://localhost:8100', sid)
        driver.image_path = ['.', 'images']
        return driver

    def __init__(self):
        self.d = self.launch()
        self.times = 0
        self.position = Position(self.d)
        self.start_time = now()
        self.stop_reason = 'task completed'

    def analysis(self):
        print '┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓'
        print '┃%-50s┃' % (str(self.__class__)[25:-2] + ' finished!!!')
        print '┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫'
        print '┃%25s%-25s┃' % ('start time: ', self.start_time)
        print '┃%25s%-25s┃' % ('finish time: ', now())
        print '┃%25s%-25s┃' % ('times: ', self.times)
        print '┃%25s%-25s┃' % ('stop reason: ', self.stop_reason)
