install: venv

venv:
	virtualenv venv
	venv/bin/pip install -r setup/pip-requirements.txt
