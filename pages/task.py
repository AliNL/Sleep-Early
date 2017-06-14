# coding=utf-8
import atx

from .steps import *


class Task(object):
    def launch(self, device):
        if device == 'android':
            driver = atx.connect()
            set_delay(0.8)
        elif device == 'ios':
            driver = atx.connect('http://localhost:8100')
        else:
            raise IOError('Invalid device type!!!')
        atx.drivers.mixin.log.setLevel(50)
        return driver

    def __init__(self, device):
        self.d = self.launch(device)
        self.name = 'task'
        self.times = 0
        self.position = Position(self.d)
        self.start_time = now()
        self.stop_reason = 'task completed'

    def analysis(self):
        print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
        print('┃ %-49s┃' % (self.name + ' finished!!!'))
        print('┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫')
        print('┃%25s%-25s┃' % ('start time: ', self.start_time))
        print('┃%25s%-25s┃' % ('finish time: ', now()))
        print('┃%25s%-25s┃' % ('times: ', self.times))
        print('┃%25s%-25s┃' % ('stop reason: ', self.stop_reason))
