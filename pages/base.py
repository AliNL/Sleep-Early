import time

import atx

from pages import Position


class BasePage(object):
    def __init__(self, driver=None, chapter=None, level=None, position=None, delay=0):
        if driver:
            self.d = driver
            self.chapter = chapter
            self.level = level
            self.position = position
            self.delay = delay
        else:
            self.__init__(*self.setup())
        self.d.image_match_threshold = 0.9

    @staticmethod
    def setup():
        from launcher import DATA_PATH
        from xml.dom import minidom
        dom = minidom.parse(DATA_PATH + 'config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        chapter = int(root.getElementsByTagName('chapter')[0].firstChild.data)
        level = int(root.getElementsByTagName('level')[0].firstChild.data)
        if device == 'android':
            driver = atx.connect(platform='android')
            delay = 0.8
        elif device == 'ios':
            driver = atx.connect('http://localhost:8100', platform='ios')
            delay = 0
        else:
            raise IOError('Invalid device type!!!')
        atx.drivers.mixin.log.setLevel(50)
        return driver, chapter, level, Position(driver), delay

    def get_info(self):
        return self.d, self.chapter, self.level, self.position

    def click_by_times(self, times=4):
        for t in range(times):
            self.d.click(*self.position['screen_bottom'])
            time.sleep(1 + self.delay)

    def wait_with_delay(self, seconds):
        time.sleep(seconds + self.delay)

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)
