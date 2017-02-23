#!/usr/local/bin/ python
from function import *
import sys
import getopt
import xml.dom.minidom


def main(argv):
    try:
        dom = xml.dom.minidom.parse('config.xml')
        root = dom.documentElement
        root.getElementsByTagName('device')
        device = root.getElementsByTagName('device')
    except Exception:
        device = 'android'
    finally:
        is_lead = False


    try:
        opts, args = getopt.getopt(argv, "hld:", ["is_lead=", "device="])
    except getopt.GetoptError:
        print('-d\tdevice: ios/android\tdefault: android')
        print('-l\tis_lead\tno value needed')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('-d\tdevice: ios/android\tdefault: android')
            print('-l\tis_lead\tno value needed')
            sys.exit()
        elif opt in ("-l", "--is_lead"):
            is_lead = True
        elif opt in ("-d", "--device"):
            device = arg

    task = Group(device)

    while True:
        if is_lead:
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
