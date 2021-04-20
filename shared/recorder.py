import logging
import os
import sys

from shared.widgets.builder import full_path


class SwaVanLogRecorder:
    __log_file_name__ = "data/logs/swavan.log"
    logger = logging.getLogger('')

    @classmethod
    def send_log(cls, message: str):
        cls.logger.info(message)

    @classmethod
    def init(cls):
        if not cls.is_log_file_exist():
            open(full_path("data/logs/swavan.log"), 'w').close()
        cls.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(full_path(cls.__log_file_name__))
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        cls.logger.addHandler(fh)
        cls.logger.addHandler(sh)

    @classmethod
    def reading_log(cls):
        return (row for row in open(full_path(cls.__log_file_name__)))

    @classmethod
    def is_log_file_exist(cls) -> bool:
        return os.path.exists(full_path(cls.__log_file_name__))
