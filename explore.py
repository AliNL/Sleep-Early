#!/usr/local/bin/ python
from function import *

driver = launch()

times = raw_input('times=')
chapter = raw_input('chapter=')
task = Explore(driver)

for num in range(int(times)):
    task.choose_chapter(int(chapter))
    while not task.fight_boss():
        task.fight_monster()
    task.get_small_box()
    task.get_big_box()
    if task.find_shi_ju():
        break
