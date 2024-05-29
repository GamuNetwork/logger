import os
import inspect
from datetime import datetime

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
    
