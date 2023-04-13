#!/bin/bash

APP="app"

if [ ! -d "$APP" ]; then
    echo "error: appliaction directory no available"
    exit 1
fi

pushd "$APP"
python main.py
popd
