#!/usr/bin/env python
from function import *
import sys
import getopt


def main(argv):
    times = 0
    level = 0
    device = ''

    try:
        opts, args = getopt.getopt(argv, "ht:l:d:", ["times=", "level=", "device="])
    except getopt.GetoptError:
        print 'Please input: python break.py -t <times>(int) -l <level/10>(0<int<8) -d <device>(android or ios)'
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print 'Please input: python break.py -t <times>(int) -l <level/10>(0<int<8) -d <device>(android or ios)'
            sys.exit()
        elif opt in ("-t", "--times"):
            times = int(arg)
        elif opt in ("-l", "--level"):
            level = int(arg)
        elif opt in ("-d", "--device"):
            device = arg

    task = Break(times, level, device)

    task.breaking()


if __name__ == "__main__":
    main(sys.argv[1:])
