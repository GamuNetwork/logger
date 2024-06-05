from sys import stdout, stderr
from datetime import datetime
from typing import Any, Callable, List
import argparse
from utils import getCallerInfo, getTime, replaceNewLine, centerString, strictTypeCheck, CustomJSONEncoder
from customTypes import COLORS, LEVELS, SENSITIVE_LEVELS, Target, TERMINAL_TARGETS
from json import dumps


class Logger:

    __instance = None # type: Logger
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
            cls.__instance.targets = [Target(TERMINAL_TARGETS.STDOUT, "terminal")]
            cls.__instance.sensitiveData = [] # list of sensitive data that should not be printed
            cls.__instance.moduleMap = {} # key : filename, value : module name
            
            #configuring default target
            Target.get("terminal")["level"] = LEVELS.INFO
            Target.get("terminal")["sensitiveMode"] = SENSITIVE_LEVELS.HIDE
        return cls.__instance    
    
    @strictTypeCheck
    def __print(self, level : LEVELS, message : Any, filename : str):
        for target in self.targets:
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
        if filename in self.moduleMap:
            if target.type == Target.Type.TERMINAL:
                result += f" [ {COLORS.BLUE}{centerString(self.moduleMap[filename], 10)}{COLORS.RESET} ]"
            else:
                result += f" [ {centerString(self.moduleMap[filename], 10)} ]"
            
        if type(message) in [dict, list]:
            message = dumps(message, indent=4, cls=CustomJSONEncoder)
        elif type(message) not in [str, int, float]:
            message = str(message)
        
        result += " " + replaceNewLine(message, 33 + (15 if filename in self.moduleMap else 0))
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
        for target in self.targets:
            self.__printMessageInTarget(message, color, target)
    
    @strictTypeCheck
    def __parseSensitive(self, message : str, target : Target) -> str:
        match target["sensitiveMode"]:
            case SENSITIVE_LEVELS.HIDE:
                for sensitive in self.sensitiveData:
                    message = message.replace(sensitive, "*" * len(sensitive)) 
                return message          
            case SENSITIVE_LEVELS.SHOW:
                return message
            
    @staticmethod
    @strictTypeCheck
    def deepDebug(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.DEEP_DEBUG, message, filename)

    @staticmethod
    @strictTypeCheck
    def debug(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.DEBUG, message, filename)
    
    @staticmethod
    @strictTypeCheck
    def info(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.INFO, message, getCallerInfo())
    
    @staticmethod
    @strictTypeCheck
    def warning(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.WARNING, message, filename)
        
    @staticmethod
    @strictTypeCheck
    def error(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.ERROR, message, filename)
        
    @staticmethod
    @strictTypeCheck
    def critical(message : Any, filename = getCallerInfo()):
        Logger().__print(LEVELS.CRITICAL, message, filename)
        
    @staticmethod
    @strictTypeCheck
    def message(message : Any, color : COLORS = COLORS.NONE):
        Logger().__printMessage(message, color)
        
    @staticmethod
    @strictTypeCheck
    def setLevel(targetName: str, level : LEVELS):
        target = Target.get(targetName)
        if target in Logger().targets:
            target["level"] = level
        else:
            raise ValueError("Target not found")
        
    @staticmethod
    @strictTypeCheck
    def setSensitiveMode(targetName: str, mode : SENSITIVE_LEVELS):
        target = Target.get(targetName)
        if target in Logger().targets:
            target["sensitiveMode"] = mode
        else:
            raise ValueError("Target not found")
        
        if mode == SENSITIVE_LEVELS.SHOW:
            Logger().__printMessageInTarget("Sensitive mode was disable, this file may contain sensitive information, please do not share it with anyone", COLORS.YELLOW, target)
        
    @staticmethod
    @strictTypeCheck
    def setModule(name : str):
        if name == "":
            del Logger().moduleMap[getCallerInfo()]
        elif len(name) > 10:
            raise ValueError("Module name should be less than 10 characters")
        else:
            Logger().moduleMap[getCallerInfo()] = name
        
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
        Logger().targets.append(target)
        Logger.setLevel(target.name, level)
        Logger.setSensitiveMode(target.name, sensitiveMode)
        return target.name
    
    @staticmethod
    @strictTypeCheck
    def addSensitiveData(data : Any):
        Logger().sensitiveData.append(data)
        
    @staticmethod
    @strictTypeCheck
    def configArgparse(parser : argparse.ArgumentParser):
        log_group = parser.add_argument_group("Logging options")
        log_group.add_argument("--log-level", type=str, default="INFO", help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        log_group.add_argument("--log-target", type=argparse.FileType('w'), default=stdout, help="Set the logging target (default: stdout)")
        log_group.add_argument("--log-sensitive", type=str, default="HIDE", help="Set the sensitive data display mode (HIDE, SHOW, ENCODE)", choices=["HIDE", "SHOW", "ENCODE"])
        
    @staticmethod
    @strictTypeCheck
    def parseArgs(args : argparse.Namespace):
        self = Logger()
        if args.log_level:
            self.setTevel(LEVELS.from_string(args.log_level))
        if args.log_target:
            self.setTarget(args.log_target)
        if args.log_sensitive:
            self.showSensitive(args.log_sensitive)
            
    @staticmethod
    @strictTypeCheck
    def reset():
        Target.clear()
        Logger.__instance.targets = [Target(TERMINAL_TARGETS.STDOUT, "terminal")]
        Logger.__instance.sensitiveData = []
        Logger.__instance.moduleMap = {}
        
        #configuring default target
        Target.get("terminal")["level"] = LEVELS.INFO
        Target.get("terminal")["sensitiveMode"] = SENSITIVE_LEVELS.HIDE
            
@strictTypeCheck
def deepDebug(message : Any):
    Logger.deepDebug(message, getCallerInfo())
        
@strictTypeCheck
def debug(message : Any):
    Logger.debug(message, getCallerInfo())

@strictTypeCheck
def info(message : Any):
    Logger.info(message, getCallerInfo())

@strictTypeCheck
def warning(message : Any):
    Logger.warning(message, getCallerInfo())
    
@strictTypeCheck
def error(message : Any):
    Logger.error(message, getCallerInfo())

@strictTypeCheck
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
            result = func(*args, **kwargs)
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
        Logger.setSensitiveMode("terminal", SENSITIVE_LEVELS.HIDE)
        Logger.addTarget("main.log", LEVELS.DEEP_DEBUG, SENSITIVE_LEVELS.SHOW)
        Logger.addSensitiveData("password")
        
        info(Target.get("terminal").type)
        
        deepDebug("This is a deep debug message")
        debug("This is a debug message")
        info("hello, this is my password !")
        warning("This is a warning")
        error("this is an error")
        critical("The process will now exit")
        
    main()