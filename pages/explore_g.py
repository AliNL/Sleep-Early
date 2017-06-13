# coding=utf-8
import getopt
from xml.dom import minidom

from function import *


def main(argv):
    try:
        dom = minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        print('loading config from xml...')
    except IOError:
        device = 'android'
    finally:
        is_lead = False

    task = ExploreG(device)

    while True:
        if is_lead:
            task.exploring_fight(3)
            task.get_small_box()
            time.sleep(10)
            click_ok(task.d)
        else:
            task.exploring_wait()
            task.get_small_box()
            task.get_big_box()
            if not click_get(task.d):
                break
        task.analysis()


if __name__ == "__main__":
    main(sys.argv[1:])
