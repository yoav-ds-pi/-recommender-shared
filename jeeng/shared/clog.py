from typing import Union
import logging


def setup_logger(base_level: Union[int, str] = logging.WARNING):
    logging.basicConfig()
    logging.root.setLevel(level=base_level)
    logging.basicConfig(level=base_level)
    logger = logging.getLogger(__name__)
    logger.info('logger started')


def get_logger(name: str, base_level: Union[int, str] = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(base_level)
    return logger
