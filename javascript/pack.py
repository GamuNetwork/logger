import os
import sys
import shutil 
import argparse
import re

FILEDIR = os.path.dirname(os.path.abspath(__file__))

TSCONFIG_PATH = f"{FILEDIR}/tsconfig.json"

def runTests() -> bool:
    return os.system("npm test") == 0

def savePyproject():
    shutil.copyfile(TSCONFIG_PATH, TSCONFIG_PATH + ".save")
    
def restorePyproject():
    shutil.move(TSCONFIG_PATH + ".save", TSCONFIG_PATH)
    
def setProjectVersion(version : str):
    with open(TSCONFIG_PATH, 'r') as file:
        data = file.read()
    data = data.replace('{version}', version)
    with open(TSCONFIG_PATH, 'w') as file:
        file.write(data)
        
def createPackage():
    os.system("npm run build")
    
    
    
if __name__ == '__main__':
    def getArgs() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Python project build script')
        parser.add_argument('-pv', help='Set project version', default="0.0.0", type=str, metavar='x.y.z')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
        parser.add_argument('-nt', '--no-tests', help='Do not run tests', action='store_true')
        parser.add_argument('-nb', '--no-build', help='Do not build package', action='store_true')
        args = parser.parse_args()
        
        if not re.match(r"\d+\.\d+\.\d+", args.pv):
            print("Invalid version format; must be in the form of 'x.y.z', where x, y, and z are integers")
            sys.exit(1)
        
        return args

    args = getArgs()
    
    if not args.no_tests:
        if not runTests():
            exit(1)

    if not args.no_build:
        savePyproject()
        setProjectVersion(args.pv)
        createPackage()
        restorePyproject()