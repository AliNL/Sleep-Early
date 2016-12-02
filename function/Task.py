# coding=utf-8
from steps import *


class Task(object):
    def __init__(self, driver):
        self.d = driver
        self.times = 0
        self.position = Position(driver)
        self.start_time = now()

    def analysis(self):
        print 'task "%s" finished' % self.__class__
        print 'start time:\t%s' % self.start_time
        print 'finish time:\t%s' % now()
        print 'times:\t%s' % self.times
