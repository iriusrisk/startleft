import logging

import click

SIMPLE_MESSAGE_FORMAT = '%(message)s'
VERBOSE_MESSAGE_FORMAT = '%(asctime)s %(process)d %(levelname)-8s%(module)s - %(message)s'

def mock_sl():
    print('Escribiendo')

def __clean_root_handlers():
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)


def __set_simple_logger(level=None):
    logging.basicConfig(format=SIMPLE_MESSAGE_FORMAT, level=level)


def __set_verbose_logger(level=None):
    logging.basicConfig(
        format=VERBOSE_MESSAGE_FORMAT,
        level=level)


def configure_logging(verbose, level=None):
    __clean_root_handlers()
    __set_verbose_logger(level) if verbose else __set_simple_logger(level)


def get_log_level(ctx, param, value):
    levels = {
        'NONE': 100,
        'CRIT': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    if value.upper() in levels:
        return levels[value.upper()]
    else:
        raise click.BadParameter(f"Log level must be one of: {', '.join(levels.keys())}")
