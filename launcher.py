import os
from app.config import Config

from app.task import TaskChoose


def main():
    if not os.path.exists('config.xml'):
        Config().start_config()
    else:
        TaskChoose().choose_task()


main()
