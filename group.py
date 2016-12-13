#!/usr/local/bin/ python
from function import *
import sys
import getopt


def main(argv):
    times = 0
    is_lead = ''
    device = ''

    try:
        opts, args = getopt.getopt(argv, "ht:l:d:", ["times=", "is_lead=", "device="])
    except getopt.GetoptError:
        print 'Please input: python group.py -t <times>(int) -l <is_lead>(y or n) -d <device>(android or ios)'
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print 'Please input: python group.py -t <times>(int) -l <is_lead>(y or n) -d <device>(android or ios)'
            sys.exit()
        elif opt in ("-t", "--times"):
            times = int(arg)
        elif opt in ("-l", "--is_lead"):
            is_lead = arg
        elif opt in ("-d", "--device"):
            device = arg

    task = Group(device)

    for num in range(int(times)):
        if is_lead == 'y':
            if not task.start_group_fight():
                break
            task.group_fight()
            task.click_ok()
        else:
            if not task.wait_in_group():
                break
            task.group_fight()
            task.click_ok()
        task.analysis()


if __name__ == "__main__":
    main(sys.argv[1:])
