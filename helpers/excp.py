import datetime
import traceback
import time
from colorama import init, Fore, Style


init()


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Colors:
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    RED = Fore.RED
    LIGHTGREEN = Fore.LIGHTGREEN_EX
    LIGHTBLUE = Fore.LIGHTBLUE_EX
    LIGHTRED = Fore.LIGHTRED_EX
    LIGHTYELLOW = Fore.LIGHTYELLOW_EX
    RESETALL = Style.RESET_ALL


class Excp:
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    excp_error = None
    excp_ctime = f"{time.ctime()} {tz}"
    excp_line = None
    excp_func = None
    excp_script = None
    excp_traceback = None
    excp_spaces = ' ' * 7
    excp_error_msg = None

    def __init__(self):
        pass

    @classmethod
    def tcb(cls, error):
        cls.excp_traceback = traceback.format_exception_only(type(error), error)
        return cls.excp_traceback

    @classmethod
    def exp_msg(cls, line, error, function_name, script_name):
        # function_name = function_name.__name__
        cls.excp_error = error
        cls.excp_line = line
        cls.excp_func = function_name
        cls.excp_script = script_name
        cls.excp_traceback = traceback.format_exception_only(type(error), error)

        print(f"{Colors.LIGHTRED}ERROR: {Colors.RESETALL}{error}")
        print(f"{Colors.LIGHTRED}*{Colors.RESETALL} "
              f"Date: {cls.excp_ctime}")
        print(f"{Colors.LIGHTRED}*{Colors.RESETALL} "
              f"ERROR ON LINE: {line}")
        print(f"{Colors.LIGHTRED}*{Colors.RESETALL} "
              f"Function: {function_name}")
        print(f"{Colors.LIGHTRED}*{Colors.RESETALL} "
              f"File: {script_name}")
        print(f"{Colors.LIGHTRED}*{Colors.RESETALL} "
              f"{traceback.format_exception_only(type(error), error)}")

        tb = traceback.format_exception_only(type(error), error)
        cls.excp_error_msg = (f"ERROR: {error} | ERROR ON LINE: {line} | "
                              f"Function: {function_name} | File: "
                              f"{script_name}\n{cls.excp_spaces}"
                              f"{tb} {cls.excp_ctime}")
        return cls.excp_error_msg
