#!/usr/local/bin/ python
import function

function.launch()

times = raw_input('times=')
is_lead = raw_input('is_lead=')

for num in range(int(times)):
    function.easy_group(bool(is_lead))
