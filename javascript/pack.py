from feanor import BaseBuilder

class Builder(BaseBuilder):
    def Setup(self):
        self.addFile("../LICENSE", "/LICENSE")
        self.addFile("release.md", "/readme.md")
        self.addAndReplaceByPackageVersion("package.json")
        self.addAndReplaceByPackageVersion("package-lock.json")
        self.addDirectory("config")
        self.addDirectory("src")       
        self.addFile("tsconfig.json") 
        
        self.runCommand("npm ci")
        
        
    def Build(self):
        self.runCommand("npm run build")
        self.runCommand(f'npm pack --pack-destination "{self.distDir}"')
        
        
    def BuildTests(self):
        self.addDirectory("tests")
        self.runCommand(f"npm test")
    
    
    def Publish(self):
        self.runCommand(f"npm publish --access public")
