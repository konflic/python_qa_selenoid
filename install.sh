#!/bin/bash

FILE=env/

if [ -d "$FILE" ]; then
    source env/bin/activate &&
    pip install -U pip &&
    pip install -Ur requirements.txt
else
    python3 -m venv env &&
    source env/bin/activate &&
    pip install -U pip &&
    pip install -Ur requirements.txt
fi
