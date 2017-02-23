#!/usr/local/bin/ python
# coding=utf-8
from function import *
import os
import sys
import getopt
import xml.dom.minidom


def main(argv):
    try:
        dom = xml.dom.minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')
        chapter = int(root.getElementsByTagName('chapter'))
    except Exception:
        chapter = 16
        device = 'android'
    finally:
        times = 20

    try:
        opts, args = getopt.getopt(argv, "ht:c:d:", ["times=", "chapter=", "device="])
    except getopt.GetoptError:
        print('-d\tdevice: ios/android\tdefault: android')
        print('-c\tchapter: 1~18\tdefault: 16')
        print('-t\ttime: times\tdefault: 0')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('-d\tdevice: ios/android\tdefault: android')
            print('-c\tchapter: 1~18\tdefault: 16')
            print('-t\ttime: times\tdefault: 0')
            sys.exit()
        elif opt in ("-t", "--times"):
            times = int(arg)
        elif opt in ("-c", "--chapter"):
            chapter = int(arg)
        elif opt in ("-d", "--device"):
            device = arg

    task = Explore(chapter, device)

    for num in range(times):
        if num == 0:
            if is_exploring(task.d):
                task.exploring_fight()
                task.get_small_box()
                task.get_big_box()
                if task.found_shi_ju():
                    os.system('say -v Ting-Ting "找到石距啦"')
                    break
                if task.is_pl_not_enough():
                    os.system('say -v Ting-Ting "体力不足"')
                    break
                task.analysis()
            else:
                navigate_to_explore_map(task.d)
        task.choose_chapter()
        task.exploring_fight()
        task.get_small_box()
        task.get_big_box()
        if task.found_shi_ju():
            os.system('say -v Ting-Ting "找到石距啦"')
            task.d.delay(5 * 60)
            # break
        if task.is_pl_not_enough():
            os.system('say -v Ting-Ting "体力不足"')
            break
        task.analysis()


if __name__ == "__main__":
    main(sys.argv[1:])
