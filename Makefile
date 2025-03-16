install: pyproject.toml
	pip install --upgrade pip &&\
	TMPDIR=/home/ec2-user/pip_cache pip install --cache-dir=/home/ec2-user/pip_cache --editable . &&\
	pip install --editable .[cli] &&\
	pip install --editable .[api] &&\
	pip install --editable .[test]
	
lint:
	pylint --disable=R,C src/dc_app/*.py &&\
	pylint --disable=R,C src/dc_app/*/*.py &&\
	pylint --disable=R,C tests/*.py

test:
	python -m pytest -vv --cov=src/dc_app tests

format:
	black src/dc_app/*.py &&\
	black src/dc_app/*/*.py &&\
	black tests/*.py

all:
	install lint format test
