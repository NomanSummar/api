import logging
from logging import FileHandler
from logging import Formatter
import os


s = '=' * 79
p = '/'.join(os.path.abspath(__file__).split('/')[:-2])


LOG_FORMAT = (
    "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")

CRITICAL_LOG_FORMAT = (
    "{s}\n\r%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d".format(s=s))

LOG_LEVEL = logging.INFO


def logger(script, logfile):
    core_info_log_file = os.path.join(
        p, "all_logs", "core", f"{os.path.splitext(logfile)[0]}_info.log")
    core_warning_log_file = os.path.join(
        p, "all_logs", "core", f"{os.path.splitext(logfile)[0]}_warning.log")
    core_error_log_file = os.path.join(
        p, "all_logs", "core", f"{os.path.splitext(logfile)[0]}_error.log")
    core_critical_log_file = os.path.join(
        p, "all_logs", "core", f"{os.path.splitext(logfile)[0]}_critical.log")

    core_logger = logging.getLogger(f"{script}.logs")
    core_logger.setLevel(LOG_LEVEL)

    core_info_logger_file_handler = FileHandler(core_info_log_file)
    core_info_logger_file_handler.setLevel(logging.INFO)
    core_info_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))

    core_warning_logger_file_handler = FileHandler(core_warning_log_file)
    core_warning_logger_file_handler.setLevel(logging.WARNING)
    core_warning_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))

    core_error_logger_file_handler = FileHandler(core_error_log_file)
    core_error_logger_file_handler.setLevel(logging.ERROR)
    core_error_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))

    core_critical_logger_file_handler = FileHandler(core_critical_log_file)
    core_critical_logger_file_handler.setLevel(logging.CRITICAL)
    core_critical_logger_file_handler.setFormatter(Formatter(CRITICAL_LOG_FORMAT))

    core_logger.addHandler(core_info_logger_file_handler)
    core_logger.addHandler(core_warning_logger_file_handler)
    core_logger.addHandler(core_error_logger_file_handler)
    core_logger.addHandler(core_critical_logger_file_handler)

    return core_logger
