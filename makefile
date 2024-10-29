VERSION = 2.1.0


.PHONY: all server

all: server


server: server-build server-install

ensure_env_exists:
	@if [ ! -d "env" ]; then \
		python3 -m venv env; \
	fi

ensure_testenv_exists:
	@if [ ! -d "testenv" ]; then \
		python3 -m venv testenv; \
	fi

install_build_deps: ensure_env_exists
	env/bin/pip install -r requirements-dev.txt

server-build: ensure_env_exists install_build_deps
	env/bin/feanor python/pack.py --debug -pv $(VERSION)

server-install: ensure_testenv_exists
	testenv/bin/pip install dist/*.whl --force-reinstall
