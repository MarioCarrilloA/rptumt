#!/bin/bash

YOLOV5_REPO="https://github.com/ultralytics/yolov5.git"
YOLOV5_WDIR="yolov5"

# YOLO working version
YOLOv5_TAG="v6.2"

# Check YOLOv5 code
if [ ! -d "YOLOV5_REPO" ]; then
    echo "downloading YOLOv5 code"
    git clone $YOLOV5_REPO
else
    echo "YOLOv5 code found"
fi

# Move to a specific version
pushd $YOLOV5_WDIR
    git checkout $YOLOv5_TAG
popd

