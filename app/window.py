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

#VERSION = "Cam_display v0.10"

import sys, time, threading, cv2
try:
    from PyQt5.QtCore import Qt
    pyqt5 = True
except:
    pyqt5 = False
if pyqt5:
    from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
    from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
    from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor
else:
    from PyQt4.QtCore import Qt, pyqtSignal, QTimer, QPoint
    from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit, QLabel
    from PyQt4.QtGui import QWidget, QAction, QVBoxLayout, QHBoxLayout
    from PyQt4.QtGui import QFont, QPainter, QImage, QTextCursor
try:
    import Queue as Queue
except:
    import queue as Queue

IMG_SIZE    = 1280,720          # 640,480 or 1280,720 or 1920,1080
IMG_FORMAT  = QImage.Format_RGB888
DISP_SCALE  = 1                # Scaling factor for display image
DISP_MSEC   = 50                # Delay between display cycles
#CAP_API     = cv2.CAP_ANY       # API: CAP_ANY or CAP_DSHOW etc...
CAP_API     = cv2.CAP_V4L2       # API: CAP_ANY or CAP_DSHOW etc...
EXPOSURE    = 0                 # Zero for automatic exposure
#EXPOSURE    = 2400                 # Zero for automatic exposure
TEXT_FONT   = QFont("Courier", 10)

camera_num  = 1                 # Default camera (first in list)
image_queue = Queue.Queue()     # Queue to hold images
capturing   = True              # Flag to indicate capturing


from PyQt5 import QtCore, QtGui, QtWidgets
Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


SAMPLING_TIME = 1


# Grab images from the camera (separate thread)
def grab_images(cam_num, queue):
    cap = cv2.VideoCapture(cam_num-1 + CAP_API)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
    if EXPOSURE:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    else:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

    #self.log_msg(logging.INFO, "capturing frames...")
    while capturing:
        if cap.grab():
            retval, image = cap.retrieve(0)
            if image is not None and queue.qsize() < 2:
                queue.put(image)
            else:
                time.sleep(DISP_MSEC / 1000.0)
        else:
            print("Error: can't grab camera image")
            break
    #self.log_msg(logging.INFO, "stop capturing frames")
    cap.release()
    #self.log_msg(logging.INFO, "releasing")




# Signals need to be contained in a QObject or subclass in order to be correctly
# initialized.
#
class Signaller(QtCore.QObject):
    signal = Signal(str, logging.LogRecord)


# You specify the slot function to do whatever GUI updates you want. The handler
# doesn't know or care about specific UI elements.
#
class QtHandler(logging.Handler):
    def __init__(self, slotfunc, *args, **kwargs):
        super(QtHandler, self).__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slotfunc)

    def emit(self, record):
        s = self.format(record)
        self.signaller.signal.emit(s, record)

#
# This example uses QThreads, which means that the threads at the Python level
# are named something like "Dummy-1". The function below gets the Qt name of the
# current thread.
#
def ctname():
    return QtCore.QThread.currentThread().objectName()


#
# Used to generate random levels for logging.
#
LEVELS = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
          logging.CRITICAL)


# This example worker just outputs messages sequentially, interspersed with
# random delays of the order of a few seconds.
#
class Worker(QtCore.QObject):
    @Slot()
    def start(self):
        extra = {'qThreadName': ctname() }
        logger.debug('Started work', extra=extra)
        i = 1
        # Let the thread run until interrupted. This allows reasonably clean
        # thread termination.
        while not QtCore.QThread.currentThread().isInterruptionRequested():
            delay = 0.5 + random.random() * 2
            time.sleep(delay)
            level = random.choice(LEVELS)
            logger.log(level, 'Message after delay of %3.1f: %d', delay, i, extra=extra)
            i += 1



class MainWindow(QMainWindow, guiApp):

    COLORS = {
        logging.DEBUG: 'black',
        logging.INFO: 'blue',
        logging.WARNING: 'orange',
        logging.ERROR: 'red',
        logging.CRITICAL: 'purple',
    }

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        ################################# SIGNALS
        f = QtGui.QFont('nosuchfont')
        f.setStyleHint(f.Monospace)
        self.console.setFont(f)
        self.console.setReadOnly(True)
        self.handler = h = QtHandler(self.update_status)
        # Remember to use qThreadName rather than threadName in the format string.
        fs = '%(asctime)s %(qThreadName)-12s %(levelname)-8s %(message)s'
        formatter = logging.Formatter(fs)
        h.setFormatter(formatter)
        logger.addHandler(h)
        # Set up to terminate the QThread when we exit
        app.aboutToQuit.connect(self.force_quit)

        # Lay out all the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.console)

        # Connect the non-worker slots and signals
        #self.liveview_button.clicked.connect(self.manual_update)

        # Start a new worker thread and connect the slots for the worker
        self.start_thread()
        #self.sampling_button.clicked.connect(self.worker.start)
        self.sampling_button.clicked.connect(self.get_sample)

        # DISABLE BUTTON
        # Once started, the button should be disabled
        #self.sampling_button.clicked.connect(lambda : self.sampling_button.setEnabled(False))


        # MONITORING
        self.monitor_timer = QTimer(self)
        self.monitor_running = False
        self.data_x = []
        self.data_y = []
        self.ref_x = []
        self.ref_y = []
        self.ref_line = self.status_chart.plot(self.ref_x, self.ref_y, name="100um size", pen='r')
        self.msu_line = self.status_chart.plot(self.data_x, self.data_y, name="measurements",
                    pen='b', symbol='o', symbolSize=5)

        #legend.addItem(self.ref_line, name=self.ref_name.opts['beads'])
        self.monitor_queue = Queue.Queue()

#
        self.liveview_enabled = False

        # Init view
        self.show_default_view()
        self.log_msg(logging.INFO, "initialized system")


        # Sample items
        self.sampled_images = {}


    def grab_images(self, cam_num, queue):
        cap = cv2.VideoCapture(cam_num-1 + CAP_API)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
        if EXPOSURE:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
        else:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

        self.log_msg(logging.INFO, "capturing frames")
        while capturing:
            if cap.grab():
                retval, image = cap.retrieve(0)
                if image is not None and queue.qsize() < 2:
                    queue.put(image)
                else:
                    time.sleep(DISP_MSEC / 1000.0)
            else:
                self.log_msg(logging.ERROR, "cannot grab frames from camera, session cancelled!")
                break
        cap.release()

        img = np.zeros([IMG_SIZE[1], IMG_SIZE[0], 3], dtype=np.uint8)
        queue.put(img)


    def grab_sample_image(self, cam_num):
        cap = cv2.VideoCapture(cam_num-1 + CAP_API)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
        if EXPOSURE:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
        else:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

        self.log_msg(logging.INFO, "getting frame from camera")
        if cap.grab():
            retval, image = cap.retrieve(0)
            cap.release()
            if image is not None:
                return image
            else:
                None

    def show_default_view(self):
        img = np.zeros([IMG_SIZE[1], IMG_SIZE[0], 3], dtype=np.uint8)
        self.display_image(img, self.disp, 1)
        pass

    def get_random_id(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def get_sample(self):
        self.log_msg(logging.INFO, "getting sample")
        image = self.grab_sample_image(camera_num)
        if image.all() == None:
            self.log_msg(logging.ERROR, "cannot grab frame from camera")
        else:
            now = datetime.now()
            sample_id = self.get_random_id(6)
            image_name = sample_id + "_" + now.strftime("%d_%m_%Y-%H_%M_%S")
            self.sampled_images.update({image_name: image})
            self.listView.addItem(QListWidgetItem(image_name))

    def listwidgetclicked(self, item):
        image_key = item.text()
        print(image_key)
        img = self.sampled_images[image_key]
        image_queue.put(img)
        self.show_image(image_queue, self.disp, DISP_SCALE)

    def update_plot(self):
        self.log_msg(logging.INFO, "updating plot")
        if not self.monitor_queue.empty():
            data = self.monitor_queue.get()
            self.data_y.append(data)
            self.data_x = list(range(len(self.data_y)))

            # Reference data
            self.ref_x = list(range(len(self.data_y) + 5))
            self.ref_y = [0.5] * (len(self.data_y) + 5)
            self.msu_line.setData(self.data_x, self.data_y)
            self.ref_line.setData(self.ref_x, self.ref_y)
            self.log_msg(logging.INFO, str(data))

            # Update info
            self.last_point.setText("{:.6f}".format(data))
            self.total_samples.setText(str(len(self.data_x)))

    def start_monitoring(self):
        self.log_msg(logging.INFO, "Starting loop")
        count = 0
        measurement_flag = True
        while self.monitor_running:
            self.log_msg(logging.INFO, "loop")
            if measurement_flag == True:
                self.log_msg(logging.INFO, "getting measurement")
                avg_area = random.uniform(0.1, 1.0)
                self.monitor_queue.put(avg_area)
                measurement_flag = False
            count+=1
            if (count == SAMPLING_TIME):
                count=0
                measurement_flag=True
            time.sleep(1)

        self.log_msg(logging.INFO, "monitor process finished")

    def monitoring(self):
        if (self.monitor_running == False):
            self.log_msg(logging.INFO, "starting monitoring process ...")
            self.monitor_timer = QTimer(self)
            self.monitor_timer.timeout.connect(lambda:self.update_plot())
            self.monitor_timer.start(1000)
            self.monitor_thread = threading.Thread(target=self.start_monitoring)
            self.monitor_thread.start()
            self.monitor_running = True
            self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Stop monitoring", None))
        else:
            self.monitor_running = False
            self.monitor_thread.join()
            self.log_msg(logging.INFO, "stopping monitoring process ...")
            self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Start monitoring", None))
            self.monitor_timer.stop()

    def liveview(self):
        global capturing
        if (self.liveview_enabled == False):
            self.log_msg(logging.WARNING, "long exposure of the culture to light may affect the incubation process.")
            capturing = True
            self.log_msg(logging.INFO, "starting live view session ...")
            self.timer = QTimer(self)           # Timer to trigger display
            self.timer.timeout.connect(lambda:
            self.show_image(image_queue, self.disp, DISP_SCALE))
            self.timer.start(DISP_MSEC)
            self.capture_thread = threading.Thread(target=self.grab_images,
                    args=(camera_num, image_queue))

            self.capture_thread.start()
            time.sleep(1)
            if self.capture_thread.is_alive():
                self.liveview_enabled = True
                self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Stop live view", None))
            #else:
            #    self.log_msg(logging.ERROR, "live view session cancelled!")
        else:
            self.log_msg(logging.INFO, "stopping live view session...")
            self.liveview_enabled = False
            #global capturing
            capturing = False
            print("waiting for thread")
            self.capture_thread.join()
            print("shows black background")
            self.show_default_view()
            self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Start live view", None))
            self.timer.stop()
            #time.sleep(3)
            #self.show_default_view()


    # Fetch camera image from queue, and display it
    def show_image(self, imageq, display, scale):
        if not imageq.empty():
            image = imageq.get()
            if image is not None and len(image) > 0:
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.display_image(img, display, scale)

    # Display an image, reduce size if required
    def display_image(self, img, display, scale=1):
        disp_size = img.shape[1]//scale, img.shape[0]//scale
        disp_bpl = disp_size[0] * 3
        if scale > 1:
            img = cv2.resize(img, disp_size,
                             interpolation=cv2.INTER_CUBIC)
        qimg = QImage(img.data, disp_size[0], disp_size[1],
                      disp_bpl, IMG_FORMAT)
        display.setImage(qimg)

    # Handle sys.stdout.write: update text display
    def write(self, text):
        self.text_update.emit(str(text))
    def flush(self):
        pass

    # Append to text display
    def append_text(self, text):
        cur = self.textbox.textCursor()     # Move cursor to end of text
        cur.movePosition(QTextCursor.End)
        s = str(text)
        while s:
            head,sep,s = s.partition("\n")  # Split line at LF
            cur.insertText(head)            # Insert text at cursor
            if sep:                         # New line if LF
                cur.insertBlock()
        self.textbox.setTextCursor(cur)     # Update visible cursor

    # Window is closing: stop video capture
    def closeEvent(self, event):
        global capturing
        capturing = False
        #self.capture_thread.join()


#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################


    def start_thread(self):
        self.worker = Worker()
        self.worker_thread = QtCore.QThread()
        self.worker.setObjectName('Worker')
        self.worker_thread.setObjectName('WorkerThread')  # for qThreadName
        self.worker.moveToThread(self.worker_thread)
        # This will start an event loop in the worker thread
        self.worker_thread.start()

    def kill_thread(self):
        # Just tell the worker to stop, then tell it to quit and wait for that
        # to happen
        self.worker_thread.requestInterruption()
        if self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
        else:
            print('worker has already exited.')

    def force_quit(self):
        # For use when the window is closed
        if self.worker_thread.isRunning():
            self.kill_thread()

    # The functions below update the UI and run in the main thread because
    # that's where the slots are set up

    @Slot(str, logging.LogRecord)
    def update_status(self, status, record):
        color = self.COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.console.appendHtml(s)


    @Slot()
    def log_msg(self, level, msg):
        # This function uses the formatted message passed in, but also uses
        # information from the record to format the message in an appropriate
        # color according to its severity (level).
        #level = random.choice(LEVELS)
        extra = {'qThreadName': ctname() }
        logger.log(level, msg, extra=extra)




    @Slot()
    def manual_update(self):
        # This function uses the formatted message passed in, but also uses
        # information from the record to format the message in an appropriate
        # color according to its severity (level).
        level = random.choice(LEVELS)
        extra = {'qThreadName': ctname() }
        logger.log(level, 'Manually logged!', extra=extra)

    @Slot()
    def clear_display(self):
        self.console.clear()


