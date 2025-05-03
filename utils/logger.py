import logging
import sys


def setup_logger(name: str, level: str = "INFO"):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), "INFO"))

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s  %(levelname)s  %(name)s  %(message)s'
    ))

    if not logger.handlers:
        logger.addHandler(handler)

    return logger

if __name__ == '__main__':
    logger = setup_logger('RAG')
    logger.info('App started')