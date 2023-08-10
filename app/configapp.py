from PyQt5.QtWidgets import (
    QDesktopWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from PyQt5.QtCore import (QTime, pyqtSignal)


class Configuration(QWidget):
    """
    This class is to show a second window (GUI) to modify
    the sampling configuration.
    """
    sig = pyqtSignal()
    # TODO: Specify sampling time by using a configuration file
    def __init__(self):
        super().__init__()
        # Default sampling time values
        self.hours = 1
        self.minutes = 0
        self.seconds = 0
        self.sampling_time = (self.hours * 3600) + (self.minutes * 60) + self.seconds
        self.resize(150, 150)
        self.setWindowTitle("Configuration")
        layout = QVBoxLayout()
        label = QLabel("Specifiy sampling time")
        layout.addWidget(label)

        # Set the time
        default_time = QTime()
        default_time.setHMS(self.hours, self.minutes, self.seconds)
        self.sampling_time_edit = QTimeEdit()
        self.sampling_time_edit.setTime(default_time)
        self.sampling_time_edit.setTimeRange(QTime(00, 00, 5), QTime(24, 59, 59))
        self.sampling_time_edit.setDisplayFormat("hh:mm:ss")
        layout.addWidget(self.sampling_time_edit)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.read_data)
        layout.addWidget(ok_button)
        self.setLayout(layout)

        # Move window location to the center
        geo = self.frameGeometry()
        desktop = QDesktopWidget().availableGeometry().center()
        geo.moveCenter(desktop)
        self.move(geo.topLeft())


    def show_error_msg(self, info):
        """
        Shows an error message box for an invalid input
        """
        self.hide()
        # Set last valid configuration
        last_time = QTime()
        print("Last configuration", self.hours, self.minutes, self.seconds)
        self.sampling_time_edit.setTime(QTime(self.hours, self.minutes, self.seconds))
        msg = QMessageBox()
        msg.setWindowTitle("Configuration error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Invalid input")
        msg.setInformativeText(info)
        msg.setStandardButtons(QMessageBox.Close)
        msg.exec_()


    def read_data(self):
        """
        Reads the input data from the text boxes
        """
        conf = self.sampling_time_edit.time()
        tmp_hours = conf.hour()
        tmp_minutes = conf.minute()
        tmp_seconds = conf.second()
        tmp_sampling_time = (tmp_hours * 3600) + (tmp_minutes * 60) + tmp_seconds

        print("Sampling time:", self.sampling_time)

        if tmp_sampling_time < 5:
            self.show_error_msg("Sampling time must be greater or equal than 5 seconds")
        else:
            print("correct input")
            self.hours = tmp_hours
            self.minutes = tmp_minutes
            self.seconds = tmp_seconds
            self.sampling_time = tmp_sampling_time
            self.hide()
            self.sig.emit()

    def get_sampling_time(self):
        """
        Gets the wait time to take every image
        """
        return self.sampling_time

    def get_HMS_sampling_time(self):
        """
        Gets hours, minutes and seconds which this app
        waits to take every image
        """
        return self.hours, self.minutes, self.seconds
