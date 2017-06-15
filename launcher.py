import sys

import os
from appdirs import user_data_dir

from pages.steps.path_manager import set_path, cfg
from windows.config_window import ConfigPage
from windows.task_choose import TaskChoose


def main():
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    current = bundle_dir
    temp = user_data_dir('Sleep Early', 'SanGe')

    if not os.path.exists(temp):
        os.makedirs(temp)
    set_path(current, temp)
    if not os.path.exists(cfg()):
        ConfigPage().start_config()
    else:
        TaskChoose().choose_task()


if __name__ == "__main__":
    main()
