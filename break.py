#!/usr/bin/env python
from function import *
import sys
import getopt


def main(argv):
    time_ = 24
    level = 7
    target = 1
    device = 'android'

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
