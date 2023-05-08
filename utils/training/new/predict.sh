#!/bin/bash

cd "yolov5"
pip install -r requirements.txt
pip install opencv-python-headless
pip install tensorboard==2.4.1
pip install protobuf==3.20.1
echo "Prediction"
cd ..

#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'Tests/*.png'
#python yolov5/classify/predict.py --weights yolov5/yolov5s.pt --source Testing/image_1.png
#python yolov5/classify/predict.py --weights yolov5/yolov5s.pt --source Testing/image_2.png
#python yolov5/classify/predict.py --weights yolov5/yolov5s.pt --source Testing/image_3.png
#python yolov5/classify/predict.py --weights yolov5/yolov5s.pt --source Testing/image_4.png
#python yolov5/classify/predict.py --weights yolov5/yolov5s.pt --source Testing/image_5.png

# THESIS

#python yolov5/detect.py  --line-thickness 3 --weights yolov5/runs/train/exp/weights/best.pt --source 'Benchmark/*.png'

#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'beads_size_estimation/90um/*.png'
#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'beads_size_estimation/200um/*.png'
#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'beads_size_estimation/355um/*.png'
#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'beads_size_estimation/500um/*.png'



#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'sizes/90um/*.png'
#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'sizes/200um/*.png'
#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'sizes/355um/*.png'
#python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'sizes/500um/*.png'

python yolov5/detect.py --save-txt --weights yolov5/runs/train/exp/weights/best.pt --source 'bead_size_validation/*.png'

