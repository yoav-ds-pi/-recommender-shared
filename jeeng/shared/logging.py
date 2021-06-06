import logging


def setup_logger():
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)
    logger = logging.getLogger(__name__)
    logger.info('logger started')
