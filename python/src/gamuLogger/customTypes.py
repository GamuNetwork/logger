from enum import Enum
from typing import Callable
import sys
import os
import argparse
from json import loads
from xml.etree import ElementTree
import threading

class Module:
    __instances = {} #type: dict[tuple[str, str], Module]
    def __init__(self, name : str, parent : 'Module' = None, file : str = None, function : str = None):
        self.parent = parent
        self.name = name
        self.file = file
        self.function = function
        
        Module.__instances[(self.file, self.function)] = self
    
    def getCompleteName(self) -> str:
        if self.parent is None:
            return self.name
        return self.parent.getCompleteName() + '.' + self.name
    
    def getCompletePath(self) -> list[str]:
        if self.parent is None:
            return [self.name]
        return self.parent.getCompletePath() + [self.name]
    
    @staticmethod
    def get(filename : str, function : str) -> 'Module':
        if Module.exist(filename, function):
            return Module.__instances[(filename, function)]
        else:
            raise ValueError(f"No module found for file {filename} and function {function}")
        
    @staticmethod
    def exist(filename : str, function : str) -> bool:
        return (filename, function) in Module.__instances
    
    @staticmethod
    def delete(filename : str, function : str):
        if Module.exist(filename, function):
            del Module.__instances[(filename, function)]
        else:
            raise ValueError(f"No module found for file {filename} and function {function}")
    
    @staticmethod
    def getByName(name : str) -> 'Module':
        for module in Module.__instances.values():
            if module.getCompleteName() == name:
                return module
        raise ValueError(f"No module found for name {name}")
    
    @staticmethod
    def existByName(name : str) -> bool:
        for module in Module.__instances.values():
            if module.getCompleteName() == name:
                return True
        return False
    
    @staticmethod
    def deleteByName(name : str):
        if Module.existByName(name):
            del Module.__instances[name]
        else:
            raise ValueError(f"No module found for name {name}")
        
    
    @staticmethod
    def clear():
        Module.__instances = {}
        
    @staticmethod
    def new(name : str, file : str = None, function : str = None) -> 'Module':
        if Module.existByName(name):
            existing = Module.getByName(name)
            if file == existing.file and function == existing.function:
                return existing
            else:
                raise ValueError(f"Module {name} already exists with file {existing.file} and function {existing.function}")
        
        if '.' in name:
            parentName, moduleName = name.rsplit('.', 1)
            if Module.existByName(parentName):
                #get the parent module
                parent = Module.getByName(parentName)
                return Module(moduleName, parent, file, function)
            else:
                raise ValueError(f"No module found for name {parentName}")
        return Module(name, None, file, function)
    
        
        

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
    MAGENTA = '\033[96m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    NONE = ''
    
    def __str__(self):
        return self.value
    
    def __add__(self, other):
        """
        Allow to concatenate a string with a color, example:
        ```python
        print(COLORS.RED + "This is red text" + COLORS.RESET)
        ```
        or using an f-string:
        ```python
        print(f"{COLORS.RED}This is red text{COLORS.RESET}")
        ```
        """
        return f"{self}{other}"
    
    def __radd__(self, other):
        """
        Allow to concatenate a string with a color, example:
        ```python
        print(COLORS.RED + "This is red text" + COLORS.RESET)
        ```
        or using an f-string:
        ```python
        print(f"{COLORS.RED}This is red text{COLORS.RESET}")
        ```
        """
        return f"{other}{self}"
    
    def __repr__(self):
        return self.value

class LEVELS(Enum):
    """
    ## list of levels:
    - DEEP_DEBUG:   this level is used to print very detailed information, it may contain sensitive information
    - DEBUG:        this level is used to print debug information, it may contain sensitive information
    - INFO:         this level is used to print information about the normal execution of the program
    - WARNING:      this level is used to print warnings about the execution of the program (non-blocking, but may lead to errors)
    - ERROR:        this level is used to print errors that may lead to the termination of the program
    - CRITICAL:     this level is used to print critical errors that lead to the termination of the program, typically used in largest except block
    """
    
    DEEP_DEBUG = 0  # this level is used to print very detailed information, it may contain sensitive information
    DEBUG = 1       # this level is used to print debug information, it may contain sensitive information
    INFO = 2        # this level is used to print information about the normal execution of the program
    WARNING = 3     # this level is used to print warnings about the execution of the program (non-blocking, but may lead to errors)
    ERROR = 4       # this level is used to print errors that may lead to the termination of the program
    CRITICAL = 5    # this level is used to print critical errors that lead to the termination of the program, typically used in largest except block
    
    
    @staticmethod
    def from_string(level : str) -> 'LEVELS':
        match level.lower():
            case 'deep_debug':
                return LEVELS.DEEP_DEBUG
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

    def __str__(self) -> str:
        """
        Return the string representation of the level, serialized to 10 characters (centered with spaces)
        """
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

    def __le__(self, other : 'LEVELS'):
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
    
class SENSITIVE_LEVELS(Enum):
    HIDE = 10
    SHOW = 11
    
    @staticmethod
    def from_string(level : str) -> 'SENSITIVE_LEVELS':
        match level.lower():
            case 'hide':
                return SENSITIVE_LEVELS.HIDE
            case 'show':
                return SENSITIVE_LEVELS.SHOW
            case _:
                return SENSITIVE_LEVELS.HIDE
    
    @staticmethod
    def from_bool(value : bool) -> 'SENSITIVE_LEVELS':
        return SENSITIVE_LEVELS.SHOW if value else SENSITIVE_LEVELS.HIDE
    
class TERMINAL_TARGETS(Enum):
    STDOUT = 30
    STDERR = 31
    
    def __str__(self) -> str:
        match self:
            case TERMINAL_TARGETS.STDOUT:
                return 'stdout'
            case TERMINAL_TARGETS.STDERR:
                return 'stderr'
            
    @staticmethod
    def from_string(target : str) -> 'TERMINAL_TARGETS':
        match target.lower():
            case 'stdout':
                return TERMINAL_TARGETS.STDOUT
            case 'stderr':
                return TERMINAL_TARGETS.STDERR
            case _:
                raise ValueError(f"Invalid terminal target: {target}")

class Target:
    __instances = {} #type: dict[str, Target]
    
    class Type(Enum):
        FILE = 20
        TERMINAL = 21
        
        def __str__(self) -> str:
            match self:
                case Target.Type.FILE:
                    return 'file'
                case Target.Type.TERMINAL:
                    return 'terminal'
    
    def __new__(cls, target : Callable[[str], None] | TERMINAL_TARGETS, name : str = None):
        if name is None:
            if isinstance(target, TERMINAL_TARGETS):
                name = name if name is not None else str(target)
            elif hasattr(target, '__name__'):
                name = target.__name__
            else:
                raise ValueError("The target must be a function or a TERMINAL_TARGETS; use Target.fromFile(file) to create a file target")
        if target in cls.__instances:
            return cls.__instances[name]
        instance = super().__new__(cls)
        cls.__instances[name] = instance
        return instance
    
    def __init__(self, target : Callable[[str], None] | TERMINAL_TARGETS, name : str = None):
        
        if isinstance(target, str):
            raise ValueError("The target must be a function or a TERMINAL_TARGETS; use Target.fromFile(file) to create a file target")
        
        targetFunc = target
        if isinstance(target, TERMINAL_TARGETS):
            match target:
                case TERMINAL_TARGETS.STDOUT:
                    targetFunc = sys.stdout.write
                case TERMINAL_TARGETS.STDERR:
                    targetFunc = sys.stderr.write
            self.__type = Target.Type.TERMINAL
            self.__name = name if name is not None else str(target)
        else:
            self.__type = Target.Type.FILE
            self.__name = name if name is not None else target.__name__

        self.target = targetFunc
        self.properties = {} #type: dict[str, any]
        self.__lock = threading.Lock()

    @staticmethod
    def fromFile(file : str) -> 'Target':
        def writeToFile(string : str):
            with open(file, 'a') as f:
                f.write(string)
        with open(file, 'w') as f: # clear the file
            f.write('')
        return Target(writeToFile, file)

    @staticmethod
    def fromJson(data: str|dict) -> 'Target':
        """
        examples of json data:
        File:
        ```json
        {
            "file": "log.txt",
            "level": "info",
            "sensitiveMode": "hide"
        }
        ```
        Stdout (console):
        ```json	
        {
            "name": "stdout",
            "terminal": "stdout"
        }
        ```
        """
        if isinstance(data, str):
            with open(data, 'r') as f:
                data = loads(f.read()) #type: dict
                
        result = None #type: Target
                
        if 'file' in data:
            result = Target.fromFile(data['file'])
        elif 'terminal' in data:
            result = Target(TERMINAL_TARGETS.from_string(data['terminal']))
        else:
            raise ValueError("The target must be a file or a terminal")
        
        if 'name' in data:
            result.name = data['name']
        
        result["level"] = LEVELS.from_string(data['level']) if 'level' in data else LEVELS.INFO
        result["sensitiveMode"] = SENSITIVE_LEVELS.from_string(data['sensitiveMode']) if 'sensitiveMode' in data else SENSITIVE_LEVELS.HIDE
        
        return result

    @staticmethod
    def fromXml(data: str|ElementTree.Element) -> 'Target':
        """
        examples of xml data:
        File:
        ```xml
        <target level="info" sensitiveMode="hide" file="log.txt"/>
        ```
        Stdout (console):
        ```xml
        <target name="stdout" terminal="stdout"/>
        ```
        """
        if isinstance(data, str):
            data = ElementTree.parse(data).getroot()
        
        result = None
        
        if data.tag != 'target':
            raise ValueError("The root element must be 'target'")
        
        if "file" in data.attrib:
            result = Target.fromFile(data.attrib['file'])
        elif "terminal" in data.attrib:
            result = Target(TERMINAL_TARGETS.from_string(data.attrib['terminal']))
        else:
            raise ValueError("The target must be a file or a terminal")
        
        if 'name' in data.attrib:
            result.name = data.attrib['name']
            
        result["level"] = LEVELS.from_string(data.attrib['level']) if 'level' in data.attrib else LEVELS.INFO
        result["sensitiveMode"] = SENSITIVE_LEVELS.from_string(data.attrib['sensitiveMode']) if 'sensitiveMode' in data.attrib else SENSITIVE_LEVELS.HIDE
        
        return result
            

    def __call__(self, string : str):
        with self.__lock: # prevent multiple threads to write at the same time
            self.target(string)
        
    def __str__(self) -> str:
        return self.__name
    
    def __repr__(self) -> str:
        return f"Target({self.__name})"
    
    def __getitem__(self, key: str) -> any:
        return self.properties[key]
    
    def __setitem__(self, key: str, value: any):
        self.properties[key] = value
        
    def __delitem__(self, key: str):
        del self.properties[key]
        
    def __contains__(self, key: str) -> bool:
        return key in self.properties
    
    @property
    def type(self) -> 'Target.Type':
        return self.__type

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name : str):
        old_name = self.__name
        self.__name = name
        del Target.__instances[old_name]
        Target.__instances[name] = self
        
    def delete(self):
        Target.unregister(self)

    
    @staticmethod
    def get(name : str | TERMINAL_TARGETS) -> 'Target':
        name = str(name)
        if Target.exist(name):
            return Target.__instances[name]
        else:
            raise ValueError(f"Target {name} does not exist")
    
    @staticmethod
    def exist(name : str | TERMINAL_TARGETS) -> bool:
        name = str(name)
        return name in Target.__instances.keys()
    
    @staticmethod
    def list() -> list['Target']:
        return list(Target.__instances.keys())
    
    @staticmethod
    def clear():
        Target.__instances = {}
        
    @staticmethod
    def register(target : 'Target'):
        Target.__instances[target.name] = target
        
    @staticmethod
    def unregister(target):
        if isinstance(target, str):
            name = target
        else:
            name = target.name
        if Target.exist(name):
            del Target.__instances[name]
        else:
            raise ValueError(f"Target {name} does not exist")
        

class LoggerConfig:
    def __init__(self, sensitiveDatas : list[str] = [], targets : list[Target] = []):
        self.sensitiveDatas = sensitiveDatas
        self.targets = targets
        self.showThreadsName = False
        self.showProcessName = False
        
        
    def clear(self):
        self.sensitiveDatas = []
        self.targets = []
        self.showThreadsName = False
        self.showProcessName = False
        
    @staticmethod
    def fromJson(data : str|dict, filePath : str = None) -> 'LoggerConfig':
        """
        examples of json data:
        ```json
        {
            "sensitiveDatas": ["password", "token"],
            "targets": [
                {
                    "file": "log.txt",
                    "level": "info",
                    "sensitiveMode": "hide"
                },
                {
                    "name": "stdout",
                    "terminal": "stdout"
                }
            ]
        }
        """
        if isinstance(data, str):
            filePath = data
            with open(data, 'r') as f:
                data = loads(f.read()) #type: dict
            
        elif filePath is None:
            raise ValueError("The filePath must be provided when the data is a dict")
        
        filePath = os.path.abspath(filePath)
        folderPath = os.path.dirname(filePath)
        
        sensitiveDatas = []
        targets = []
        
        if 'sensitiveDatas' in data:
            sensitiveDatas = data['sensitiveDatas']
        if 'targets' in data:
            targets = [Target.fromJson(target) for target in data['targets']]
        
        return LoggerConfig(sensitiveDatas, targets)
    
    @staticmethod
    def fromXml(data : str|ElementTree.Element, filePath : str = None) -> 'LoggerConfig':
        """
        examples of xml data:
        ```xml
        <config>
            <sensitiveDatas>
                <data>password</data>
                <data>token</data>
            </sensitiveDatas>
            <targets>
                <target file='log.txt' level='info' sensitiveMode='hide'/>
                <target terminal='stdout' name='stdout'/>
            </targets>
        </config>
        """
        if isinstance(data, str):
            filePath = data
            data = ElementTree.parse(data).getroot()
            
        elif filePath is None:
            raise ValueError("The filePath must be provided when the data is a ElementTree.Element")
        
        filePath = os.path.abspath(filePath)
        
        sensitiveDatas = []
        targets = []
        
        if data.find('sensitiveDatas') is not None:
            sensitiveDatas = [sensitiveData.text for sensitiveData in data.find('sensitiveDatas')]
        if data.find('targets') is not None:
            targets = [Target.fromXml(target) for target in data.find('targets')]
        
        return LoggerConfig(sensitiveDatas, targets)
    
    @staticmethod
    def fromConfigFile(filePath : str) -> 'LoggerConfig':
        if filePath.endswith('.json'):
            return LoggerConfig.fromJson(filePath)
        elif filePath.endswith('.xml'):
            return LoggerConfig.fromXml(filePath)
        else:
            raise ValueError("The file must be a json or xml file")
            
    
    def deleteTarget(self, name : str):
        for target in self.targets:
            if target.name == name:
                self.targets.remove(target)
                return
        raise ValueError(f"Target {name} not found")
    
    
    @staticmethod
    def configArgParse(parser : argparse.ArgumentParser) -> argparse._ArgumentGroup:
        """Add the logger configuration arguments to an argparse parser

        Args:
            parser (argparse.ArgumentParser): The parser to which the arguments will be added

        Returns:
            argparse._ArgumentGroup: The group of arguments added to the parser
        """
        masterGroup = parser.add_argument_group('Logger configuration')
        
        masterGroup.add_argument('--config', '-c', type=str, help='The path to the logger configuration file (json or xml)')
        
        masterGroup.add_argument('--sensitiveDatas', '-d', nargs='+', help='The list of sensitive datas to hide in the logs, separated by spaces')
        masterGroup.add_argument('--addTarget', '-t', action="append", nargs='+', help='Add a target to the logger, the arguments are the target configuration (in order: target (stdout, stderr or filename), level (deep-debug, debug, info, warning, error, critical), sensitiveMode (hide, show), sensitiveDatas (list of sensitive datas to hide), name) All arguments are optional exept the target')
                
        return masterGroup
    
    def parseArgs(self, args : argparse.Namespace):
        if args.config is not None:
            newConfig = LoggerConfig.fromConfigFile(args.config)
            self.sensitiveDatas = newConfig.sensitiveDatas
            self.targets = newConfig.targets
            self.moduleMap = newConfig.moduleMap
            
        if args.sensitiveDatas is not None:
            self.sensitiveDatas = args.sensitiveDatas
            
        if args.addTarget is not None:
            defaultParams = [None, 'info', 'hide', [], None]
            for targetArgs in args.addTarget:
                params = defaultParams.copy()
                params[:len(targetArgs)] = targetArgs #merge the two lists
                target = None
                if params[0] in ('stdout', 'stderr'):
                    target = Target(TERMINAL_TARGETS.from_string(params[0]), params[4])
                else:
                    target = Target.fromFile(params[0])
                    if params[4] is not None:
                        target.name = params[4]
                target["level"] = LEVELS.from_string(params[1])
                target["sensitiveMode"] = SENSITIVE_LEVELS.from_string(params[2])
                target["sensitiveDatas"] = params[3]
            
                if target.name in [t.name for t in self.targets]:
                    self.targets[[t.name for t in self.targets].index(target.name)] = target
                else:
                    self.targets.append(target)
    
    def __getitem__(self, key: str) -> any:
        match key:
            case 'sensitiveDatas':
                return self.sensitiveDatas
            case 'targets':
                return self.targets
            case 'showThreadsName':
                return self.showThreadsName
            case 'showProcessName':
                return self.showProcessName
            case _:
                raise KeyError(f"Parameter {key} not found")
            
    def __setitem__(self, key: str, value: any):
        match key:
            case 'sensitiveDatas':
                self.sensitiveDatas = value
            case 'targets':
                self.targets = value
            case 'showThreadsName':
                self.showThreadsName = value
            case 'showProcessName':
                self.showProcessName = value
            case _:
                raise KeyError(f"Parameter {key} not found")
            
    def __str__(self):
        return f"LoggerConfig(sensitiveDatas={self.sensitiveDatas}, targets={list(map(str, self.targets))}, showThreadsName={self.showThreadsName}, showProcessName={self.showProcessName})"
            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Logger configuration')
    LoggerConfig.configArgParse(parser)
    args = parser.parse_args()
    config = LoggerConfig()
    config.parseArgs(args)