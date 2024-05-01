#!/bin/bash

venv/bin/python3 setup.py clean --all
venv/bin/python3 setup.py build
venv/bin/python3 setup.py bdist_wheel
venv/bin/twine upload --repository nexus dist/scouter_agent_python-0.1.0-py3-none-any.whl
