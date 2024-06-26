from builderTool import BaseBuilder, Logger

class Builder(BaseBuilder):
    def Setup(self):
        self.addFile("../LICENSE", "/LICENSE")
        self.addAndReplaceByPackageVersion("package.json", self.tempDir+"/package.json")
        self.addAndReplaceByPackageVersion("package-lock.json", self.tempDir+"/package-lock.json")
        self.addDirectory("config")
        self.addDirectory("src")       
        self.addFile("tsconfig.json") 
        
        #install node modules
        Logger.debug("Installing node modules")
        return self.runCommand("npm ci")
        
        
    def Build(self):
        return self.runCommand("npm run build")
        
        
        
    def Tests(self):
        self.addDirectory("tests")
        return self.runCommand(f"npm test")
    
    
    def Publish(self):
        self.runCommand(f"npm publish --access public")
        
BaseBuilder.execute()