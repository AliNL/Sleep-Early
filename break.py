#!/usr/bin/env python
from function import *
import sys
import getopt
import xml.dom.minidom


def main(argv):
    try:
        dom = xml.dom.minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        level = int(root.getElementsByTagName('level')[0].firstChild.data)
        print('loading config from xml...')
    except Exception:
        device = 'android'
        level = 7
    finally:
        time_ = 24
        target = 1

    try:
        opts, args = getopt.getopt(argv, "ht:l:d:a:", ["times=", "level=", "device=", "target="])
    except getopt.GetoptError:
        print('-d\tdevice: ios/android\tdefault: android')
        print('-l\tlevel: 1~7\tdefault: 7')
        print('-t\ttime: float(hours)\tdefault: 24')
        print('-a\tfirst target: 1~3\tdefault: 1')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('-d\tdevice: ios/android\tdefault: android')
            print('-l\tlevel: 1~7\tdefault: 7')
            print('-t\ttime: float(hours)\tdefault: 24')
            print('-a\tfirst target: 1~3\tdefault: 1')
            sys.exit()
        elif opt in ("-t", "--time"):
            time_ = float(arg)
        elif opt in ("-l", "--level"):
            level = int(arg)
        elif opt in ("-a", "--target"):
            target = int(arg)
        elif opt in ("-d", "--device"):
            device = arg

    task = Break(time_, level, target, device)

    task.breaking()


if __name__ == "__main__":
    main(sys.argv[1:])
