import os

from pages.steps.path_manager import set_path, cfg
from windows.config_window import ConfigPage
from windows.task_choose import TaskChoose

current = os.path.dirname(__file__)


def main():
    from appdirs import user_data_dir
    temp = user_data_dir('Sleep Early', 'SanGe')

    print(os.path.dirname(__file__))
    print(current)
    if not os.path.exists(temp):
        os.makedirs(temp)
    set_path(current, temp)
    if not os.path.exists(cfg()):
        ConfigPage().start_config()
    else:
        TaskChoose().choose_task()


if __name__ == "__main__":
    main()
