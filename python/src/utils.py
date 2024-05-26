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

def parseMessage(message : str):
    return message.replace('\n', '\n' + ('\t' * 4)+' | ')

if __name__ == "__main__":
    print(getCallerInfo())
    