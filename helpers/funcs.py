import datetime
import inspect
import os
import sys
import re
import time
import traceback

from helpers.excp import Bcolors


tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()


def what_func():
    return inspect.stack()[1][3]


def get_base_prefix_compat():
    return getattr(sys, "base_prefix", None) or \
        getattr(sys, "real_prefix", None) or sys.prefix


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if match is not None:
        return match.group(0)
    else:
        return ""


def server_errors_writer(msg):
    file_to_save = "server_errors.log"
    with open(file_to_save, 'a') as error_output:
        error_output.write(msg)


def msg_writer(filename, msg):
    with open(f"all_logs/{filename}", 'a') as output:
        os.chmod(f"all_logs/{filename}", 0o755)
        output.write(msg)


def server_exp_msg(line, error, function_name, script_name):
    # function_name = function_name.__name__
    err = (f"{Bcolors.FAIL}ERROR: {Bcolors.ENDC} {time.ctime()} -- {error} "
           f"| ERROR ON LINE: {line} | Function: {function_name} "
           f"| File: {script_name}")
    traceback_err = (f"{Bcolors.FAIL}*{Bcolors.ENDC} "
                     f"{traceback.format_exception_only(type(error), error)}")
    print(err)
    print(traceback_err)
    msg = (f"{time.ctime()} -- ERROR: {error} | ERROR ON LINE: {line} "
           f"| Function: {function_name} | File: {script_name}\n\t\t\t    "
           f"{traceback.format_exception_only(type(error), error)}\n")
    server_errors_writer(msg=msg)


def convert_keys(_dict):
    keys = []
    for key in _dict:
        keys.append(key)
    keys = tuple(keys)
    keys = str(keys).replace("'", '`')
    return keys
