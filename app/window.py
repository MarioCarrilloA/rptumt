import cv2
import datetime
import logging
import random
import sys
import os
import time
import numpy as np
import time
import string
import pyqtgraph
import threading

from camera import *
from datetime import datetime
from guiapp import *
from yolov5_upstream import detect
from sample import *

class MainWindow(QMainWindow, guiApp):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        self.console.setReadOnly(True)
        app.aboutToQuit.connect(self.console.force_quit)

        # Lay out all the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.console)

        # Start a new worker thread and connect the slots for the worker
        self.console.start_thread()
        #self.sampling_button.clicked.connect(self.take_sample)

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

        self.monitor_queue = Queue()
        self.local_image_queue = Queue()
        self.liveview_enabled = False

        # Camera settings
        self.width = 1280
        self.heigt = 720

        # Display settings
        self.img_format = QImage.Format_RGB888
        self.display_scale = 1
        self.display_time = 50

        # Init view
        self.show_default_view()
        self.console.log_msg(logging.INFO, "initialized system")

        # Sample items
        self.sampled_images = {}
        self.camera = Camera()

        # Connection
        self.start_liveview_button.clicked.connect(self.start_liveview2)
        self.stop_liveview_button.clicked.connect(self.stop_liveview)
        self.start_monitor_button.clicked.connect(self.start_monitor)
        self.stop_monitor_button.clicked.connect(self.stop_monitor)
        self.take_sample_button.clicked.connect(self.take_sample)
        self.raw_radiobutton.clicked.connect(self.change_image_type)
        self.predicted_radiobutton.clicked.connect(self.change_image_type)

        # Last collected and processed sample
        self.last_measurment = None
        self.last_selected_sample = None

    def show_default_view(self):
        img = np.zeros([self.heigt, self.width, 3], dtype=np.uint8)
        self.display_image(img, self.disp, 1)


    def predict(self, sample_path, img_name):
        pwd = os.getcwd()
        predicted_sample_path = sample_path.replace("sample", "predicted")

        # Usage of YOLOv5 nano model
        model = pwd + "/" + "model/nano.pt"
        input_img = sample_path + "/" + img_name
        detect.run(
            weights=model,
            source=input_img,
            project=sample_path,
            name="prediction",
            hide_conf=True,
            hide_labels=True,
            line_thickness=1,
            save_txt=True
        )


    def generate_random_id(self, k=5):
        newid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(k))
        return newid


    def take_sample(self):
        self.take_sample_button.setEnabled(False)
        sample_path, img_name = self.camera.save_single_image()
        self.predict(sample_path, img_name)
        self.console.log_msg(logging.INFO, "New sample processed")
        sample_id = os.path.basename(sample_path) + "_" + self.generate_random_id(5)
        new_sample = Sample(sample_id)
        new_sample.sample_path = sample_path
        self.sampled_images.update({sample_id: new_sample})
        self.listView.insertItem(0, QListWidgetItem(sample_id))
        self.load_img_in_display(sample_id)
        self.take_sample_button.setEnabled(True)
        self.last_measurment = new_sample
        self.last_selected_sample = sample_id

    def change_image_type(self):
        if self.last_selected_sample == None:
            if self.raw_radiobutton.isChecked():
                self.console.log_msg(logging.INFO, "Set display raw mode")
            else:
                self.console.log_msg(logging.INFO, "Set display prediction mode")
            return
        else:
            self.load_img_in_display(self.last_selected_sample)


    def load_img_in_display(self, image_key):
        sample = self.sampled_images[image_key]
        if self.raw_radiobutton.isChecked():
            img = sample.load_sample_image()
            self.console.log_msg(logging.INFO, "Show raw image: " + str(image_key))
        else:
            img = sample.load_predicted_image()
            self.console.log_msg(logging.INFO, "Show predicted image: " + str(image_key))
        self.local_image_queue.put(img)
        self.show_image(self.local_image_queue, self.disp, self.display_scale)


    def clicked_list(self, item):
        image_key = item.text()
        self.last_selected_sample = image_key
        self.load_img_in_display(image_key)


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
        self.console.log_msg(logging.INFO, "Starting video loop")
        count = 0
        measurement_flag = True
        while self.monitor_running:
            if measurement_flag == True:
                self.console.log_msg(logging.INFO, "getting measurement")
                avg_area = random.uniform(50, 600)
                self.monitor_queue.put(avg_area)
                measurement_flag = False
            count+=1
            if (count == SAMPLING_TIME):
                count=0
                measurement_flag=True
            time.sleep(1)

        self.console.log_msg(logging.INFO, "monitor process finished")


    def update_state(self):
        self.update_plot()
        #self.take_sample()


#    def monitor(self):
#        if (self.monitor_running == False):
#            self.console.log_msg(logging.INFO, "starting monitoring process ...")
#            self.monitor_timer = QTimer(self)
#            self.monitor_timer.timeout.connect(lambda:self.update_state())
#            self.monitor_timer.start(1000)
#            self.monitor_thread = threading.Thread(target=self.start_monitoring)
#            self.monitor_thread.start()
#            self.monitor_running = True
#            self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Stop monitoring", None))
#        else:
#            self.monitor_running = False
#            self.monitor_thread.join()
#            self.console.log_msg(logging.INFO, "stopping monitoring process ...")
#            self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Start monitoring", None))
#            self.monitor_timer.stop()


    def start_monitor(self):
        self.console.log_msg(logging.INFO, "starting monitoring process ...")
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(lambda:self.update_state())
        self.monitor_timer.start(1000)
        self.monitor_thread = threading.Thread(target=self.start_monitoring)
        self.monitor_thread.start()
        self.monitor_running = True
        self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Stop monitoring", None))
        self.start_monitor_button.setEnabled(False)
        self.start_liveview_button.setEnabled(False)
        self.stop_monitor_button.setEnabled(True)


    def stop_monitor(self):
        self.monitor_running = False
        self.monitor_thread.join()
        self.console.log_msg(logging.INFO, "stopping monitoring process ...")
        self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Start monitoring", None))
        self.monitor_timer.stop()
        self.start_monitor_button.setEnabled(True)
        self.start_liveview_button.setEnabled(True)
        self.stop_monitor_button.setEnabled(False)


    def start_liveview2(self):
        self.console.log_msg(logging.WARNING,
            "long exposure of the culture to light may affect the incubation process.")
        self.camera.enable_capture()
        self.console.log_msg(logging.INFO, "starting live view session ...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:
            self.show_image(self.camera.image_queue, self.disp, self.display_scale))
        self.timer.start(self.display_time)
        self.capture_thread = threading.Thread(target=self.camera.grab_frames)
        self.capture_thread.start()
        self.start_liveview_button.setEnabled(False)
        self.take_sample_button.setEnabled(False)
        self.start_monitor_button.setEnabled(False)
        self.stop_liveview_button.setEnabled(True)


    def stop_liveview(self):
        self.console.log_msg(logging.INFO, "stopping live view session...")
        self.camera.disable_capture()
        print("waiting for thread")
        self.capture_thread.join()

        print("shows black background")
        self.show_default_view()
        self.timer.stop()
        self.start_liveview_button.setEnabled(True)
        self.take_sample_button.setEnabled(True)
        self.start_monitor_button.setEnabled(True)
        self.stop_liveview_button.setEnabled(False)


#    def start_liveview(self):
#        if (self.liveview_enabled == False):
#            self.console.log_msg(logging.WARNING,
#                "long exposure of the culture to light may affect the incubation process.")
#            self.camera.enable_capture()
#            self.console.log_msg(logging.INFO, "starting live view session ...")
#            self.timer = QTimer(self)           # Timer to trigger display
#            self.timer.timeout.connect(lambda:
#            self.show_image(self.camera.image_queue, self.disp, self.display_scale))
#            self.timer.start(self.display_time)
#            self.capture_thread = threading.Thread(target=self.camera.grab_frames)
#
#            self.capture_thread.start()
#            time.sleep(1)
#            if self.capture_thread.is_alive():
#                self.liveview_enabled = True
#                self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Stop live view", None))
#        else:
#            self.console.log_msg(logging.INFO, "stopping live view session...")
#            self.liveview_enabled = False
#            self.camera.disable_capture()
#            print("waiting for thread")
#            self.capture_thread.join()
#            print("shows black background")
#            self.show_default_view()
#            self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Start live view", None))
#            self.timer.stop()


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


