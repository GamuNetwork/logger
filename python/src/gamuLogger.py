from enum import Enum
from sys import stdout, stderr
from datetime import datetime
from typing import Any, Callable, List
import argparse
from utils import getCallerInfo, getTime, replaceNewLine, centerString
from customTypes import COLORS, LEVELS, SENSITIVE_LEVELS, Target
from json import dumps


class Logger:

    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
            cls.__instance.targets = [Target(print, "terminal")]
            cls.__instance.show_sensitive_data = SENSITIVE_LEVELS.HIDE
            cls.__instance.sensitive_data = [] # list of sensitive data that should not be printed
            cls.__instance.moduleMap = {} # key : filename, value : module name
            
            #configuring default target
            Target.get("terminal")["level"] = LEVELS.INFO
        return cls.__instance    
    
    def __print(self, level : LEVELS, message : str, filename : str):
        for target in self.targets:
            if not target["level"] <= level:
                continue
            result = ""
            if target.type == Target.Type.TERMINAL:
                result += f"[{str(COLORS.BLUE)}{getTime()}{str(COLORS.RESET)}] [{level.color()}{level}{str(COLORS.RESET)}]"
            else:
                # if the target is a file, we don't need to color the output
                result += f"[{getTime()}] [{level}]"
            
            if filename in self.moduleMap:
                if target.type == Target.Type.TERMINAL:
                    result += f" [ {COLORS.BLUE}{centerString(self.moduleMap[filename], 10)}{COLORS.RESET} ]"
                else:
                    result += f" [ {centerString(self.moduleMap[filename], 10)} ]"
                
            if type(message) in [dict, list]:
                message = dumps(message, indent=4)
            elif type(message) not in [str, int, float]:
                message = str(message)
            
            result += " " + replaceNewLine(message, 33 + (15 if filename in self.moduleMap else 0))
            target(result)
    
    @staticmethod
    def deepDebug(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.DEEP_DEBUG, message, filename)

    @staticmethod
    def debug(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.DEBUG, message, filename)
    
    @staticmethod
    def info(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.INFO, message, getCallerInfo())
    
    @staticmethod
    def warning(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.WARNING, message, filename)
        
    @staticmethod
    def error(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.ERROR, message, filename)
        
    @staticmethod
    def critical(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.CRITICAL, message, filename)
        
    @staticmethod
    def message(message : Any, color : COLORS = COLORS.NONE):
        Logger().__print(LEVELS.INFO, f"{color}{message}{COLORS.RESET}")
        
    @staticmethod
    def setLevel(targetName: str, level : LEVELS):
        target = Target.get(targetName)
        if target in Logger().targets:
            target["level"] = level
        else:
            raise ValueError("Target not found")
        
    @staticmethod
    def setModule(name : str):
        Logger().moduleMap[getCallerInfo()] = name
        
    @staticmethod
    def addTarget(targetFunc : Callable[[str], None] | str | Target, level : LEVELS = LEVELS.INFO):
        target = None #type: Target
        if type(targetFunc) == str:
            target = Target.fromFile(targetFunc)
        elif type(targetFunc) == Target:
            target = targetFunc
        else:
            target = Target(targetFunc)
        Logger().targets.append(target)
        Logger.setLevel(target.name, level)
        
    @staticmethod
    def showSensitive(mode : SENSITIVE_LEVELS):
        Logger().show_sensitive_data = mode
        if mode == Logger().SENSITIVE_LEVELS.SHOW:
            Logger().__message("Sensitive mode was disable, this file may contain sensitive information, please do not share it with anyone", COLORS.YELLOW)
        elif mode == Logger().SENSITIVE_LEVELS.ENCODE:
            Logger().__message("Sensitive mode was enable, this file may contain encoded sensitive information, please do not share it with anyone", COLORS.YELLOW)
        
    @staticmethod
    def addSensitive(sensitive : Any):
        Logger().sensitive_data.append(sensitive)
        
    @staticmethod
    def configArgparse(parser : argparse.ArgumentParser):
        log_group = parser.add_argument_group("Logging options")
        log_group.add_argument("--log-level", type=str, default="INFO", help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        log_group.add_argument("--log-target", type=argparse.FileType('w'), default=stdout, help="Set the logging target (default: stdout)")
        log_group.add_argument("--log-sensitive", type=str, default="HIDE", help="Set the sensitive data display mode (HIDE, SHOW, ENCODE)", choices=["HIDE", "SHOW", "ENCODE"])
        
    @staticmethod
    def parseArgs(args : argparse.Namespace):
        self = Logger()
        if args.log_level:
            self.set_level(LEVELS.from_string(args.log_level))
        if args.log_target:
            self.set_target(args.log_target)
        if args.log_sensitive:
            self.show_sensitive(args.log_sensitive)
    
            
def deepDebug(message : Any):
    Logger.deepDebug(message, getCallerInfo())
        
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
    
    
def deepDebugFunc(chrono : bool = False):
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
            deepDebug(f"Calling {func.__name__} with\nargs: {args}\nkwargs: {kwargs}")
            if chrono:
                start = datetime.now()
            result = func(*args, **kwargs)
            if chrono:
                end = datetime.now()
                deepDebug(f"Function {func.__name__} took {end-start} to execute and returned \"{result}\"")
            else:
                deepDebug(f"Function {func.__name__} returned \"{result}\"")
            return result
        return wrapper
    return pre_wrapper

def debugFunc(chrono : bool = False):
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

# create the instance of the logger
Logger()
