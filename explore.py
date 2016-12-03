#!/usr/local/bin/ python
# coding=utf-8
from function import *
import os

times = raw_input('times=')
chapter = raw_input('chapter=')

task = Explore(int(chapter))

for num in range(int(times)):
    task.choose_chapter()
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
task.analysis()
