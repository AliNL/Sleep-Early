# coding=utf-8
from .common_steps import *


@freeze
def exit_group_or_exploring(d):
    if d.click_image(img('close'), timeout=1.0):
        return False
    if d.click_image(img('in_group'), timeout=1.0):
        return True
    if d.click_image(img('back'), timeout=1.0):
        return True


@log("前往探索地图")
def navigate_to_explore_map(d):
    for i in range(5):
        if in_explore_map(d):
            return True
        if exit_group_or_exploring(d):
            d.click_image(img('confirm'), timeout=1.0)
    raise IOError("Unable to navigate!!!")


@log("前往阴阳寮结界突破")
def navigate_to_public_breaking(d):
    for i in range(5):
        if is_breaking(d):
            return True
        navigate_to_explore_map(d)
        d.click_image(img('break_icon'), timeout=1.0)
        d.click_image(img('public_tab'), timeout=1.0)
    raise IOError("Unable to navigate!!!")
