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

class AppGui(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"3DSCIP Viewer")
        #MainWindow.resize(1650, 950)
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
        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(-1, -1, 1280, 130))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')
        self.plainTextEdit.insertPlainText('Test test test test test test test\n')

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
        self.pushButton = QPushButton(self.gBoxControl)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 40, 103, 36))
        self.pushButton_2 = QPushButton(self.gBoxControl)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 90, 103, 36))

        # Menu bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1217, 29))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        pass
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        #self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        #self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        #self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.gBoxControl.setTitle(QCoreApplication.translate("MainWindow", u"control", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Sampling", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Live view", None))
    # retranslateUi



class MainWindow(QMainWindow, AppGui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def show_new_window(self, checked):
        w = AnotherWindow()
        w.show()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
