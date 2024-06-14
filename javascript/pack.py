import os
import sys
import shutil 
import argparse
import re

FILEDIR = os.path.dirname(os.path.abspath(__file__))

PACKAGE_JSON_PATH = f"{FILEDIR}/package.json"
PACKAGE_LOCK_JSON_PATH = f"{FILEDIR}/package-lock.json"

def runTests() -> bool:
    return os.system("npm test") == 0

def copyLicense() -> None:
    shutil.copyfile(f"{FILEDIR}/../LICENSE", f"{FILEDIR}/LICENSE")

def savePyproject():
    shutil.copyfile(PACKAGE_JSON_PATH, PACKAGE_JSON_PATH + ".save")
    shutil.copyfile(PACKAGE_LOCK_JSON_PATH, PACKAGE_LOCK_JSON_PATH + ".save")
    
def restorePyproject():
    shutil.move(PACKAGE_JSON_PATH + ".save", PACKAGE_JSON_PATH)
    shutil.move(PACKAGE_LOCK_JSON_PATH + ".save", PACKAGE_LOCK_JSON_PATH)
    
def setProjectVersion(version : str):
    for path in [PACKAGE_JSON_PATH, PACKAGE_LOCK_JSON_PATH]:
        with open(path, 'r') as file:
            data = file.read()
        data = data.replace('{version}', version)
        with open(path, 'w') as file:
            file.write(data)
        
def createPackage():
    os.system("npm run build")
    
def publishPackage():
    os.system("npm publish --access public")
    
class VersionedPyProject:
    def __init__(self, version : str, no_clean = False):
        self.version = version
        self.no_clean = no_clean
        
    def __enter__(self):
        savePyproject()
        setProjectVersion(self.version)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if not self.no_clean:
            restorePyproject()
    
    
    
if __name__ == '__main__':
    def getArgs() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Python project build script')
        parser.add_argument('-pv', help='Set project version', default="0.0.0", type=str, metavar='x.y.z')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
        parser.add_argument('-nt', '--no-tests', help='Do not run tests', action='store_true')
        parser.add_argument('-nb', '--no-build', help='Do not build package', action='store_true')
        parser.add_argument('-p', '--publish', help='Publish package', action='store_true')
        args = parser.parse_args()
        
        if not re.match(r"\d+\.\d+\.\d+", args.pv):
            print("Invalid version format; must be in the form of 'x.y.z', where x, y, and z are integers")
            sys.exit(1)
        
        return args

    args = getArgs()
    
    with VersionedPyProject(args.pv, True):
        if not args.no_tests:
            if not runTests():
                exit(1)

        if not args.no_build:
            createPackage()
        
        if args.publish: #not run by default
            publishPackage()
            