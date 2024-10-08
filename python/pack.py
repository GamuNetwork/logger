from feanor import BaseBuilder

class Builder(BaseBuilder):
    def Setup(self):
        self.addDirectory("src")
        self.addFile("release.md", "/readme.md")
        self.addAndReplaceByPackageVersion('src/gamuLogger/__init__.py')
        
        self.addAndReplaceByPackageVersion('pyproject.toml')
        self.addFile('../LICENSE', 'LICENSE')
        
        self.venv().install('build==1.2.1')
        self.venv().install('pytest==8.2.2')
        
    def Build(self):
        self.venv().runModule(f"build {self.tempDir} --outdir {self.distDir}")
    
    def Tests(self):
        self.addDirectory('tests')
        self.venv().runModule(f"pytest {self.tempDir}/tests")
