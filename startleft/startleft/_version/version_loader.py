import logging

logger = logging.getLogger(__name__)

DEFAULT_STARTLEFT_VERSION = 'development-version'


def load_startleft_version() -> str:
    try:
        from startleft.version import version
        return version
    except ModuleNotFoundError:
        logger.warning('Cannot get the real version of StartLeft, loading the default version')

    return DEFAULT_STARTLEFT_VERSION
