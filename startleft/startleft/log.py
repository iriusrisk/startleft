import logging

import click

from startleft.startleft.filter.log_security_filter import LogSecurityFilter

SIMPLE_MESSAGE_FORMAT = '%(message)s'
VERBOSE_MESSAGE_FORMAT = '%(asctime)s %(process)d %(levelname)-8s%(module)s - %(message)s'
MAX_MSG_LOG_SIZE = 99999

uvicorn_levels_map: dict = {
    10: 'DEBUG',
    20: 'INFO',
    30: 'WARNING',
    40: 'ERROR',
    50: 'CRITICAL'
}


def __clean_root_handlers():
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)


def __set_simple_logger(level=None):
    logging.basicConfig(format=SIMPLE_MESSAGE_FORMAT, level=level)


def __set_verbose_logger(level=None):
    logging.basicConfig(
        format=VERBOSE_MESSAGE_FORMAT,
        level=level)


def __set_filters():
    for handler in logging.root.handlers:
        handler.addFilter(LogSecurityFilter(MAX_MSG_LOG_SIZE))


def configure_logging(verbose, level=None):
    __clean_root_handlers()
    __set_verbose_logger(level) if verbose else __set_simple_logger(level)
    __set_filters()


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


def get_root_logger():
    return logging.getLogger()


def get_uvicorn_logger():
    return logging.getLogger('uvicorn.error')


def __translate_log_level_into_uvicorn(log_level: int):
    if log_level in uvicorn_levels_map:
        return uvicorn_levels_map[log_level]
    else:
        raise click.BadParameter(f"Log level must be one of: {', '.join(log_level.keys())}")


def get_uvicorn_log_level():
    return __translate_log_level_into_uvicorn(get_root_logger().getEffectiveLevel())


def set_log_level_from_uvicorn():
    uvicorn_log_level = get_uvicorn_logger().level
    configure_logging(True, uvicorn_log_level)
    get_root_logger().level = uvicorn_log_level
