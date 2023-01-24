#!/bin/bash

set -e

YOLOV5_REPO_URL="https://github.com/ultralytics/yolov5.git"
YOLOV5_REPO_DIR="yolov5"
YOLOv5_TAG="v6.2"
YOLOV5_WORKDIR="yolov5_upstream"
APP_CODE="app"

# Mode to application source code
pushd "$APP_CODE"
if [ ! -d "$YOLOV5_WORKDIR" ]; then
    echo "creating workspace for yolov5 code"
    mkdir "$YOLOV5_WORKDIR"
fi

pushd "$YOLOV5_WORKDIR"
if [ -d "$YOLOV5_REPO_DIR" ]; then
    echo "$(pwd)"
    echo "A directory with the same name of YOLOv5 repository already exist!"
    echo "exit..."
    exit 0
fi

git clone "$YOLOV5_REPO_URL"
pushd "$YOLOV5_REPO_DIR"
echo "switch to tag: $YOLOv5_TAG"
git checkout $YOLOv5_TAG -q
popd

# Copy relevant code for detection
cp -r "$YOLOV5_REPO_DIR/models" .
cp -r "$YOLOV5_REPO_DIR/utils" .
cp -f "$YOLOV5_REPO_DIR/export.py" .
cp -f "$YOLOV5_REPO_DIR/detect.py" .

popd

echo "finish successfully"

