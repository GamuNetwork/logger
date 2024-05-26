from enum import Enum
from typing import Callable

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
                    return LEVELS.DEBUG
                case 'info':
                    return LEVELS.INFO
                case 'warning':
                    return LEVELS.WARNING
                case 'error':
                    return LEVELS.ERROR
                case 'critical':
                    return LEVELS.CRITICAL
                case _:
                    return LEVELS.INFO

        def __str__(self):
            match self:
                case LEVELS.DEEP_DEBUG:
                    return '  DEBUG   '
                case LEVELS.DEBUG:
                    return '  DEBUG   '
                case LEVELS.INFO:
                    return '   INFO   '
                case LEVELS.WARNING:
                    return ' WARNING  '
                case LEVELS.ERROR:
                    return '  ERROR   '
                case LEVELS.CRITICAL:
                    return ' CRITICAL '
        
        def __int__(self):
            return self.value

        def __le__(self, other):
            return self.value <= other.value
    
        def color(self) -> COLORS:
            match self:
                case LEVELS.DEEP_DEBUG:
                    return COLORS.BLUE
                case LEVELS.DEBUG:
                    return COLORS.BLUE
                case LEVELS.INFO:
                    return COLORS.GREEN
                case LEVELS.WARNING:
                    return COLORS.YELLOW
                case LEVELS.ERROR:
                    return COLORS.RED
                case LEVELS.CRITICAL:
                    return COLORS.DARK_RED
                case _:
                    return COLORS.RESET
    
    
class SENSITIVE_LEVELS(Enum):
    HIDE = 0
    SHOW = 1
    ENCODE = 2
    

class Target:
    __instances = {}
    
    class Type(Enum):
        FILE = 0
        TERMINAL = 1
    
    def __new__(cls, target : Callable[[str], None], name : str = None):
        if target in cls.__instances:
            return cls.__instances[target]
        instance = super().__new__(cls)
        cls.__instances[target] = instance
        return instance
    
    def __init__(self, target : Callable[[str], None], name : str = None):
        self.target = target
        self.name = name if name is not None else target.__name__
        self.properties = {}
        self.type = Target.Type.TERMINAL if target == print else Target.Type.FILE

    @staticmethod
    def fromFile(file : str):
        def writeToFile(string : str):
            with open(file, 'a') as f:
                f.write(string + '\n')
        with open(file, 'w') as f: # clear the file
            f.write('')
        return Target(writeToFile, file)
    
    def __call__(self, string : str):
        self.target(string)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Target({self.name})"
    
    def __getitem__(self, key):
        return self.properties[key]
    
    def __setitem__(self, key, value):
        self.properties[key] = value
        
    def __delitem__(self, key):
        del self.properties[key]
        
    def __contains__(self, key):
        return key in self.properties
    
    @staticmethod
    def get(name : str) -> 'Target':
        for target in Target.__instances.values():
            if target.name == name:
                return target
        return None
    
    @staticmethod
    def exist(name : str) -> bool:
        return Target.get(name) is not None