#!/usr/local/bin/ python
from function import *

times = raw_input('times=')
chapter = raw_input('chapter=')

task = Explore(int(chapter))

for num in range(int(times)):
    task.choose_chapter()
    task.exploring_fight()
    task.get_small_box()
    task.get_big_box()
    if task.found_shi_ju():
        break
    if task.is_pl_not_enough():
        break

task.analysis()
