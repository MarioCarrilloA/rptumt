import cv2
import logging
import numpy as np
from queue import Queue
#from multiprocessing import Queue
import time


SAMPLING_TIME = 1

class Camera():
    def __init__(self):
        self.capturing = False

        # Configuration
        self.width = 1280
        self.heigh = 720
        self.cap_api = cv2.CAP_V4L2
        self.cycle_time = 50
        self.exposure_time = 0 # Zero for automatic exposure time
        self.camera_number = 1
        self.image_queue = Queue()


    def _create_video_capture(self):
        cap = cv2.VideoCapture(self.camera_number - 1 + self.cap_api)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.heigh)
        if self.exposure_time:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
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

