#!/usr/bin/env python
from function import *

times = raw_input('times=')
level = raw_input('level/10=')

task = Break(int(times), int(level))

task.breaking()
