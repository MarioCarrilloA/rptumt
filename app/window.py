import csv
import cv2
import datetime
import glob
import logging
import numpy as np
import os
import platform
import pyqtgraph
import random
import statistics
import string
import sys
import threading
import time

from camera import *
from configapp import *
from datetime import datetime
from guiapp import *
from yolov5_upstream import detect
from sample import *


class MainWindow(QMainWindow, guiApp, QObject):
    # Signal to check when the thread has finished
    # to process and image
    image_processed = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        # Console only show messages
        self.console.setReadOnly(True)
        app.aboutToQuit.connect(self.console.force_quit)

        # Lay out all the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.console)

        # Start a new worker thread and connect the slots for the worker
        self.console.start_thread()

        # Components to compute and plot statistics
        self.monitor_timer = QTimer(self)
        self.monitor_running = False
        self.data_x = []
        self.data_y = []
        self.estimated_size_line = self.status_chart.plot(self.data_x, self.data_y,
                    pen='magenta', symbol='o', symbolPen="blue", symbolSize=5)
        self.monitor_queue = Queue()
        self.local_image_queue = Queue()

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
        self.start_liveview_button.clicked.connect(self.start_liveview)
        self.stop_liveview_button.clicked.connect(self.stop_liveview)
        self.start_monitor_button.clicked.connect(self.start_monitor)
        self.stop_monitor_button.clicked.connect(self.stop_monitor)
        self.take_sample_button.clicked.connect(self.take_sample)
        self.config_button.clicked.connect(self.configure)
        self.quit_button.clicked.connect(self.quit)
        self.raw_radiobutton.clicked.connect(self.display_image_type)
        self.predicted_radiobutton.clicked.connect(self.display_image_type)

        # Last collected and processed sample
        self.last_measurment = None
        self.last_selected_sample = None

        # Set default values
        self.total_bboxes.setText("NA")
        self.bboxes_area_mean.setText("NA")
        self.bboxes_area_sd.setText("NA")
        self.estimated_size.setText("NA")
        self.status.setText("NA")
        self.total_images.setText("NA")

        # Connect to receive signal from thread
        self.image_processed.connect(self.show_sample_statistics)

        # Create instance of configuration
        self.config = Configuration()

        # Flags to exit the program correctly
        self.liveview_active = False
        self.monitoring_active = False


    def configure(self):
        self.config.show()
        self.console.log_msg(logging.INFO, "Configure")


    def quit(self):
        # Finish active tasks
        if (self.liveview_active == True):
            self.console.log_msg(logging.WARNING, "Liveview process is active")
            self.stop_liveview()

        if (self.monitoring_active == True):
            self.console.log_msg(logging.WARNING, "Monitoring process is active")
            self.stop_monitor()

        self.console.log_msg(logging.INFO, "Exit...")
        QCoreApplication.instance().quit()


    @QtCore.pyqtSlot()
    def show_sample_statistics(self):
        sample = self.last_measurment

        # Format output
        mean = "{:.8f}".format(sample.mean)
        sd = "{:.8f}".format(sample.sd)
        estimated_size = "{:.2f}".format(sample.estimated_size)
        status = sample.status
        total_bboxes = str(sample.total_bboxes)
        total_images = str(len(self.data_x))

        # Set output
        self.bboxes_area_mean.setText(mean)
        self.bboxes_area_sd.setText(sd)
        self.estimated_size.setText(estimated_size)
        self.status.setText(status)
        self.total_bboxes.setText(total_bboxes)
        self.total_images.setText(total_images)
        self.console.log_msg(logging.INFO, "Update control panel information")


    def show_default_view(self):
        # Message configuration
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        color = (0, 255, 0) # Green color
        system_info = str("Platform: " + platform.system() + " - " + platform.machine())
        ct = str("System initialized: " + datetime.now().strftime('%d-%m-%Y'))

        # Empty image
        img = np.zeros([self.heigt, self.width, 3], dtype=np.uint8)

        # Write message in default frame
        img = cv2.putText(img, 'No available data to display', (10, 20),
            font, font_scale, color, thickness, cv2.LINE_AA)
        img = cv2.putText(img, system_info, (10, 40), font,
            font_scale, color, thickness, cv2.LINE_AA)
        img = cv2.putText(img, ct, (10, 60), font,
            font_scale, color, thickness, cv2.LINE_AA)
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
            hide_labels=False,
            line_thickness=1,
            save_txt=True
        )


    def generate_random_id(self, k=5):
        newid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(k))
        return newid


    def read_labels(self, label_files):
        areas = []
        print("Computing areas of input files...")
        for label_file in label_files:
            f = open(label_file, 'r')
            labels = f.readlines()
            f.close()
            for label in labels:
                (cathegory, xc, yc, w, h) = label.strip().split(" ")
                area = float(w) * float(h)
                areas.append(area)
        return areas


    def estimate_object_size(self, x):
        #size = 54.6533 + (274658.1545 * x) - (32493746.2635 * pow(x, 2))
        size = 49.7559 + (282642.6953 * x) - (34327751.6515 * pow(x, 2))
        return size


    def generate_sample_data(self, sample_path, img_name):
        label_path = sample_path + "/prediction/labels"
        label_files = glob.glob(label_path + "/*.txt")

        # Init sample structure
        identity = os.path.basename(sample_path) + "_" + self.generate_random_id(5)
        sample = Sample(identity=identity)
        sample.sample_path = sample_path

        # Evaluate if there are label files
        if len(label_files) == 0:
            self.console.log_msg(logging.WARNING, "Labels no found")
            return sample

        # Compute statistics
        areas = self.read_labels(label_files)
        if (len(areas) >= 3):
            mean = statistics.mean(areas)
            sd = statistics.stdev(areas)
            estimated_size = self.estimate_object_size(mean)
            sample.mean = mean
            sample.sd = sd
            sample.estimated_size = estimated_size
            sample.status = "VALID"
        else:
            self.console.log_msg(logging.WARNING, "Invalid: not enough data to compute statistics")
        sample.areas = areas
        sample.total_bboxes = len(areas)
        return sample


    def update_info_panel(self, sample):
        self.bboxes_area_mean.setText(str(sample.mean))
        self.bboxes_area_sd.setText(str(sample.sd))
        self.estimated_size.setText(str(sample.estimated_size))
        self.status.setText(sample.status)
        self.total_bboxes.setText(str(sample.total_bboxes))


    def update_data_plot(self, sample):
        self.data_y.append(sample.estimated_size)
        self.data_x = list(range(len(self.data_y)))
        self.estimated_size_line.setData(self.data_x, self.data_y)


    def log_sample(self, s):
        log_sample_file = self.camera.experiment_id + "/samples.csv"
        row = []
        header = []
        if os.path.isfile(log_sample_file) == False:
            header = ["sample", "mean", "sd", "numsamples", "Esize", "status"]
        with open (log_sample_file,'a') as csvfile:
            fwriter = csv.writer(csvfile, delimiter=',')
            row.append(s.sample_path + "/" + s.image_name)
            row.append(s.mean)
            row.append(s.sd)
            row.append(s.total_bboxes)
            row.append(s.estimated_size)
            row.append(s.status)
            if len(header) != 0:
                fwriter.writerow(header)
            fwriter.writerow(row)


    def process_sample(self):
        sample_path, img_name = self.camera.save_single_image()
        self.console.log_msg(logging.INFO, "Processing prediction...")

        # Feed CNN model with the recent image
        self.predict(sample_path, img_name)
        self.console.log_msg(logging.INFO, "New sample processed")

        # Compute data from labels
        sample = self.generate_sample_data(sample_path, img_name)
        self.sampled_images.update({sample.identity: sample})
        self.listView.insertItem(0, QListWidgetItem(sample.identity))
        self.load_img_in_display(sample.identity)
        self.last_measurment = sample
        self.last_selected_sample = sample.identity
        self.take_sample_button.setEnabled(True)
        self.start_liveview_button.setEnabled(True)
        self.console.log_msg(logging.INFO, "Finish to process " + str(sample.identity))
        self.update_data_plot(sample)
        self.log_sample(sample)

        # Emit signal to update information on GUI
        self.image_processed.emit()


    def take_sample(self):
        self.take_sample_button.setEnabled(False)
        self.start_liveview_button.setEnabled(False)
        self.console.log_msg(logging.INFO, "Taking new sample, init camera...")
        prediction_thread = threading.Thread(target=self.process_sample)
        prediction_thread.start()


    def display_image_type(self):
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


    def start_monitor(self):
        sampling_time = self.config.get_sampling_time()
        self.console.log_msg(logging.INFO, "starting monitoring process...")
        self.console.log_msg(logging.INFO, "sampling time: " + str(sampling_time) + " seconds")
        self.monitoring_active = True
        self.config_button.setEnabled(False)
        self.start_monitor_button.setEnabled(False)
        self.start_liveview_button.setEnabled(False)
        self.stop_monitor_button.setEnabled(True)
        self.console.log_msg(logging.INFO, "starting monitoring process ...")
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(lambda:self.take_sample())

        # Timer every 10 seconds by default
        # The seconds will be converted to milliseconds
        self.monitor_timer.start(sampling_time * 1000)


    def stop_monitor(self):
        self.console.log_msg(logging.INFO, "stopping monitoring process ...")
        self.monitoring_active = False
        self.monitor_timer.stop()
        self.config_button.setEnabled(True)
        self.start_monitor_button.setEnabled(True)
        self.start_liveview_button.setEnabled(True)
        self.stop_monitor_button.setEnabled(False)


    def start_liveview(self):
        self.console.log_msg(logging.WARNING,
            "long exposure of the culture to light may affect the incubation process.")
        self.liveview_active = True
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
        self.liveview_active = False
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
        self.display_image_type()


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


