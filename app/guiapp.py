# Partially created by: Qt User Interface Compiler version 5.15.5
# but many changes were added manually.
##################################################################

import pyqtgraph

from console import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
        self.status_chart.setTitle("Estimated average size", color="b", size="14pt")
        self.status_chart.addLegend()
        self.status_chart.getAxis('left').setTextPen('black')
        self.status_chart.getAxis('bottom').setTextPen('black')
        self.styles = {"color": "blue", "font-size": "14px"}
        self.status_chart.setLabel("left", "object size um", **self.styles)
        self.status_chart.setLabel("bottom", "Sample number", **self.styles)
        self.status_chart.showGrid(x=True, y=True)
        self.status_chart.setYRange(0, 600, padding=0)

        # Sampled images
        self.gBoxSamples = QGroupBox(self.centralwidget)
        self.gBoxSamples.setObjectName(u"groupBox_5")
        self.gBoxSamples.setGeometry(QRect(1320, 405, 280, 375))
        self.gBoxSamples.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxSamples.setTitle(QCoreApplication.translate("MainWindow", u"Sampled images", None))
        self.listView = QListWidget(self.gBoxSamples)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(10, 25, 260, 345))
        self.listView.itemClicked.connect(self.clicked_list)

        # status information
        self.gstatus_info = QGroupBox(self.centralwidget)
        self.gstatus_info.setObjectName(u"status_info")
        self.gstatus_info.setGeometry(QRect(1610, 405, 285, 375))
        self.gstatus_info.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gstatus_info.setTitle(QCoreApplication.translate("MainWindow", u"Status information", None))
        self.total_bboxes = QLineEdit(str(0.0))
        self.total_bboxes.setReadOnly(True)
        self.bboxes_area_mean = QLineEdit(str(0))
        self.bboxes_area_mean.setReadOnly(True)
        self.bboxes_area_sd = QLineEdit(str(0))
        self.bboxes_area_sd.setReadOnly(True)
        self.estimated_size = QLineEdit(str(0))
        self.estimated_size.setReadOnly(True)
        self.status = QLineEdit(str(0))
        self.status.setReadOnly(True)

        self.total_images = QLineEdit(str(0))
        self.total_images.setReadOnly(True)
        self.vspace = QLabel()
        self.vspace.setGeometry(0, 0, 20, 30)
        self.table = QFormLayout(self.gstatus_info)

        # Radiobuttons to select type of image
        self.raw_radiobutton = QtWidgets.QRadioButton()
        self.raw_radiobutton.setText("Raw")
        self.predicted_radiobutton = QtWidgets.QRadioButton()
        self.predicted_radiobutton.setText("Predicted")
        self.predicted_radiobutton.setChecked(True)

        self.table.addRow("", self.vspace) # This is to add extra space, TODO: improve this
        self.table.addRow("Total Bboxes", self.total_bboxes)
        self.table.addRow("Areas mean [0,1]", self.bboxes_area_mean)
        self.table.addRow("Areas SD [0,1]", self.bboxes_area_sd)
        self.table.addRow("Estimated size (um)", self.estimated_size)
        self.table.addRow("Status", self.status)
        #self.table.addRow("", self.vspace)
        self.table.addRow("Display mode:", None)
        self.table.setVerticalSpacing(10)
        self.table.addRow(self.predicted_radiobutton, self.raw_radiobutton)
        self.table.addRow("Total collected images", self.total_images)
        #self.table.addRow(self.predicted_radiobutton, None)

        # Control
        self.gBoxControl = QGroupBox(self.centralwidget)
        self.gBoxControl.setObjectName(u"controlBox")
        self.gBoxControl.setGeometry(QRect(1320, 795, 575, 170))
        self.gBoxControl.setStyleSheet("QGroupBox{border: 1px solid gray;}")
        self.gBoxControl.setTitle(QCoreApplication.translate("MainWindow", u"Control", None))

        # New control buttons
        # Buttons for live view control
        self.liveview_label = QLabel("Camera Live View", self.gBoxControl)
        self.liveview_label.setFont(QFont('Arial', 16))
        self.liveview_label.move(20, 40)
        self.liveview_label.setStyleSheet("QLabel { color : purple; }");

        self.start_liveview_button = QPushButton(self.gBoxControl)
        self.start_liveview_button.setGeometry(QRect(50, 80, 52, 52))
        self.start_liveview_button.setIcon(QIcon('../imgs/icons/start_live.png'))
        self.start_liveview_button.setIconSize(QSize(48, 48))
        self.start_liveview_button.setToolTip("Start live view")

        self.stop_liveview_button = QPushButton(self.gBoxControl)
        self.stop_liveview_button.setGeometry(QRect(104, 80, 52, 52))
        self.stop_liveview_button.setIcon(QIcon('../imgs/icons/stop_live.png'))
        self.stop_liveview_button.setIconSize(QSize(48, 48))
        self.stop_liveview_button.setEnabled(False)
        self.stop_liveview_button.setToolTip("Stop live view")

        # Buttons for monitoring control
        self.monitor_label = QLabel("Monitoring control", self.gBoxControl)
        self.monitor_label.setFont(QFont('Arial', 16))
        self.monitor_label.move(245, 40)
        self.monitor_label.setStyleSheet("QLabel { color : purple; }");

        self.start_monitor_button = QPushButton(self.gBoxControl)
        self.start_monitor_button.setGeometry(QRect(220, 80, 52, 52))
        self.start_monitor_button.setIcon(QIcon('../imgs/icons/play_monitor.png'))
        self.start_monitor_button.setIconSize(QSize(48, 48))
        self.start_monitor_button.setToolTip("Start monitoring")

        self.stop_monitor_button = QPushButton(self.gBoxControl)
        self.stop_monitor_button.setGeometry(QRect(274, 80, 52, 52))
        self.stop_monitor_button.setIcon(QIcon('../imgs/icons/stop_monitor.png'))
        self.stop_monitor_button.setIconSize(QSize(48, 48))
        self.stop_monitor_button.setToolTip("Stop monitoring")
        self.stop_monitor_button.setEnabled(False)

        self.take_sample_button = QPushButton(self.gBoxControl)
        self.take_sample_button.setGeometry(QRect(328, 80, 52, 52))
        self.take_sample_button.setIcon(QIcon('../imgs/icons/take_sample.png'))
        self.take_sample_button.setToolTip("Take a sample")
        self.take_sample_button.setIconSize(QSize(48, 48))

        self.config_button = QPushButton(self.gBoxControl)
        self.config_button.setGeometry(QRect(382, 80, 52, 52))
        self.config_button.setIcon(QIcon('../imgs/icons/configuration.png'))
        self.config_button.setToolTip("Configuration")
        self.config_button.setIconSize(QSize(48, 48))


        # Quit button
        self.quit_label = QLabel("Quit", self.gBoxControl)
        self.quit_label.setFont(QFont('Arial', 16))
        self.quit_label.move(490, 40)
        self.quit_label.setStyleSheet("QLabel { color : purple; }");

        self.quit_button = QPushButton(self.gBoxControl)
        self.quit_button.setGeometry(QRect(488, 80, 52, 52))
        self.quit_button.setIcon(QIcon('../imgs/icons/quit.png'))
        self.quit_button.setToolTip("Quit")
        self.quit_button.setIconSize(QSize(48, 48))


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


