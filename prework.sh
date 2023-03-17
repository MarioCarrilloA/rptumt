#!/bin/bash

set -e

YOLOV5_REPO_URL="https://github.com/ultralytics/yolov5.git"
YOLOV5_REPO_DIR="yolov5"
YOLOv5_TAG="v6.2"
YOLOV5_WORKDIR="yolov5_upstream"
APP_CODE="app"
BENCHMARK_CODE="benchmark"
TMP="tmp"

if [ -d "$TMP" ]; then
    echo "preprocess step already executed!"
    exit 1
fi

# Download YOLOv5 code from upstream
mkdir "$TMP"
echo "Download YOLOv5 source code"
pushd "$TMP"
git clone "$YOLOV5_REPO_URL"
pushd "$YOLOV5_REPO_DIR"
echo "switch to tag: $YOLOv5_TAG"
git checkout $YOLOv5_TAG -q
popd
popd

# Prepare output directories
if [ ! -d "$APP_CODE/$YOLOV5_WORKDIR" ]; then
    mkdir -p "$APP_CODE/$YOLOV5_WORKDIR"
fi

if [ ! -d "$BENCHMARK_CODE/$YOLOV5_WORKDIR" ]; then
    mkdir -p "$BENCHMARK_CODE/$YOLOV5_WORKDIR"
fi

# Copy relevant code for detection
echo "copy relevant code for prediction"
cp -r "$TMP/$YOLOV5_REPO_DIR/models" "$APP_CODE/$YOLOV5_WORKDIR"
cp -r "$TMP/$YOLOV5_REPO_DIR/utils" "$APP_CODE/$YOLOV5_WORKDIR"
cp -f "$TMP/$YOLOV5_REPO_DIR/export.py" "$APP_CODE/$YOLOV5_WORKDIR"
cp -f "$TMP/$YOLOV5_REPO_DIR/detect.py" "$APP_CODE/$YOLOV5_WORKDIR"
cp -r "$TMP/$YOLOV5_REPO_DIR/models" "$BENCHMARK_CODE/$YOLOV5_WORKDIR"
cp -r "$TMP/$YOLOV5_REPO_DIR/utils" "$BENCHMARK_CODE/$YOLOV5_WORKDIR"
cp -f "$TMP/$YOLOV5_REPO_DIR/export.py" "$BENCHMARK_CODE/$YOLOV5_WORKDIR"
cp -f "$TMP/$YOLOV5_REPO_DIR/detect.py" "$BENCHMARK_CODE/$YOLOV5_WORKDIR"

echo "finish successfully"
