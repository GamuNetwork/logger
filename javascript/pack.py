from builderTool import BaseBuilder, NULL_TARGET, Logger
import shutil, os
from tempfile import mkstemp

class Builder(BaseBuilder):
    def Setup(self):
        Logger.debug("Copying LICENSE, package.json and package-lock.json")
        shutil.copyfile("../LICENSE", self.tempDir+"/LICENSE")
        self.CopyAndReplaceByPackageVersion("package.json", self.tempDir+"/package.json")
        self.CopyAndReplaceByPackageVersion("package-lock.json", self.tempDir+"/package-lock.json")
        
        Logger.debug("Copying config files")
        shutil.copytree("config", self.tempDir+"/config")
        
        # copy sources
        Logger.debug("Copying sources")
        shutil.copytree("src", self.tempDir+"/src")        
        
        #install node modules
        Logger.debug("Installing node modules")
        return self.runCommand("npm ci")
        
        
    def Build(self):
        
        Logger.debug("copying tsconfig.json")
        shutil.copyfile("tsconfig.json", self.tempDir+"/tsconfig.json")
        
        Logger.debug("Building project")
        return self.runCommand("npm run build")
        
        
        
    def Tests(self):
        Logger.debug("copying tests")
        shutil.copytree("tests", self.tempDir+"/tests")
        Logger.debug("Running tests")
        return self.runCommand(f"npm test")
    
    
    def Publish(self):
        self.runCommand(f"npm publish --access public")
        
BaseBuilder.execute()