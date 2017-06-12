import os

from config import Config
from task import TaskChoose


def main():
    if not os.path.exists('config.xml'):
        Config().start_config()
    else:
        TaskChoose().choose_task()


main()
