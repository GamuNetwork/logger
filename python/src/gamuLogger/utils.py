import os
import inspect
from datetime import datetime
from typing import Any
from json import JSONEncoder


def getCallerInfo():
    """
    Returns the absolute filename of the caller of the parent function
    
    > ⚠️ From the next version, this fuction will return a tuple (filepath, function_name) instead of just the filepath
    """
    return getCallerFilePath(inspect.stack())


def getCallerFilePath(stack = inspect.stack()) -> str:
    """
    Returns the absolute filepath of the caller of the parent function
    """
    return os.path.abspath(stack[2][1])

def getCallerFunctionName(stack = inspect.stack()):
    """
    Returns the name of the function that called this one, including the class name if the function is a method
    """
    if len(stack) < 2:
        return "main"
    caller = stack[1]
    caller_name = caller.function
    if caller_name == "<module>":
        return "main"
    
    parents = getAllParents(caller.filename, caller.lineno)[::-1]
    if len(parents) > 0:
        if caller_name == parents[-1]:
            return '.'.join(parents)
        else:
            return '.'.join(parents) + '.' + caller_name
    else:
        return caller_name
    

# def getCallerInfo():
#     return getCallerFilePath(inspect.stack()), getCallerFunctionName(inspect.stack())

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
                raise TypeError(f"Argument {i} of function {func.__name__} must be of type ("+", ".join(map(type2string, types)) + ")")
            
        for key, value in kwargs.items():
            types = func_args[key]
            if type(value) not in types and not Any in types:
                raise TypeError(f"Argument {key} of function {func.__name__} must be of type ("+", ".join(map(type2string, types)) + ")")
        
        return func(*args, **kwargs)
    return wrapper

def countLinesLength(string : str) -> list[int]:
    lines = string.split('\n')
    return [len(line) for line in lines]

def splitLongString(string : str, length : int = 100) -> str:
    """Split a long string into multiple lines, on spaces"""
    result = []
    if len(string) <= length:
        return string
    
    lines = [line.split(' ') for line in string.split('\n')]
    
    for line in lines:
        current_line = []
        for word in line:
            if len(word) > length:
                raise ValueError("A word is longer than the maximum length")
            if len(' '.join(current_line)) + len(word) > length:
                result.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        result.append(' '.join(current_line))
    return '\n'.join(result)

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




def getAllParents(filepath, lineno):
    """
    Get all parent classes of a class or method, based on indentation in the file
    """
    
    # Read
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Get the line
    line = lines[lineno-1]
    
    # Get the indentation
    indentation = len(line) - len(line.lstrip())
    
    # Get the parent classes
    parents = []
    for i in range(lineno-1, 0, -1):
        line = lines[i]
        if len(line) - len(line.lstrip()) < indentation:
            indentation = len(line) - len(line.lstrip())
            if "class" in line:
                parents.append(line.strip()[:-1].split(' ')[1])
    
    return parents


if __name__ == '__main__':
    print(getCallerInfo())
    
    class foo:
        print(getCallerInfo())
        def __init__(self):
            print(getCallerInfo())
        
        def toto(self):
            print(getCallerInfo())
            
        class bar:                
            def titi(self):
                print(getCallerInfo())
            
    def salut():
        print(getCallerInfo())
        
    f = foo()
    f.toto()
    f.bar().titi()
    salut()