import cv2
import logging
import numpy as np
import os
import random
import time

from picamera2 import Picamera2
from queue import Queue
from datetime import datetime

SAMPLING_TIME = 1
CAMERA_PREPARATION_TIME = 2


class Camera():
    def __init__(self):
        self.capturing = False

        # Support for Opencv:
        # The camera can be handled by the official python
        # module of Raspberry Pi (picamera(2)). However, it
        # can be also handled by OpenCV.
        self.cap_api = cv2.CAP_V4L2
        self.image_queue = Queue()
        self.camera_number = 1

        # Configuration
        self.width = 1280
        self.heigh = 720
        self.cycle_time = 50
        self.exposure_time = 2400 # microseconds
        self.workspace_path = os.environ['HOME'] + "/" + "Workspace3DSC"
        now = datetime.now()
        self.experiment_id = self.workspace_path + "/" + "experiment_" + now.strftime("%d_%m_%Y-%H_%M_%S")

        # Create output paths
        if os.path.exists(self.workspace_path) == False:
            os.makedirs(self.workspace_path)

        if os.path.exists(self.experiment_id) == False:
            os.makedirs(self.experiment_id)


    def _get_configured_camera(self):
        camera = Picamera2()
        camera_config = camera.create_still_configuration(main={"size": (self.width, self.heigh)})
        camera.configure(camera_config)
        camera.set_controls({"ExposureTime": self.exposure_time})
        return camera


    def save_single_image(self):
        now = datetime.now()
        imgname = "sample.png"
        sample_path = self.experiment_id + "/" + "sample_" + now.strftime("%d_%m_%Y-%H_%M_%S")
        os.mkdir(sample_path)
        camera = self._get_configured_camera()
        camera.start()
        time.sleep(CAMERA_PREPARATION_TIME)
        camera.capture_file(sample_path + "/" + imgname)
        camera.stop()
        camera.close()
        return sample_path, imgname


    def grab_frames(self):
        camera = self._get_configured_camera()
        camera.start()
        logging.info("capturing frames")
        while self.capturing:
            image = camera.capture_array()
            if image is not None and self.image_queue.qsize() < 2:
                self.image_queue.put(image)
            else:
                time.sleep(self.cycle_time / 1000.0)
        camera.stop()
        camera.close()
        img = np.zeros([self.heigh, self.width, 3], dtype=np.uint8)
        self.image_queue.put(img)


    def _create_video_capture(self):
        cap = cv2.VideoCapture(self.camera_number - 1 + self.cap_api)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.heigh)
        if self.exposure_time:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, 2400)
        else:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        return cap


    def grab_images(self):
        cap = self._create_video_capture()
        logging.info("capturing frames")
        while self.capturing:
            if cap.grab():
                retval, image = cap.retrieve(0)
                if image is not None and self.image_queue.qsize() < 2:
                    self.image_queue.put(image)
                else:
                    time.sleep(self.cycle_time / 1000.0)
            else:
                logging.error("cannot grab frames from camera, session cancelled!")
                break
        cap.release()

        img = np.zeros([self.heigh, self.width, 3], dtype=np.uint8)
        self.image_queue.put(img)


    def grab_sample_image(self):
        cap = self._create_video_capture()
        logging.info("getting frame from camera")
        if cap.grab():
            retval, image = cap.retrieve(0)
            cap.release()
            return image
        return None


    def disable_capture(self):
        self.capturing = False


    def enable_capture(self):
        self.capturing = True

