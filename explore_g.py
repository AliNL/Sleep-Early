#!/usr/local/bin/ python
from function import *
import sys
import getopt
import xml.dom.minidom


def main(argv):
    try:
        dom = xml.dom.minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        print('loading config from xml...')
    except IOError:
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
