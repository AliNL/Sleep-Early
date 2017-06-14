# # coding=utf-8
# from xml.dom import minidom
#
# from function import *
#
#
# def main():
#     dom = minidom.parse('./config.xml')
#     root = dom.documentElement
#     device = root.getElementsByTagName('device')[0].firstChild.data
#     is_lead = False
#     task = ExploreG(device)
#
#     while True:
#         if is_lead:
#             task.exploring_fight(3)
#             task.get_small_box()
#             time.sleep(10)
#             click_ok(task.d)
#         else:
#             task.exploring_wait()
#             task.get_small_box()
#             task.get_big_box()
#             if not click_get(task.d):
#                 break
#         task.analysis()
#
