import os
import random
import time
import tkinter
import RPi.GPIO as GPIO

from configparser import ConfigParser
from datetime import datetime
from picamera import PiCamera


# read configuration.ini for sampling configuration
config_object = ConfigParser()
config_object.read("/home/pi/Desktop/RESULTS/CONFIGURATION.ini")

# parse file
sampling_conf = config_object["SAMPLING_CONFIGURATION"]

TOTAL_NUM_SAMPLES = int(sampling_conf["total_samples"])
TIME_PER_CYCLE = int(sampling_conf["time_per_cycle"])
NUM_SAMPLES_PER_CYCLE = int(sampling_conf["num_samples_per_cycle"])

# Camera configuration
RESOLUTION = (1280, 720)
SHUTTER_SPEED = 2400
INIT_CAMERA_TIME = 5

# Sampling configuration
#TOTAL_NUM_SAMPLES = 50
#TIME_PER_CYCLE = 10
#NUM_SAMPLES_PER_CYCLE = 5

# Results configuration
RESULTS_PATH = "/home/pi/Desktop/RESULTS/Datasets/"

# GPIO number, do not confuse with number of pin
GPIO_NUM = 24

def turn_on_led():
    GPIO.output(GPIO_NUM, GPIO.HIGH)
    print("LED on")


def turn_off_led():
    print("LED off")
    GPIO.output(GPIO_NUM, GPIO.LOW)


def create_dataset_dir():
    now = datetime.now()
    dirname = RESULTS_PATH + "dataset_" + now.strftime("%d_%m_%Y-%H_%M_%S")
    try:
        os.mkdir(dirname)
        print("Directory:" , dirname, " created ") 
    except FileExistsError:
        print("Directory:" , dirname,  " already exists")

    return dirname

def main():
    # Setup GPIO for led
    print("Data collection V2.0")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_NUM, GPIO.OUT)
    turn_off_led()

    outdir = create_dataset_dir()
    wait_counter = 0
    init_process_flag = True
    samples = 1
    while (samples <= TOTAL_NUM_SAMPLES):
        if (init_process_flag == True or wait_counter == TIME_PER_CYCLE):
            print("starting the camera...")
            camera = PiCamera()
            camera.shutter_speed = SHUTTER_SPEED
            camera.resolution = RESOLUTION
            print("Shutter speed", camera.shutter_speed)

            # Camera preview
            root = tkinter.Tk()
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            camera.preview_fullscreen = False
            camera.preview_window = (round(ws/2), 160, 640, 360)

            wait_counter = 0
            if (init_process_flag == True):
                print("Starting first cycle")
                init_process_flag = False

            # Turn on light
            turn_on_led()
            camera.start_preview()
            print("waiting " + str(INIT_CAMERA_TIME) + " second to init camera")
            time.sleep(INIT_CAMERA_TIME)
            print("taking samples...!!!")
            now = datetime.now()
            for i in range(0, NUM_SAMPLES_PER_CYCLE):
                t = now.strftime("%d_%m_%Y-%H_%M_%S")
                outimg = outdir + "/" + "image_3DSSC_" + t + "_sample_" + str(samples) + ".png"
                camera.capture(outimg)
                # This time is random to avoid synchronization with the tube
                # rotation and therefore always get images from different views
                time_per_sample = round(random.uniform(0.1, 0.8), 2)
                print(str(time_per_sample) + ": " + outimg)
                time.sleep(time_per_sample)
                samples+=1
            turn_off_led()
            # Close camera
            camera.stop_preview()
            camera.close()
        print("second  " + str(wait_counter) + " of " + str(TIME_PER_CYCLE) + " for the next cycle")
        wait_counter+=1
        time.sleep(1)

    print("Dataset created successfully!")
    print("path:", outdir)


if __name__ == "__main__":
    main()
