from sys import stdout, stderr
from datetime import datetime
from typing import Any, Callable, List
import argparse
from json import dumps

from .utils import getCallerInfo, getTime, replaceNewLine, centerString, strictTypeCheck, CustomJSONEncoder, splitLongString
from .customTypes import COLORS, LEVELS, SENSITIVE_LEVELS, Target, TERMINAL_TARGETS, LoggerConfig


class Logger:

    __instance = None # type: Logger
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
            cls.__instance.config = LoggerConfig()
            
            #configuring default target
            if len(cls.__instance.config["targets"]) == 0:
                cls.__instance.config["targets"] = [Target(TERMINAL_TARGETS.STDOUT)]
                Target.get("stdout")["level"] = LEVELS.INFO
                Target.get("stdout")["sensitiveMode"] = SENSITIVE_LEVELS.HIDE
        return cls.__instance    
    
#---------------------------------------- Internal methods ----------------------------------------
    
    @strictTypeCheck
    def __print(self, level : LEVELS, message : Any, filename : str):
        for target in self.config['targets']:
            self.__printInTarget(level, message, filename, target)
        
    @strictTypeCheck
    def __printInTarget(self, level : LEVELS, message : Any, filename : str, target : Target):
        if not target["level"] <= level:
            return
        result = ""
        if target.type == Target.Type.TERMINAL:
            result += f"[{COLORS.BLUE}{getTime()}{COLORS.RESET}] [{level.color()}{level}{COLORS.RESET}]"
        else:
            # if the target is a file, we don't need to color the output
            result += f"[{getTime()}] [{level}]"
        
        if filename in self.config['moduleMap']:
            if target.type == Target.Type.TERMINAL:
                result += f" [ {COLORS.BLUE}{centerString(self.config['moduleMap'][filename], 10)}{COLORS.RESET} ]"
            else:
                result += f" [ {centerString(self.config['moduleMap'][filename], 10)} ]"
            
        if type(message) in [int, float, bool]:
            message = str(message)
        elif type(message) == str:
            message = splitLongString(message, 150)
        else:
            message = dumps(message, indent=4, cls=CustomJSONEncoder)
        
        result += " " + replaceNewLine(message, 33 + (15 if filename in self.config['moduleMap'] else 0))
        result = self.__parseSensitive(result, target)
        target(result+"\n")
            
    @strictTypeCheck
    def __printMessageInTarget(self, message : str, color : COLORS, target : Target):
        message = self.__parseSensitive(message, target)
        if target.type == Target.Type.TERMINAL:
            target(f"{color}{message}{COLORS.RESET}")
        else:
            target(message+"\n")
        
    @strictTypeCheck
    def __printMessage(self, message : str, color : COLORS):
        for target in self.config['targets']:
            self.__printMessageInTarget(message, color, target)
    
    @strictTypeCheck
    def __parseSensitive(self, message : str, target : Target) -> str:
        match target["sensitiveMode"]:
            case SENSITIVE_LEVELS.HIDE:
                for sensitive in self.config['sensitiveDatas']:
                    message = message.replace(sensitive, "*" * len(sensitive)) 
                return message          
            case SENSITIVE_LEVELS.SHOW:
                return message
            
#---------------------------------------- Logging methods -----------------------------------------
            
    @staticmethod
    def deepDebug(message : Any, filename = None):
        if filename is None:
            filename = getCallerInfo()
        Logger().__print(LEVELS.DEEP_DEBUG, message, filename)

    @staticmethod
    def debug(message : Any, filename = None):
        if filename is None:
            filename = getCallerInfo()
        Logger().__print(LEVELS.DEBUG, message, filename)
    
    @staticmethod
    def info(message : Any, filename = None):
        if filename is None:
            filename = getCallerInfo()
        Logger().__print(LEVELS.INFO, message, filename)
    
    @staticmethod
    def warning(message : Any, filename = None):
        if filename is None:
            filename = getCallerInfo()
        Logger().__print(LEVELS.WARNING, message, filename)
        
    @staticmethod
    def error(message : Any, filename = None):
        if filename is None:
            filename = getCallerInfo()
        Logger().__print(LEVELS.ERROR, message, filename)
        
    @staticmethod
    def critical(message : Any, filename = None):
        if filename is None:
            filename = getCallerInfo()
        Logger().__print(LEVELS.CRITICAL, message, filename)
        
    @staticmethod
    @strictTypeCheck
    def message(message : Any, color : COLORS = COLORS.NONE):
        Logger().__printMessage(message, color)
        
#---------------------------------------- Configuration methods -----------------------------------
        
    @staticmethod
    @strictTypeCheck
    def setLevel(targetName: str, level : LEVELS):
        target = Target.get(targetName)
        if target in Logger().config['targets']:
            target["level"] = level
        else:
            raise ValueError("Target not found")
        
    @staticmethod
    @strictTypeCheck
    def setSensitiveMode(targetName: str, mode : SENSITIVE_LEVELS):
        target = Target.get(targetName)
        if target in Logger().config['targets']:
            target["sensitiveMode"] = mode
        else:
            raise ValueError("Target not found")
        
        if mode == SENSITIVE_LEVELS.SHOW:
            Logger().__printMessageInTarget("Sensitive mode was disable, this file may contain sensitive information, please do not share it with anyone", COLORS.YELLOW, target)
        
    @staticmethod
    def setModule(name : str):
        if name == "":
            del Logger().config['moduleMap'][getCallerInfo()]
        elif len(name) > 15:
            raise ValueError("Module name should be less than 15 characters")
        else:
            Logger().config['moduleMap'][getCallerInfo()] = name
            
        
    @staticmethod
    @strictTypeCheck
    def addTarget(targetFunc : Callable[[str], None] | str | Target | TERMINAL_TARGETS, level : LEVELS = LEVELS.INFO, sensitiveMode : SENSITIVE_LEVELS = SENSITIVE_LEVELS.HIDE) -> str:
        target = None #type: Target
        if type(targetFunc) == str:
            target = Target.fromFile(targetFunc)
        elif type(targetFunc) == Target:
            target = targetFunc
        else:
            target = Target(targetFunc)
        Logger().config['targets'].append(target)
        Logger.setLevel(target.name, level)
        Logger.setSensitiveMode(target.name, sensitiveMode)
        return target.name
    
    @staticmethod
    @strictTypeCheck
    def addSensitiveData(data : Any):
        Logger().config['sensitiveDatas'].append(data)
        
    @staticmethod
    @strictTypeCheck
    def setConfigFile(configFile : str):
        Logger().config = LoggerConfig.fromConfigFile(configFile)
        
    @staticmethod
    @strictTypeCheck
    def reset():
        Target.clear()
        Logger().config.clear()
        
        #configuring default target
        Logger.__instance.config["targets"] = [Target(TERMINAL_TARGETS.STDOUT)]
        Target.get("stdout")["level"] = LEVELS.INFO
        Target.get("stdout")["sensitiveMode"] = SENSITIVE_LEVELS.HIDE
        
    @staticmethod
    @strictTypeCheck
    def configArgParse(parser : argparse.ArgumentParser):
        return LoggerConfig.configArgParse(parser)
    
    @staticmethod
    @strictTypeCheck
    def parseArgs(args : argparse.Namespace) -> None:
        Logger.__instance.config.parseArgs(args)
        
            
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
    
@strictTypeCheck
def message(message : Any, color : COLORS = COLORS.NONE):
    """
    Print a message to the standard output, in yellow color\n
    This method should be used before any other method\n
    It is used to pass information to the user about the global execution of the program
    """
    Logger.message(message, color)
    
@strictTypeCheck
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
    @strictTypeCheck
    def pre_wrapper(func : Callable):
        @strictTypeCheck
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

@strictTypeCheck
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
    @strictTypeCheck
    def pre_wrapper(func : Callable):
        @strictTypeCheck
        def wrapper(*args, **kwargs):
            debug(f"Calling {func.__name__} with\nargs: {args}\nkwargs: {kwargs}")
            if chrono:
                start = datetime.now()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error(f"An error occured in function {func.__name__}: {e.__class__.__name__} - {e}")
                raise e
            if chrono:
                end = datetime.now()
                debug(f"Function {func.__name__} took {end-start} to execute and returned \"{result}\"")
            else:
                debug(f"Function {func.__name__} returned \"{result}\"")
            return result
        return wrapper
    return pre_wrapper

@strictTypeCheck
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
    @strictTypeCheck
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        debug(f"Function {func.__name__} took {end-start} to execute")
        return result
    return wrapper

# create the instance of the logger
Logger()

if __name__ == '__main__':
    from time import sleep
    
    @chrono
    def main():
        # Logger.setSensitiveMode("terminal", SENSITIVE_LEVELS.HIDE)
        # Logger.addTarget("main.log", LEVELS.DEEP_DEBUG, SENSITIVE_LEVELS.SHOW)
        # Logger.addSensitiveData("password")
        # Logger.setConfigFile("config.json")
        
        parser = argparse.ArgumentParser(description='Python project build script')
        Logger.configArgParse(parser)
        args = parser.parse_args()
        Logger.parseArgs(args)
        
        info(Logger())
        
        info("This is a deep debug message very very long : lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec odio vitae")
        debug("This is a debug message")
        info("hello, this is my password !")
        warning("This is a warning")
        error("this is an error")
        warning("password")
        critical("The process will now exit")
        
    main()