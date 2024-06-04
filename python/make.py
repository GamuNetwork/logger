import os
import sys
import shutil 
import argparse

FILEDIR = os.path.dirname(os.path.abspath(__file__))

def savePyproject():
    shutil.copyfile(f"{FILEDIR}/pyproject.toml", f"{FILEDIR}/pyproject.toml.save")
    
def restorePyproject():
    shutil.move(f"{FILEDIR}/pyproject.toml.save", f"{FILEDIR}/pyproject.toml")
    
def setProjectVersion(version : str):
    with open(f"{FILEDIR}/pyproject.toml", 'r') as file:
        data = file.read()
    data = data.replace('{version}', version)
    with open(f"{FILEDIR}/pyproject.toml", 'w') as file:
        file.write(data)
        
def createPackage():
    os.system(sys.executable + f" -m build {FILEDIR}")
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python project build script')
    parser.add_argument('--version', help='Set project version', default="0.0.0")
    args = parser.parse_args()
    
    savePyproject()
    setProjectVersion(args.version)
    createPackage()
    restorePyproject()