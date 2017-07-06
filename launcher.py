import sys

import os

from pages.steps.path_manager import set_path, cfg
from windows.config_window import ConfigPage
from windows.task_choose import TaskChoose


def main():
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    set_path(bundle_dir)
    if not os.path.exists(cfg()):
        ConfigPage().start_config()
    else:
        TaskChoose().choose_task()


if __name__ == "__main__":
    main()
