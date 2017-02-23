#!/usr/local/bin/ python
# coding=utf-8
import getopt
from function import *
import xml.dom.minidom


def main(argv):
    try:
        dom = xml.dom.minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        level = int(root.getElementsByTagName('level')[0].firstChild.data)
        chapter = int(root.getElementsByTagName('chapter')[0].firstChild.data)
        print('loading config from xml...')
    except IOError:
        device = 'android'
        level = 7
        chapter = 16
    finally:
        times = 25

    try:
        opts, args = getopt.getopt(argv, "ht:l:d:c:", ["times=", "level=", "device=", "chapter="])
    except getopt.GetoptError:
        print('-d\tdevice: ios/android\tdefault: android')
        print('-l\tlevel: 1~7\tdefault: 7')
        print('-t\ttimes: int\tdefault: 25')
        print('-c\tchapter: 1~18\tdefault: 16')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('-d\tdevice: ios/android\tdefault: android')
            print('-l\tlevel: 1~7\tdefault: 7')
            print('-t\ttimes: int\tdefault: 25')
            print('-c\tchapter: 1~18\tdefault: 16')
            sys.exit()
        elif opt in ("-t", "--times"):
            times = int(arg)
        elif opt in ("-l", "--level"):
            level = int(arg)
        elif opt in ("-c", "--chapter"):
            chapter = int(arg)
        elif opt in ("-d", "--device"):
            device = arg

    ex = Explore(chapter, device)
    br = Break(-1, level, 1, device)
    bp = Break(0, level, 1, device)
    t = 0

    for num in range(times):
        navigate_to_explore_map(ex.d)
        ex.choose_chapter()
        ex.exploring_fight()
        ex.get_small_box()
        ex.get_big_box()
        if ex.found_shi_ju():
            ex.d.delay(5 * 60)
        if time.time() - t > 600:
            if br.if_tickets_enough():
                br.breaking()
            t = time.time()
            bp.breaking()
        if ex.is_pl_not_enough():
            break
        ex.analysis()

if __name__ == "__main__":
    main(sys.argv[1:])