import os
import logging
import google.cloud.logging
from jeeng.shared.common import str_to_bool
from typing import Union


def setup_logger(base_level: Union[int, str] = logging.WARNING, gcp_logging=str_to_bool(os.getenv('USE_GCP_LOGGING'))):
    if gcp_logging:
        logging_client = google.cloud.logging.Client()
        logging_client.setup_logging()
    logging.basicConfig()
    logging.root.setLevel(level=base_level)
    logging.basicConfig(level=base_level)
    logger = logging.getLogger(__name__)
    logger.info('logger started')


def get_logger(name: str, base_level: Union[int, str] = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(base_level)
    return logger
