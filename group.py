#!/usr/local/bin/ python
from function import *

times = raw_input('times=')
is_lead = raw_input('is_lead=')

task = Group()

for num in range(int(times)):
    if is_lead:
        if not task.start_group_fight():
            break
        task.group_fight()
        task.click_ok()
    else:
        if not task.wait_in_group():
            break
        task.group_fight()
        task.click_ok()

task.analysis()
