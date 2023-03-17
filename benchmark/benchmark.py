import argparse
import os
import sys
import time
from yolov5_upstream import detect

YOLOV5_MODELS_PATH="YOLOv5_trained_models"
BENCHMARK_INPUTS="benchmark_inputs"
WEIGHTS_PATH="output/weights/best.pt"

def execute_benchmark(model_size, weights):
    print("weights: " + weights)
    fstats = os.stat(weights)
    print("File size: {:.4f} MB".format((fstats.st_size/1024)/1024))

    inputs = BENCHMARK_INPUTS + "/*.png"
    outputs = "./results" + "/" + model_size
    st = time.time()
    detect.run(
        weights=weights,
        source=inputs,
        hide_conf=True,
        hide_labels=False,
        line_thickness=1,
        save_txt=False,
        project=outputs
    )
    et = time.time()
    elapsed_time = et - st
    print("ELAPSED TIME: " + str(elapsed_time))


def main(args):
    model_size = str(args.size)
    weights = ""
    if model_size == "default":
        weights = YOLOV5_MODELS_PATH + "/default/" + WEIGHTS_PATH

    elif model_size == "nano":
        weights = YOLOV5_MODELS_PATH + "/nano/" + WEIGHTS_PATH

    elif model_size == "small":
        weights = YOLOV5_MODELS_PATH + "/small/" + WEIGHTS_PATH

    elif model_size == "medium":
        weights = YOLOV5_MODELS_PATH + "/medium/" + WEIGHTS_PATH

    elif model_size == "large":
        weights = YOLOV5_MODELS_PATH + "/large/" + WEIGHTS_PATH

    elif model_size == "extra":
        weights = YOLOV5_MODELS_PATH + "/extra/" + WEIGHTS_PATH

    else:
        print("error: invalid model size!")
        sys.exit(3)

    execute_benchmark(model_size, weights)

if __name__ == '__main__':
    if (os.path.exists(YOLOV5_MODELS_PATH) == False):
        print("error: yolov5 models path no found!")
        sys.exit(1)

    if (os.path.exists(BENCHMARK_INPUTS) == False):
        print("error: benchmark inputs path no found!")
        sys.exit(2)

    cmdhelp="YOLOv5 model size [default|nano|small|medium|large|extra]"
    parser = argparse.ArgumentParser(description="3DSCC benachmark")
    parser.add_argument('--size', required=True, help=cmdhelp)
    args = parser.parse_args()
    main(args)
