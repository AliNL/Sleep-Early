# coding:utf-8

fl = open('config.xml', 'w')
fl.write('<root>\n')
print('正在进行配置...\n')
print('请输入常用设备(ios/android):')
fl.write('    <device>' + input() + '</device>\n')
print('请输入常用探索章节(1~18):')
fl.write('    <chapter>' + input() + '</chapter>\n')
print('请输入突破目标等级/10(1~7):')
fl.write('    <level>' + input() + '</level>\n')
fl.write('</root>')
fl.close()
