
from guiapp import *

import datetime
import logging
import random
import sys
import time
import numpy as np
import cv2
#import qimage2ndarray
import time
from datetime import datetime
import random
import string
import pyqtgraph

from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor

import threading

from PyQt5 import QtCore, QtGui, QtWidgets
import queue as Queue



#import sys, time, threading, cv2
#try:
#    from PyQt5.QtCore import Qt
#    pyqt5 = True
#except:
#    pyqt5 = False
#if pyqt5:
#    from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
#    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
#    from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
#    from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor
#else:
#    from PyQt4.QtCore import Qt, pyqtSignal, QTimer, QPoint
#    from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit, QLabel
#    from PyQt4.QtGui import QWidget, QAction, QVBoxLayout, QHBoxLayout
#    from PyQt4.QtGui import QFont, QPainter, QImage, QTextCursor
#try:
#import Queue as Queue

#except:



#IMG_SIZE    = 1280,720          # 640,480 or 1280,720 or 1920,1080
#IMG_FORMAT  = QImage.Format_RGB888
DISP_SCALE  = 1                # Scaling factor for display image
DISP_MSEC   = 50                # Delay between display cycles
#CAP_API     = cv2.CAP_ANY       # API: CAP_ANY or CAP_DSHOW etc...
CAP_API     = cv2.CAP_V4L2       # API: CAP_ANY or CAP_DSHOW etc...
EXPOSURE    = 0                 # Zero for automatic exposure
#EXPOSURE    = 2400                 # Zero for automatic exposure
TEXT_FONT   = QFont("Courier", 10)

camera_num  = 1                 # Default camera (first in list)
image_queue = Queue.Queue()     # Queue to hold images
#capturing   = True              # Flag to indicate capturing


Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot



SAMPLING_TIME = 1


class Camera():
    def __init__(self):
        self.capturing = False
        self.width = 1280
        self.heigh = 720

    def grab_images(self, cam_num, queue):
        cap = cv2.VideoCapture(cam_num-1 + CAP_API)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.heigh)
        if EXPOSURE:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
        else:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

        #self.console.log_msg(logging.INFO, "capturing frames")
        #self.console.log_msg(logging.INFO, "capturing frames")
        logging.info("capturing frames")
        while self.capturing:
            if cap.grab():
                retval, image = cap.retrieve(0)
                if image is not None and queue.qsize() < 2:
                    queue.put(image)
                else:
                    time.sleep(DISP_MSEC / 1000.0)
            else:
                logging.error("cannot grab frames from camera, session cancelled!")
                #self.console.log_msg(logging.ERROR, "cannot grab frames from camera, session cancelled!")
                break
        cap.release()

        img = np.zeros([self.heigh, self.width, 3], dtype=np.uint8)
        queue.put(img)


    def grab_sample_image(self, cam_num):
        cap = cv2.VideoCapture(cam_num-1 + CAP_API)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.heigh)
        if EXPOSURE:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
        else:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

        #self.console.log_msg(logging.INFO, "getting frame from camera")
        logging.info("getting frame from camera")
        if cap.grab():
            retval, image = cap.retrieve(0)
            cap.release()
            if image is not None:
                return image
            else:
                None

    def disable_capture(self):
        self.capturing = False

    def enable_capture(self):
        self.capturing = True


