# coding=utf-8
from support import *


@log("是否在探索地图")
@sure
def in_explore_map(d):
    if d.exists('JueXing.1334x750.png'):
        return True
    return False


@log("是否在副本内")
@sure
def is_exploring(d):
    if d.exists('exploring.1334x750.png'):
        return True
    return False