from builderTool import BaseBuilder, PYTHON, NULL_TARGET, Logger
import shutil


class Builder(BaseBuilder):
    def Setup(self):
        shutil.copytree('src', self.tempDir + '/src')
        self.CopyAndReplaceByPackageVersion('pyproject.toml', self.tempDir + '/pyproject.toml')
        shutil.copyfile('readme.md', self.tempDir + '/readme.md')
        shutil.copyfile('../LICENSE', self.tempDir + '/LICENSE')
        shutil.copyfile('install-requirements.txt', self.tempDir + '/install-requirements.txt')
        
        self.runCommand(f"{PYTHON} -m pip install -r install-requirements.txt")
        
    def Build(self):
        return self.runCommand(f"{PYTHON} -m build {self.tempDir} --outdir {self.distDir}")
    
    def Tests(self):
        shutil.copytree('tests', self.tempDir + '/tests')
        return self.runCommand(f"{PYTHON} -m pytest {self.tempDir}/tests")

BaseBuilder.execute()