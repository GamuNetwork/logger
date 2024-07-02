from builderTool import BaseBuilder, PYTHON


class Builder(BaseBuilder):
    def Setup(self):
        self.addDirectory("src")
        self.addAndReplaceByPackageVersion('src/gamuLogger/__init__.py')
        
        self.addAndReplaceByPackageVersion('pyproject.toml')
        self.addFile('readme.md')
        self.addFile('../LICENSE', 'LICENSE')
        self.addFile('install-requirements.txt')
        
        self.runCommand(f"{PYTHON} -m pip install -r install-requirements.txt")
        
    def Build(self):
        self.runCommand(f"{PYTHON} -m build {self.tempDir} --outdir {self.distDir}")
    
    def Tests(self):
        self.addDirectory('tests')
        self.runCommand(f"{PYTHON} -m pytest {self.tempDir}/tests")

BaseBuilder.execute()
