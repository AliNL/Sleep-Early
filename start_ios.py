#!/usr/local/bin/ python
import atx

driver = atx.connect('http://localhost:8100')
sid = str(driver.start_app('com.netease.onmyoji'))
fl = open('session_id_ios', 'wb')
fl.write(sid[16:52])
fl.close()
