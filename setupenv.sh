#!/bin/sh

cd `dirname $0`

if [ "$1" = "recreate" ]; then
    rm -r .venv
fi

if [ ! -d .venv ]; then python3 -m virtualenv -p $(command -v python3) .venv; fi
source .venv/bin/activate
pip install -U pylint websockets requests
deactivate
