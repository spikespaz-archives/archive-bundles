#! /usr/bin/sh

if [ ! -d "./.venv" ]; then
    python -m venv "./.venv"
    python -m pip install -r "requirements.txt"
fi

source "./.venv/Scripts/activate"
