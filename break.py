#!/usr/bin/env python
from function import *
import sys
import getopt


def main(argv):
    time_ = 0
    level = 0
    target = 0
    device = ''

    try:
        opts, args = getopt.getopt(argv, "ht:l:d:a:", ["times=", "level=", "device=", "target="])
    except getopt.GetoptError:
        print 'Please input: python break.py -d <device> -t <hours> -l <level/10> -a <target>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print 'Please input: python break.py -d <device> -t <hours> -l <level/10> -a <target>'
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
