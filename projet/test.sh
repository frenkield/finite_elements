#!/bin/bash

export PYTHONIOENCODING=utf8
export PYTHONPATH=src

python3 -m unittest discover -s test
