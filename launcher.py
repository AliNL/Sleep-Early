import os
from pages.config_page import ConfigPage

from pages.task import TaskChoose


def main():
    if not os.path.exists('config.xml'):
        ConfigPage().start_config()
    else:
        TaskChoose().choose_task()


if __name__ == "__main__":
    main()