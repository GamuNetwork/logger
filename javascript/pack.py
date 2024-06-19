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
        os.system(f"cd {self.tempDir} && npm install > {NULL_TARGET}")
        
        
    def Build(self):
        fd, logfile = mkstemp()
        
        Logger.debug("Cpoying tsconfig.json")
        shutil.copyfile("tsconfig.json", self.tempDir+"/tsconfig.json")
        
        Logger.debug("Building project")
        exitCode = os.system(f"cd {self.tempDir} && npm run build > {logfile}") # build to dist directory in temp, for publishing
        if exitCode != 0:
            Logger.error("Build failed : \n"+open(logfile).read())
            os.remove(logfile)
            return False
        os.remove(logfile)
        return True

        
    def Tests(self):
        Logger.debug("copying tests")
        shutil.copytree("tests", self.tempDir+"/tests")
        Logger.debug("Running tests")
        return os.system(f"cd {self.tempDir} && npm test > {NULL_TARGET}") == 0
    
    
    def Publish(self):
        os.system(f"cd {self.tempDir} && npm publish --access public")
        
BaseBuilder.execute()