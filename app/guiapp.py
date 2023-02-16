# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'templateGIYTbq.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QLabel,
        QVBoxLayout,
        QWidget,
        QLineEdit,
        QFormLayout
)
import sys


import pyqtgraph

from console import *

# Image widget
class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        self.setMinimumSize(image.size())
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


class guiApp(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("3DSCIP Viewer")
        MainWindow.setObjectName("3DSCIP Viewer")
        MainWindow.setFixedSize(1900, 1000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Viewer
        self.gBoxView = QGroupBox(self.centralwidget)
        self.gBoxView.setObjectName(u"groupBox_3")
        self.gBoxView.setGeometry(QRect(10, 20, 1300, 760))
        self.gBoxView.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.disp = ImageWidget(self.gBoxView)
        self.disp.setObjectName(u"display")
        self.disp.setGeometry(QRect(10, 25, 1280, 720))

        # Logging box
        self.gBoxLog = QGroupBox(self.centralwidget)
        self.gBoxLog.setObjectName(u"groupBox_2")
        self.gBoxLog.setGeometry(QRect(10, 795, 1300, 170))
        self.gBoxLog.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxLog.setTitle(QCoreApplication.translate("MainWindow", u"logging", None))
        self.scrollArea = QScrollArea(self.gBoxLog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 25, 1280, 130))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(10, 20, 1280, 130))
        self.console = Console(self.scrollAreaWidgetContents)
        self.console.setObjectName(u"console")
        self.console.setGeometry(QRect(-1, -1, 1280, 130))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Status chart
        self.gBoxChart = QGroupBox(self.centralwidget)
        self.gBoxChart.setObjectName(u"groupBox_4")
        self.gBoxChart.setGeometry(QRect(1320, 20, 575, 375))
        self.gBoxChart.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxChart.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.status_chart = pyqtgraph.PlotWidget(self.gBoxChart)
        self.status_chart.setGeometry(QRect(10, 25, 555, 345))
        self.status_chart.setBackground('w')
        self.status_chart.setTitle("Bounding box size", color="b", size="12pt")
        self.status_chart.addLegend()
        self.styles = {"color": "blue", "font-size": "14px"}
        self.status_chart.setLabel("left", "object size um", **self.styles)
        self.status_chart.setLabel("bottom", "Sample number", **self.styles)
        self.status_chart.showGrid(x=True, y=True)


        # Sampled images
        self.gBoxSamples = QGroupBox(self.centralwidget)
        self.gBoxSamples.setObjectName(u"groupBox_5")
        self.gBoxSamples.setGeometry(QRect(1320, 405, 280, 375))
        self.gBoxSamples.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxSamples.setTitle(QCoreApplication.translate("MainWindow", u"Sampled images", None))
        self.listView = QListWidget(self.gBoxSamples)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(10, 25, 260, 345))
        #self.gBoxSamples.setEnabled(False)
        self.listView.itemClicked.connect(self.listwidgetclicked)

        # status information
        self.gstatus_info = QGroupBox(self.centralwidget)
        self.gstatus_info.setObjectName(u"status_info")
        self.gstatus_info.setGeometry(QRect(1610, 405, 285, 375))
        self.gstatus_info.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gstatus_info.setTitle(QCoreApplication.translate("MainWindow", u"Status information", None))
        self.last_point = QLineEdit(str(0.0))
        self.last_point.setReadOnly(True)
        self.total_samples = QLineEdit(str(0))
        self.total_samples.setReadOnly(True)
        self.succeed_samples = QLineEdit(str(0))
        self.succeed_samples.setReadOnly(True)
        self.failed_samples = QLineEdit(str(0))
        self.failed_samples.setReadOnly(True)
        self.ph = QLineEdit(str(0))
        self.ph.setReadOnly(True)
        self.vspace = QLabel()
        self.vspace.setGeometry(0, 0, 20, 30)
        self.table = QFormLayout(self.gstatus_info)
        self.table.addRow("", self.vspace) # This is to add extra space, TODO: improve this
        self.table.addRow("Last measurement", self.last_point)
        self.table.addRow("Total samples", self.total_samples)
        self.table.addRow("Succeed samples", self.succeed_samples)
        self.table.addRow("Failed samples", self.failed_samples)
        self.table.addRow("pH (approx.)", self.ph)

        # Control
        self.gBoxControl = QGroupBox(self.centralwidget)
        self.gBoxControl.setObjectName(u"groupBox_5")
        self.gBoxControl.setGeometry(QRect(1320, 795, 575, 170))
        self.gBoxControl.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxControl.setTitle(QCoreApplication.translate("MainWindow", u"Control", None))
        self.sampling_button = QPushButton(self.gBoxControl)
        self.sampling_button.setObjectName(u"sampling")
        self.sampling_button.setGeometry(QRect(10, 40, 130, 35))
        self.sampling_button.setText(QCoreApplication.translate("MainWindow", u"Take a sample", None))
        self.monitor_button = QPushButton(self.gBoxControl)
        self.monitor_button.setObjectName(u"monitor_button")
        self.monitor_button.setGeometry(QRect(10, 80, 130, 35))
        self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Start monitoring", None))
        self.monitor_button.clicked.connect(self.monitor)
        self.liveview_button = QPushButton(self.gBoxControl)
        self.liveview_button.setObjectName(u"liveview_button")
        self.liveview_button.setGeometry(QRect(10, 120, 130, 35))
        self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Start live view", None))
        self.liveview_button.clicked.connect(self.liveview)


        # Menu bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1217, 29))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Conect signasl and slots
        QMetaObject.connectSlotsByName(MainWindow)


