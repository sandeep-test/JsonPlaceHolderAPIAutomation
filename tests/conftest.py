import os
from tests.fixtures import *


def pytest_logger_config(logger_config):
    logger_config.add_loggers(['test_log', 'logger2'], stdout_level='info')
    logger_config.set_log_option_default('test_log,logger2')


def pytest_logger_logdirlink(config):
    return os.path.join(os.path.dirname(__file__), 'logs')
