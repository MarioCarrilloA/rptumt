#!/bin/bash

OUTDIR="images"
COUNTER_FILE="sample.txt"

if [ ! -d "$OUTDIR" ]; then
    mkdir $OUTDIR
fi

if [ ! -f "$COUNTER_FILE" ]; then
    echo 0 > $COUNTER_FILE
fi

COUNTER=$(cat $COUNTER_FILE)

OUT_IMAGE="${OUTDIR}/image_${COUNTER}.png"
echo "save $OUT_IMAGE"
raspistill -w 1280 -h 720 -ss 2400 -o $OUT_IMAGE

COUNTER=$(echo "$COUNTER + 1" | bc)
echo $COUNTER > $COUNTER_FILE
