#!/usr/local/bin/ python
# coding=utf-8
from function import *

# 试用版功能,请手动修改参数

ex = Explore(16, 'ios')
br = Break(-1, device='ios')
bp = Break(0, device='ios')
t = 0

for num in range(100):
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
        bp.breaking()
        t = time.time()
    if ex.is_pl_not_enough():
        break
    ex.analysis()

