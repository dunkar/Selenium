#!/usr/bin/env bash
if [ -f $(which python3) ]; then
    py=$(which python3)
elif [[ "$(python --version)" =~ "^Python 3.*" ]]; then
    py=$(which python)
else
    exit 1
fi

$py -m http.server 8000
