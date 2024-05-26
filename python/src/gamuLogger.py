from enum import Enum
from sys import stdout, stderr
from datetime import datetime
from typing import Any, Callable
import argparse
from utils import getCallerInfo, getTime, replaceNewLine, centerString

class COLORS(Enum):
    """
    usage:
    ```python
    print(COLORS.RED + "This is red text" + COLORS.RESET)
    print(COLORS.GREEN + "This is green text" + COLORS.RESET)
    print(COLORS.YELLOW + "This is yellow text" + COLORS.RESET)
    ```
    """
    RED = '\033[91m'
    DARK_RED = '\033[91m\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    NONE = ''
    
    def __str__(self):
        return self.value
    
    def __add__(self, other):
        return f"{self}{other}"
    
    def __radd__(self, other):
        return f"{other}{self}"
    
    def __repr__(self):
        return self.value

class Logger:
    class LEVELS(Enum):
        DEEP_DEBUG = 0  # this level is used to print very detailed information, it may contain sensitive information
        DEBUG = 1       # this level is used to print debug information, it may contain sensitive information
        INFO = 2        # this level is used to print information about the normal execution of the program
        WARNING = 3     # this level is used to print warnings about the execution of the program (non-blocking, but may lead to errors)
        ERROR = 4       # this level is used to print errors that may lead to the termination of the program
        CRITICAL = 5    # this level is used to print critical errors that lead to the termination of the program, typically used in largest except block
        
        
        @staticmethod
        def from_string(level):
            match level.lower():
                case 'debug':
                    return Logger.LEVELS.DEBUG
                case 'info':
                    return Logger.LEVELS.INFO
                case 'warning':
                    return Logger.LEVELS.WARNING
                case 'error':
                    return Logger.LEVELS.ERROR
                case 'critical':
                    return Logger.LEVELS.CRITICAL
                case _:
                    return Logger.LEVELS.INFO

        def __str__(self):
            match self:
                case Logger.LEVELS.DEEP_DEBUG:
                    return '  DEBUG   '
                case Logger.LEVELS.DEBUG:
                    return '  DEBUG   '
                case Logger.LEVELS.INFO:
                    return '   INFO   '
                case Logger.LEVELS.WARNING:
                    return ' WARNING  '
                case Logger.LEVELS.ERROR:
                    return '  ERROR   '
                case Logger.LEVELS.CRITICAL:
                    return ' CRITICAL '
        
        def __int__(self):
            return self.value

        def __le__(self, other):
            return self.value <= other.value
    
        def color(self) -> COLORS:
            match self:
                case Logger.LEVELS.DEEP_DEBUG:
                    return COLORS.BLUE
                case Logger.LEVELS.DEBUG:
                    return COLORS.BLUE
                case Logger.LEVELS.INFO:
                    return COLORS.GREEN
                case Logger.LEVELS.WARNING:
                    return COLORS.YELLOW
                case Logger.LEVELS.ERROR:
                    return COLORS.RED
                case Logger.LEVELS.CRITICAL:
                    return COLORS.DARK_RED
                case _:
                    return COLORS.RESET
    
    class SENSITIVE_LEVELS(Enum):
        HIDE = 0
        SHOW = 1
        ENCODE = 2
    
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
            cls.__instance.level = cls.LEVELS.INFO
            cls.__instance.target = stdout
            cls.__instance.show_sensitive_data = cls.SENSITIVE_LEVELS.HIDE
            cls.__instance.sensitive_data = [] # list of sensitive data that should not be printed
            cls.__instance.moduleMap = {} # key : filename, value : module name
        return cls.__instance
            
    def __build_message(self, level : LEVELS, message : str, filename : str):
        result = ""
        if self.target == stderr or self.target == stdout:
            result += f"[{str(COLORS.BLUE)}{getTime()}{str(COLORS.RESET)}] [{level.color()}{level}{str(COLORS.RESET)}]"
        else:
            # if the target is a file, we don't need to color the output
            result += f"[{getTime()}] [{level}]"
        
        if filename in self.moduleMap:
            result += f" [ {centerString(self.moduleMap[filename], 10)} ]"
            
        result += " " + replaceNewLine(message, 33 + (15 if filename in self.moduleMap else 0))
        return result
        
    def __hide_sensitive(self, message : str):
        if self.show_sensitive_data == self.SENSITIVE_LEVELS.HIDE:
            for sensitive in self.sensitive_data:
                message = message.replace(str(sensitive), '*'*len(str(sensitive)))
        elif self.show_sensitive_data == self.SENSITIVE_LEVELS.ENCODE:
            for sensitive in self.sensitive_data:
                message = message.replace(str(sensitive), str(sensitive).encode().hex()) #transform "sensitive" into "73656e736974697665"
        return message
    
    def __print(self, level : LEVELS, message : Any, filename = ""):
        message = str(message)
        message = self.__hide_sensitive(message)
        if self.level <= level:
            print(self.__build_message(level, message, filename), file=self.target)

    @staticmethod
    def deep_debug(message : Any, filename = getCallerInfo()):
        Logger().__print(Logger.LEVELS.DEEP_DEBUG, message, filename)

    @staticmethod
    def debug(message : Any, filename = getCallerInfo()):
        Logger().__print(Logger.LEVELS.DEBUG, message, filename)
    
    @staticmethod
    def info(message : Any, filename = getCallerInfo()):
        Logger().__print(Logger.LEVELS.INFO, message, getCallerInfo())
    
    @staticmethod
    def warning(message : Any, filename = getCallerInfo()):
        Logger().__print(Logger.LEVELS.WARNING, message, filename)
        
    @staticmethod
    def error(message : Any, filename = getCallerInfo()):
        Logger().__print(Logger.LEVELS.ERROR, message, filename)
        
    @staticmethod
    def critical(message : Any, filename = getCallerInfo()):
        Logger().__print(Logger.LEVELS.CRITICAL, message, filename)
        
    @staticmethod
    def message(message : Any, color : COLORS = COLORS.NONE):
        Logger().__print(Logger.LEVELS.INFO, f"{color}{message}{COLORS.RESET}")
        
    @staticmethod
    def set_level(level : LEVELS):
        Logger().level = level
        
    @staticmethod
    def set_module(name : str):
        Logger().moduleMap[getCallerInfo()] = name
        
    @staticmethod
    def set_target(target):
        Logger().target = target
        
    @staticmethod
    def show_sensitive(mode : SENSITIVE_LEVELS):
        Logger().show_sensitive_data = mode
        if mode == Logger().SENSITIVE_LEVELS.SHOW:
            Logger().__message("Sensitive mode was disable, this file may contain sensitive information, please do not share it with anyone", COLORS.YELLOW)
        elif mode == Logger().SENSITIVE_LEVELS.ENCODE:
            Logger().__message("Sensitive mode was enable, this file may contain encoded sensitive information, please do not share it with anyone", COLORS.YELLOW)
        
    @staticmethod
    def add_sensitive(sensitive : Any):
        Logger().sensitive_data.append(sensitive)
        
    @staticmethod
    def config_argparse(parser : argparse.ArgumentParser):
        log_group = parser.add_argument_group("Logging options")
        log_group.add_argument("--log-level", type=str, default="INFO", help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        log_group.add_argument("--log-target", type=argparse.FileType('w'), default=stdout, help="Set the logging target (default: stdout)")
        log_group.add_argument("--log-sensitive", type=str, default="HIDE", help="Set the sensitive data display mode (HIDE, SHOW, ENCODE)", choices=["HIDE", "SHOW", "ENCODE"])
        
    @staticmethod
    def parse_args(args : argparse.Namespace):
        self = Logger()
        if args.log_level:
            self.set_level(self.LEVELS.from_string(args.log_level))
        if args.log_target:
            self.set_target(args.log_target)
        if args.log_sensitive:
            self.show_sensitive(args.log_sensitive)
    
            
def deep_debug(message : Any):
    Logger.deep_debug(message, getCallerInfo())
        
def debug(message : Any):
    Logger.debug(message, getCallerInfo())

def info(message : Any):
    Logger.info(message, getCallerInfo())
    
def warning(message : Any):
    Logger.warning(message, getCallerInfo())
    
def error(message : Any):
    Logger.error(message, getCallerInfo())

def critical(message : Any):
    Logger.critical(message, getCallerInfo())
    
def message(message : Any, color : COLORS = COLORS.NONE):
    """
    Print a message to the standard output, in yellow color\n
    This method should be used before any other method\n
    It is used to pass information to the user about the global execution of the program
    """
    Logger.message(message, color)
    
    
def deep_debug_func(chrono : bool = False):
    """
    Decorator to print deep debug messages before and after the function call
    usage:
    ```python
    @deep_debug_func(chrono=False)
    def my_function(arg1, arg2, kwarg1=None):
        return arg1+arg2
        
    my_function("value1", "value2", kwarg1="value3")
    ```
    will print:
    ```log
    [datetime] [   DEBUG   ] Calling my_function with\n\t\t\t   | args: (value1, value2)\n\t\t\t   | kwargs: {'kwarg1': 'value3'}
    [datetime] [   DEBUG   ] Function my_function returned "value1value2"
    ```
    
    note: this decorator does nothing if the Logger level is not set to deep debug
    """
    def pre_wrapper(func : Callable):
        def wrapper(*args, **kwargs):
            deep_debug(f"Calling {func.__name__} with\nargs: {args}\nkwargs: {kwargs}")
            if chrono:
                start = datetime.now()
            result = func(*args, **kwargs)
            if chrono:
                end = datetime.now()
                deep_debug(f"Function {func.__name__} took {end-start} to execute and returned \"{result}\"")
            else:
                deep_debug(f"Function {func.__name__} returned \"{result}\"")
            return result
        return wrapper
    return pre_wrapper

def debug_func(chrono : bool = False):
    """
    Decorator to print deep debug messages before and after the function call
    usage:
    ```python
    @deep_debug_func
    def my_function(arg1, arg2, kwarg1=None):
        return arg1+arg2
        
    my_function("value1", "value2", kwarg1="value3")
    ```
    will print:
    ```log
    [datetime] [   DEBUG   ] Calling my_function with\n\t\t\t   | args: (value1, value2)\n\t\t\t   | kwargs: {'kwarg1': 'value3'}
    [datetime] [   DEBUG   ] Function my_function returned "value1value2"
    ```
    
    note: this decorator does nothing if the Logger level is not set to debug or deep debug
    """
    def pre_wrapper(func : Callable):
        def wrapper(*args, **kwargs):
            debug(f"Calling {func.__name__} with\nargs: {args} and\nkwargs: {kwargs}")
            if chrono:
                start = datetime.now()
            result = func(*args, **kwargs)
            if chrono:
                end = datetime.now()
                debug(f"Function {func.__name__} took {end-start} to execute and returned \"{result}\"")
            else:
                debug(f"Function {func.__name__} returned \"{result}\"")
            return result
        return wrapper
    return pre_wrapper

def chrono(func : Callable):
    """
    Decorator to print the execution time of a function
    usage:
    ```python
    @chrono
    def my_function(arg1, arg2, kwarg1=None):
        return arg1+arg2
        
    my_function("value1", "value2", kwarg1="value3")
    ```
    will print:
    ```log
    [datetime] [   DEBUG   ] Function my_function took 0.0001s to execute
    ```
    """
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        debug(f"Function {func.__name__} took {end-start} to execute")
        return result
    return wrapper

if __name__ == '__main__':
    Logger.set_level(Logger.LEVELS.DEEP_DEBUG)
    deep_debug("Deep debug message")
    debug({"key": "value", "key2": "value2"})
    info("Info message")
    warning("Warning message")
    error("Error message")
    critical("Critical message")
    info("This is a multi-line message\n\tThis is the second line\n\t\tThis is the third line")
    
    Logger.set_module("TestModule")
    
    critical("Critical message")
    info("This is a multi-line message\n\tThis is the second line\n\t\tThis is the third line")