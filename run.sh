#!/bin/bash

APP="app"

if [ ! -d "$APP" ]; then
    echo "error: appliaction directory no available"
    exit 1
fi

pushd "$APP"
echo "Loading application ..."
python -W ignore main.py
popd
