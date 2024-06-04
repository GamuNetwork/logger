import os
import sys
import shutil 
import argparse
import re

FILEDIR = os.path.dirname(os.path.abspath(__file__))

PYPROJECT_PATH = f"{FILEDIR}/pyproject.toml"

def savePyproject():
    shutil.copyfile(PYPROJECT_PATH, PYPROJECT_PATH + ".save")
    
def restorePyproject():
    shutil.move(PYPROJECT_PATH + ".save", PYPROJECT_PATH)
    
def setProjectVersion(version : str):
    with open(PYPROJECT_PATH, 'r') as file:
        data = file.read()
    data = data.replace('{version}', version)
    with open(PYPROJECT_PATH, 'w') as file:
        file.write(data)
        
def createPackage():
    os.system(sys.executable + f" -m build {FILEDIR}")
    
    
    
if __name__ == '__main__':
    def getArgs() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Python project build script')
        parser.add_argument('-pv', help='Set project version', default="0.0.0", type=str, metavar='x.y.z')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
        args = parser.parse_args()
        
        if not re.match(r"\d+\.\d+\.\d+", args.pv):
            print("Invalid version format; must be in the form of 'x.y.z', where x, y, and z are integers")
            sys.exit(1)
        
        return args

    args = getArgs()
    
    savePyproject()
    setProjectVersion(args.pv)
    createPackage()
    restorePyproject()