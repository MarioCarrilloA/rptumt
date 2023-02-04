from guiapp import *

import datetime
import logging
import random
import sys
import time
import numpy as np
import cv2
import time
from datetime import datetime
import random
import string
import pyqtgraph


from camera import *


class MainWindow(QMainWindow, guiApp):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        f = QtGui.QFont('nosuchfont')
        f.setStyleHint(f.Monospace)
        self.console.setFont(f)
        self.console.setReadOnly(True)
        # Remember to use qThreadName rather than threadName in the format string.
        fs = '%(asctime)s %(qThreadName)-5s %(levelname)-8s %(message)s'
        formatter = logging.Formatter(fs)
        # Set up to terminate the QThread when we exit
        app.aboutToQuit.connect(self.force_quit)

        # Lay out all the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.console)

        # Connect the non-worker slots and signals

        # Start a new worker thread and connect the slots for the worker
        self.start_thread()
        self.sampling_button.clicked.connect(self.get_sample)

        # DISABLE BUTTON
        # Once started, the button should be disabled

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

        self.monitor_queue = Queue.Queue()
        self.liveview_enabled = False

        # Camera settings
        self.width = 1280
        self.heigt = 720

        # Display settings
        self.img_format = QImage.Format_RGB888

        # Init view
        self.show_default_view()
        self.console.log_msg(logging.INFO, "initialized system")

        # Sample items
        self.sampled_images = {}
        self.camera = Camera()


    def show_default_view(self):
        img = np.zeros([self.heigt, self.width, 3], dtype=np.uint8)
        self.display_image(img, self.disp, 1)
        pass

    def get_random_id(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def get_sample(self):
        self.console.log_msg(logging.INFO, "getting sample")
        image = self.camera.grab_sample_image(camera_num)
        if image.all() == None:
            self.console.log_msg(logging.ERROR, "cannot grab frame from camera")
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
        self.console.log_msg(logging.INFO, "updating plot")
        if not self.monitor_queue.empty():
            data = self.monitor_queue.get()
            self.data_y.append(data)
            self.data_x = list(range(len(self.data_y)))

            # Reference data
            self.ref_x = list(range(len(self.data_y) + 5))
            self.ref_y = [0.5] * (len(self.data_y) + 5)
            self.msu_line.setData(self.data_x, self.data_y)
            self.ref_line.setData(self.ref_x, self.ref_y)
            self.console.log_msg(logging.INFO, str(data))

            # Update info
            self.last_point.setText("{:.6f}".format(data))
            self.total_samples.setText(str(len(self.data_x)))

    def start_monitoring(self):
        self.console.log_msg(logging.INFO, "Starting loop")
        count = 0
        measurement_flag = True
        while self.monitor_running:
            self.console.log_msg(logging.INFO, "loop")
            if measurement_flag == True:
                self.console.log_msg(logging.INFO, "getting measurement")
                avg_area = random.uniform(0.1, 1.0)
                self.monitor_queue.put(avg_area)
                measurement_flag = False
            count+=1
            if (count == SAMPLING_TIME):
                count=0
                measurement_flag=True
            time.sleep(1)

        self.console.log_msg(logging.INFO, "monitor process finished")

    def monitoring(self):
        if (self.monitor_running == False):
            self.console.log_msg(logging.INFO, "starting monitoring process ...")
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
            self.console.log_msg(logging.INFO, "stopping monitoring process ...")
            self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Start monitoring", None))
            self.monitor_timer.stop()

    def liveview(self):
        #global capturing
        if (self.liveview_enabled == False):
            self.console.log_msg(logging.WARNING,
                "long exposure of the culture to light may affect the incubation process.")
            #capturing = True
            self.camera.enable_capture()
            self.console.log_msg(logging.INFO, "starting live view session ...")
            self.timer = QTimer(self)           # Timer to trigger display
            self.timer.timeout.connect(lambda:
            self.show_image(image_queue, self.disp, DISP_SCALE))
            self.timer.start(DISP_MSEC)
            self.capture_thread = threading.Thread(target=self.camera.grab_images,
                    args=(camera_num, image_queue))

            self.capture_thread.start()
            time.sleep(1)
            if self.capture_thread.is_alive():
                self.liveview_enabled = True
                self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Stop live view", None))
            #else:
            #    self.log_msg(logging.ERROR, "live view session cancelled!")
        else:
            self.console.log_msg(logging.INFO, "stopping live view session...")
            self.liveview_enabled = False
            #global capturing
            #capturing = False
            self.camera.disable_capture()
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
                      disp_bpl, self.img_format)
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

