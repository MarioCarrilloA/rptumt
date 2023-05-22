#!/bin/bash

cd "yolov5"
pip install -r requirements.txt
pip install opencv-python-headless
pip install tensorboard==2.4.1
pip install protobuf==3.20.1
echo "Prediction"
cd ..

python yolov5/detect.py --weights yolov5/runs/train/exp18/weights/best.pt --source 'Testing/*.png'
