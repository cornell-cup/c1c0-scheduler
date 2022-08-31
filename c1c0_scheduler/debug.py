import logging

LOGGER_CONFIG = {
    # 'filename': 'scheduler.log',
    'format': '[%(asctime)s] [%(name)s]: [%(levelname)s] %(message)s',
    'datefmt': '%m-%d-%Y %H:%M:%S',
    'level': logging.WARNING
}


def get_logger():
    logging.getLogger()