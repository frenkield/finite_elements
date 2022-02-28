#!/bin/bash

export PYTHONIOENCODING=utf8
export PYTHONPATH=.:src

python3 src/questions/questions_main.py ${@:1}
