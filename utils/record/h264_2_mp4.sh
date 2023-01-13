#!/bin/bash

INPUT_H264_FILE="$1"
FPS=30

if [ -z "$INPUT_H264_FILE" ]; then
    echo "error: no input file"
    exit 1
fi

base="$(echo "$INPUT_H264_FILE" | cut -d"." -f 1)"
echo "converting $INPUT_H264_FILE to mp4"
MP4Box -add "${INPUT_H264_FILE}":fps=$FPS -new "${base}.mp4"
