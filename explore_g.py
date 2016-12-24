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
        print 'Please input: python explore_g.py -d <device>(android or ios) -l <is_lead>(y or n)'
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print 'Please input: python explore_g.py -d <device>(android or ios) -l <is_lead>(y or n)'
            sys.exit()
        elif opt in ("-l", "--is_lead"):
            is_lead = arg
        elif opt in ("-d", "--device"):
            device = arg

    task = ExploreG(device)

    while True:
        if is_lead == 'y':
            # if not task.start_group_fight():
            #     break
            task.exploring_fight()
            task.get_small_box()
            time.sleep(10)
            task.ok()
        else:
            # if not task.wait_in_group():
            #     break
            task.exploring_wait()
            task.get_small_box()
            task.get_big_box()
            task.get_invitation()
        task.analysis()


if __name__ == "__main__":
    main(sys.argv[1:])
