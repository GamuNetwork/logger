# run `make` to install the package to test it
#! THIS SCRIPT IS NOT USED IN THE WORKFLOW

all: copy_pyproject tweak_pyproject install restore_pyproject


copy_pyproject: pyproject.toml
	cp pyproject.toml pyproject.toml.save

tweak_pyproject: pyproject.toml
	sed -i "s/{version}/0.0.0/g" pyproject.toml

restore_pyproject: pyproject.toml
	mv pyproject.toml.save pyproject.toml

install:
	pip install -r requirements.txt
	python -m build .
