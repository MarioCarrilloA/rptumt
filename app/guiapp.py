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
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys

import datetime
import logging
import random
import sys
import time


from PyQt5 import QtCore, QtGui, QtWidgets
Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class guiApp(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("3DSCIP Viewer")
        MainWindow.setObjectName("3DSCIP Viewer")
        MainWindow.setFixedSize(1700, 980)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Viewer
        self.gBoxView = QGroupBox(self.centralwidget)
        self.gBoxView.setObjectName(u"groupBox_3")
        self.gBoxView.setGeometry(QRect(10, 20, 1300, 760))
        self.gBoxView.setStyleSheet("QGroupBox{border: 1px solid red;}")
        self.gBoxView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.view = QLabel(self.gBoxView)
        self.view.setObjectName(u"label")
        self.view.setGeometry(QRect(10, 20, 1280, 720))
        self.view.setStyleSheet("background-color: black")

        # Logging box
        self.gBoxLog = QGroupBox(self.centralwidget)
        self.gBoxLog.setObjectName(u"groupBox_2")
        self.gBoxLog.setGeometry(QRect(10, 795, 1300, 160))
        self.gBoxLog.setStyleSheet("QGroupBox{border: 1px solid green;}")
        self.gBoxLog.setTitle(QCoreApplication.translate("MainWindow", u"logging", None))
        self.scrollArea = QScrollArea(self.gBoxLog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 20, 1280, 130))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(10, 20, 1280, 130))
        self.console = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.console.setObjectName(u"console")
        self.console.setGeometry(QRect(-1, -1, 1280, 130))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        #self.console.insertPlainText('Initialize system...\n')

        # Status chart
        self.gBoxChart = QGroupBox(self.centralwidget)
        self.gBoxChart.setObjectName(u"groupBox_4")
        self.gBoxChart.setGeometry(QRect(1320, 20, 350, 375))
        self.gBoxChart.setStyleSheet("QGroupBox{border: 1px solid magenta;}")
        self.gBoxChart.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.label_2 = QLabel(self.gBoxChart)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 330, 345))
        self.label_2.setStyleSheet("background-color: white")

        # Sampled images
        self.gBoxSamples = QGroupBox(self.centralwidget)
        self.gBoxSamples.setObjectName(u"groupBox")
        self.gBoxSamples.setGeometry(QRect(1320, 405, 350, 375))
        self.gBoxSamples.setStyleSheet("QGroupBox{border: 1px solid blue;}")
        self.gBoxSamples.setTitle(QCoreApplication.translate("MainWindow", u"Sampled images", None))
        self.listView = QListView(self.gBoxSamples)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(10, 20, 330, 345))

        # Control
        self.gBoxControl = QGroupBox(self.centralwidget)
        self.gBoxControl.setObjectName(u"groupBox_5")
        self.gBoxControl.setGeometry(QRect(1320, 795, 350, 160))
        self.gBoxControl.setStyleSheet("QGroupBox{border: 1px solid black;}")
        self.gBoxControl.setTitle(QCoreApplication.translate("MainWindow", u"control", None))
        self.sampling_button = QPushButton(self.gBoxControl)
        self.sampling_button.setObjectName(u"sampling")
        self.sampling_button.setGeometry(QRect(20, 40, 103, 36))
        self.sampling_button.setText(QCoreApplication.translate("MainWindow", u"Sampling", None))
        self.liveview_button = QPushButton(self.gBoxControl)
        self.liveview_button.setObjectName(u"liveview_button")
        self.liveview_button.setGeometry(QRect(20, 90, 103, 36))
        self.liveview_button.setText(QCoreApplication.translate("MainWindow", u"Live view", None))

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


# Signals need to be contained in a QObject or subclass in order to be correctly
# initialized.
#
class Signaller(QtCore.QObject):
    signal = Signal(str, logging.LogRecord)

#
# Output to a Qt GUI is only supposed to happen on the main thread. So, this
# handler is designed to take a slot function which is set up to run in the main
# thread. In this example, the function takes a string argument which is a
# formatted log message, and the log record which generated it. The formatted
# string is just a convenience - you could format a string for output any way
# you like in the slot function itself.
#
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

#
# This worker class represents work that is done in a thread separate to the
# main thread. The way the thread is kicked off to do work is via a button press
# that connects to a slot in the worker.
#
# Because the default threadName value in the LogRecord isn't much use, we add
# a qThreadName which contains the QThread name as computed above, and pass that
# value in an "extra" dictionary which is used to update the LogRecord with the
# QThread name.
#
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

    def __init__(self):
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
        self.liveview_button.clicked.connect(self.manual_update)

        # Start a new worker thread and connect the slots for the worker
        self.start_thread()
        self.sampling_button.clicked.connect(self.worker.start)
        # Once started, the button should be disabled
        self.sampling_button.clicked.connect(lambda : self.sampling_button.setEnabled(False))


        self.log_msg(logging.INFO, "test.........")
        self.log_msg(logging.DEBUG, "test.........")
        self.log_msg(logging.WARNING, "test.........")
        self.log_msg(logging.ERROR, "test.........")
        self.log_msg(logging.CRITICAL, "test.........")
        logging.log(logging.INFO, "test 2------------------")
        self.log_msg(logging.CRITICAL, "test.........")

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





















app = QApplication(sys.argv)
w = MainWindow()
w.show()

logging.log(logging.INFO, "test.........")
app.exec()
