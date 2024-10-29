from feanor import BaseBuilder

class Builder(BaseBuilder):
    def Setup(self):
        self.addDirectory("src")
        self.addFile("release.md", "/readme.md")
        self.addAndReplaceByPackageVersion('src/gamuLogger/__init__.py')
        
        self.addAndReplaceByPackageVersion('pyproject.toml')
        self.addFile('../LICENSE', 'LICENSE')
        
    def Build(self):
        self.venv().install('build')
        self.venv().runModule('build', '--outdir', f"{self.distDir}")
        
    def Tests(self):
        self.addDirectory('tests')
        self.venv().install('pytest')
        self.venv().runModule('pytest', f"{self.tempDir}/tests")
