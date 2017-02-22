#!/usr/local/bin/ python
from function import *
import sys
import getopt


def main(argv):
    is_lead = ''
    device = ''

    try:
        opts, args = getopt.getopt(argv, "hl:d:", ["is_lead=", "device="])
    except getopt.GetoptError:
        print 'Please input: python group.py -d <device>(android or ios) -l <is_lead>(y or n)'
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print 'Please input: python group.py -d <device>(android or ios) -l <is_lead>(y or n)'
            sys.exit()
        elif opt in ("-l", "--is_lead"):
            is_lead = arg
        elif opt in ("-d", "--device"):
            device = arg

    task = Group(device)

    while True:
        if is_lead == 'y':
            if not task.start_group_fight():
                break
            task.group_fight()
            click_ok(task.d)
        else:
            if not task.wait_in_group():
                break
            task.group_fight()
            if not click_get(task.d):
                break
        task.analysis()


if __name__ == "__main__":
    main(sys.argv[1:])
