#!/usr/local/bin/ python
import function

function.launch()

times = raw_input('times=')
chapter = raw_input('chapter=')

for num in range(int(times)):
    function.easy_explore(int(chapter))
