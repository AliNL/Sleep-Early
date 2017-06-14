import os
from windows.config_window import ConfigPage

from windows.task_choose import TaskChoose


def main():
    if not os.path.exists('./config.xml'):
        ConfigPage().start_config()
    else:
        TaskChoose().choose_task()


if __name__ == "__main__":
    main()
