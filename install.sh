#!/bin/bash

FILE=venv/

if [ ! -d "$FILE" ]; then
    python3 -m venv venv
fi

source venv/bin/activate &&
pip install -U pip &&
pip install -Ur requirements.txt
