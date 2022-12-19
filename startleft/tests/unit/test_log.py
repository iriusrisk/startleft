import logging
from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

import startleft.startleft.api.fastapi_server as fastapi_server
import startleft.startleft.log as log

PORT = 5000

GLOBAL_LOG_LEVEL_TO_UVICORN_LOG_LEVEL = [
    ('DEBUG', 'DEBUG'),
    ('INFO', 'INFO'),
    ('WARN', 'WARNING'),
    ('ERROR', 'ERROR'),
    ('CRIT', 'CRITICAL')
]

UVICORN_LOG_LEVEL_TO_GLOBAL_LOG_LEVEL = [
    (50, logging.CRITICAL),
    (40, logging.ERROR),
    (30, logging.WARNING),
    (20, logging.INFO),
    (10, logging.DEBUG)
]


class TestLog:

    @mark.parametrize('server_log_level, uvicorn_log_level', GLOBAL_LOG_LEVEL_TO_UVICORN_LOG_LEVEL)
    def test_set_server_log_level_to_uvicorn_log(self, server_log_level, uvicorn_log_level):
        # GIVEN a set of server log levels
        log.get_root_logger().level = log.get_log_level(None, None, server_log_level)

        # WHEN the fastapi server log is configured
        log_config = fastapi_server.get_log_config()

        # THEN the uvicorn log is set with the correct log level
        assert log_config["loggers"]["uvicorn"]["level"] == uvicorn_log_level
        assert log_config["loggers"]["uvicorn.error"]["level"] == uvicorn_log_level
        assert log_config["loggers"]["uvicorn.access"]["level"] == uvicorn_log_level

    @mark.parametrize('uvicorn_log_level, server_log_level', UVICORN_LOG_LEVEL_TO_GLOBAL_LOG_LEVEL)
    def test_set_uvicorn_log_level_to_server_log(self, uvicorn_log_level, server_log_level):
        # GIVEN a set of uvicorn log levels
        uvicorn_log = log.get_uvicorn_logger()
        uvicorn_log.level = uvicorn_log_level

        # WHEN the server log is set
        log.set_log_level_from_uvicorn()

        # THEN the server log and the uvicorn log have the same log level
        assert log.get_root_logger().level == server_log_level
