import logging


def setup_logger(base_level = logging.WARNING):
    logging.basicConfig()
    logging.root.setLevel(level=base_level)
    logging.basicConfig(level=base_level)
    logger = logging.getLogger(__name__)
    logger.info('logger started')
