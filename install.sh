#!/bin/bash

FILE=env/

if [ ! -d "$FILE" ]; then
    python3 -m venv env
fi

source env/bin/activate &&
pip install -U pip &&
pip install -Ur requirements.txt --use-feature=2020-resolver
