from enum import Enum
from sys import stdout, stderr
from datetime import datetime
from typing import Any, Callable

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

class Printer:
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
                    return Printer.LEVELS.DEBUG
                case 'info':
                    return Printer.LEVELS.INFO
                case 'warning':
                    return Printer.LEVELS.WARNING
                case 'error':
                    return Printer.LEVELS.ERROR
                case 'critical':
                    return Printer.LEVELS.CRITICAL
                case _:
                    return Printer.LEVELS.INFO

        def __str__(self):
            match self:
                case Printer.LEVELS.DEEP_DEBUG:
                    return '  DEBUG   '
                case Printer.LEVELS.DEBUG:
                    return '  DEBUG   '
                case Printer.LEVELS.INFO:
                    return '   INFO   '
                case Printer.LEVELS.WARNING:
                    return ' WARNING  '
                case Printer.LEVELS.ERROR:
                    return '  ERROR   '
                case Printer.LEVELS.CRITICAL:
                    return ' CRITICAL '
        
        def __int__(self):
            return self.value

        def __le__(self, other):
            return self.value <= other.value
    
        def color(self) -> COLORS:
            match self:
                case Printer.LEVELS.DEEP_DEBUG:
                    return COLORS.BLUE
                case Printer.LEVELS.DEBUG:
                    return COLORS.BLUE
                case Printer.LEVELS.INFO:
                    return COLORS.GREEN
                case Printer.LEVELS.WARNING:
                    return COLORS.YELLOW
                case Printer.LEVELS.ERROR:
                    return COLORS.RED
                case Printer.LEVELS.CRITICAL:
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
            cls.__instance = super(Printer, cls).__new__(cls)
            cls.__instance.level = cls.LEVELS.INFO
            cls.__instance.target = stdout
            cls.__instance.show_sensitive_data = cls.SENSITIVE_LEVELS.HIDE
            cls.__instance.sensitive_data = [] # list of sensitive data that should not be printed
        return cls.__instance
    
    def __set_level(self, level : LEVELS):
        self.level = level
        
    def __set_target(self, target):
        self.target = target
        
    def __show_sensitive(self, mode : SENSITIVE_LEVELS):
        self.show_sensitive_data = mode
        if mode == self.SENSITIVE_LEVELS.SHOW:
            Printer().__message("Sensitive mode was disable, this file may contain sensitive information, please do not share it with anyone", COLORS.YELLOW)
        elif mode == self.SENSITIVE_LEVELS.ENCODE:
            Printer().__message("Sensitive mode was enable, this file may contain encoded sensitive information, please do not share it with anyone", COLORS.YELLOW)
        
    def __add_sensitive(self, sensitive : Any):
        self.sensitive_data.append(sensitive)
        
    @staticmethod
    def __parse_message(message : str):
        return message.replace('\n', '\n' + ('\t' * 4)+' | ')
    
    @staticmethod
    def __get_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __build_message(self, level : LEVELS, message : str, dateColor : COLORS = COLORS.BLUE):
        if self.target == stderr or self.target == stdout:
            return f"[{str(dateColor)}{self.__get_time()}{str(COLORS.RESET)}] [{level.color()}{level}{str(COLORS.RESET)}] {self.__parse_message(message)}"
        
    def __hide_sensitive(self, message : str):
        if self.show_sensitive_data == self.SENSITIVE_LEVELS.HIDE:
            for sensitive in self.sensitive_data:
                message = message.replace(str(sensitive), '*'*len(str(sensitive)))
        elif self.show_sensitive_data == self.SENSITIVE_LEVELS.ENCODE:
            for sensitive in self.sensitive_data:
                message = message.replace(str(sensitive), str(sensitive).encode().hex()) #transform "sensitive" into "73656e736974697665"
        return message
    
    def __print(self, level : LEVELS, message : Any, dateColor : COLORS = COLORS.BLUE):
        message = str(message)
        message = self.__hide_sensitive(message)
        if self.level <= level:
            print(self.__build_message(level, message, dateColor), file=self.target)
            
    def __deep_debug(self, message : Any, dateColor : COLORS = COLORS.BLUE):
        self.__print(self.LEVELS.DEEP_DEBUG, message, dateColor)
            
    def __debug(self, message : Any, dateColor : COLORS = COLORS.BLUE):
        self.__print(self.LEVELS.DEBUG, message, dateColor)
    
    def __info(self, message : Any, dateColor : COLORS = COLORS.GREEN):
        self.__print(self.LEVELS.INFO, message, dateColor)
        
    def __warning(self, message : Any, dateColor : COLORS = COLORS.YELLOW):
        self.__print(self.LEVELS.WARNING, message, dateColor)
        
    def __error(self, message : Any, dateColor : COLORS = COLORS.RED):
        self.__print(self.LEVELS.ERROR, message, dateColor)
        
    def __critical(self, message : Any, dateColor : COLORS = COLORS.DARK_RED):
        self.__print(self.LEVELS.CRITICAL, message, dateColor)
        
    def __message(self, message : Any, color : COLORS = COLORS.NONE):
        message = self.__hide_sensitive(message)
        print(color + message + COLORS.RESET, file=self.target)

    @staticmethod
    def deep_debug(message : Any, dateColor : COLORS = COLORS.BLUE):
        Printer().__deep_debug(message, dateColor)

    @staticmethod
    def debug(message : Any, dateColor : COLORS = COLORS.BLUE):
        Printer().__debug(message, dateColor)
    
    @staticmethod
    def info(message : Any, dateColor : COLORS = COLORS.BLUE):
        Printer().__info(message, dateColor)
    
    @staticmethod
    def warning(message : Any, dateColor : COLORS = COLORS.BLUE):
        Printer().__warning(message, dateColor)
        
    @staticmethod
    def error(message : Any, dateColor : COLORS = COLORS.BLUE):
        Printer().__error(message, dateColor)
        
    @staticmethod
    def critical(message : Any, dateColor : COLORS = COLORS.BLUE):
        Printer().__critical(message, dateColor)
        
    @staticmethod
    def message(message : Any, color : COLORS = COLORS.NONE):
        Printer().__message(message, color)
        
    @staticmethod
    def set_level(level : LEVELS):
        Printer().__set_level(level)
        
    @staticmethod
    def set_target(target):
        Printer().__set_target(target)
        
    @staticmethod
    def show_sensitive(mode : SENSITIVE_LEVELS):
        Printer().__show_sensitive(mode)
        
    @staticmethod
    def add_sensitive(sensitive : Any):
        Printer().__add_sensitive(sensitive)
        
def deep_debug(message : Any, dateColor : COLORS = COLORS.BLUE):
    Printer.deep_debug(message, dateColor)
        
def debug(message : Any, dateColor : COLORS = COLORS.BLUE):
    Printer.debug(message, dateColor)

def info(message : Any, dateColor : COLORS = COLORS.BLUE):
    Printer.info(message, dateColor)
    
def warning(message : Any, dateColor : COLORS = COLORS.BLUE):
    Printer.warning(message, dateColor)
    
def error(message : Any, dateColor : COLORS = COLORS.BLUE):
    Printer.error(message, dateColor)

def critical(message : Any, dateColor : COLORS = COLORS.BLUE):
    Printer.critical(message, dateColor)
    
def message(message : Any, color : COLORS = COLORS.NONE):
    """
    Print a message to the standard output, in yellow color\n
    This method should be used before any other method\n
    It is used to pass information to the user about the global execution of the program
    """
    Printer.message(message, color)
    
    
def deep_debug_func(func : Callable):
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
    
    note: this decorator does nothing if the Printer level is not set to deep debug
    """
    def wrapper(*args, **kwargs):
        deep_debug(f"Calling {func.__name__} with\nargs: {args}\nkwargs: {kwargs}")
        result = func(*args, **kwargs)
        deep_debug(f"Function {func.__name__} returned \"{result}\"")
        return result
    return wrapper

def debug_func(func : Callable):
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
    
    note: this decorator does nothing if the Printer level is not set to debug or deep debug
    """
    def wrapper(*args, **kwargs):
        debug(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        debug(f"Function {func.__name__} returned {result}")
        return result
    return wrapper

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
    Printer.set_level(Printer.LEVELS.DEBUG)
    debug({"key": "value", "key2": "value2"})
    info("Info message")
    warning("Warning message")
    error("Error message")
    critical("Critical message")
    
    info("This is a multi-line message\n\tThis is the second line\n\t\tThis is the third line")