import os
import inspect
from datetime import datetime
from typing import Any
from json import JSONEncoder

def getCallerInfo():
    """
    Returns the filename of the caller of the parent function
    """
    return os.path.basename(inspect.stack()[1][1])

def getTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def replaceNewLine(string : str, indent : int = 33):
    return string.replace('\n', '\n' + (' ' * indent) + '| ')


def centerString(string : str, length : int):
    return string.center(length)

def string2type(string : str):
    match string.lower().strip():
        case 'int':
            return int
        case 'str':
            return str
        case 'float':
            return float
        case 'bool':
            return bool
        case 'list':
            return list
        case 'dict':
            return dict
        case 'tuple':
            return tuple
        case 'set':
            return set
        case 'none':
            return None
        case _:
            return Any
        
def type2string(t : Any):
    match t:
        case None:
            return 'None'
        case _:
            return t.__name__

def getFunctionArguments(func) -> dict[str, list[type]]:
    signature =  str(inspect.signature(func))
    signature = signature[1:-1] # Remove parenthesis
    signature = signature.split(',')
    
    result = {}
    for arg in signature:
        arg = arg.strip()
        arg = arg.split('=')[0]
        arg = arg.split(':')
        arg = [elem.strip() for elem in arg]
        if len(arg) == 1:
            result[arg[0]] = [Any]
            continue
        types = arg[1]
        result[arg[0]] = [string2type(t) for t in types.split('|')]
        
    return result

def strictTypeCheck(func):
    def wrapper(*args, **kwargs):
        # Get the function arguments
        func_args = getFunctionArguments(func)
        
        # Check the arguments
        for i, arg in enumerate(args):
            types = func_args[list(func_args.keys())[i]]
            if type(arg) not in types and not Any in types:
                raise TypeError(f"Argument {i} of function {func.__name__} must be of type ({", ".join(map(type2string, types))})")
            
        for key, value in kwargs.items():
            types = func_args[key]
            if type(value) not in types and not Any in types:
                raise TypeError(f"Argument {key} of function {func.__name__} must be of type ({", ".join(map(type2string, types))})")
        
        return func(*args, **kwargs)
    return wrapper


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        # if we serialize an enum, just return the name
        if hasattr(o, '_name_'):
            return o._name_
        
        if hasattr(o, '__dict__'):
            return o.__dict__
        elif hasattr(o, '__str__'):
            return str(o)
        else:
            return super().default(o)

