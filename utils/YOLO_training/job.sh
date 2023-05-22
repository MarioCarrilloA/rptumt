#!/bin/bash

cd "yolov5"
pip install -r requirements.txt
pip install opencv-python-headless
pip install tensorboard==2.4.1
pip install protobuf==3.20.1
echo "running YOLO!!!!!"
echo "---------->"

#python train.py --data 3DSCC.yaml  --img 640 --cache
#python train.py --data 3DSCC.yaml --cfg yolov5n.yaml --img 640 --cache
#python train.py --data 3DSCC.yaml --cfg yolov5s.yaml --img 640 --cache
#python train.py --data 3DSCC.yaml --cfg yolov5m.yaml --img 640 --cache
#python train.py --data 3DSCC.yaml --cfg yolov5l.yaml --img 640 --cache
python train.py --data 3DSCC.yaml --cfg yolov5x.yaml --img 640 --cache
