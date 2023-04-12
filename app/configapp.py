from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDesktopWidget
)


class Configuration(QWidget):
    def __init__(self, sampling_time=10):
        super().__init__()
        self.sampling_time = sampling_time
        self.resize(150, 100)
        self.setWindowTitle("Configuration")
        layout = QVBoxLayout()
        self.label = QLabel("Specifiy sampling time (seconds)")
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.read_data)
        self.sampling_time_box = QLineEdit(str(self.sampling_time))
        layout.addWidget(self.label)
        layout.addWidget(self.sampling_time_box)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        # Move window location to the center
        geo = self.frameGeometry()
        desktop = QDesktopWidget().availableGeometry().center()
        geo.moveCenter(desktop)
        self.move(geo.topLeft())


    def show_error_msg(self, info):
        self.hide()
        self.sampling_time_box.setText(str(self.sampling_time))
        print("incorrect input")
        msg = QMessageBox()
        msg.setWindowTitle("Configuration error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Invalid input")
        msg.setInformativeText(info)
        msg.setStandardButtons(QMessageBox.Close)
        msg.exec_()

    def read_data(self):
        sampling_time = self.sampling_time_box.text()
        # Validate sampling time input
        if sampling_time.isdigit():
            if int(sampling_time) < 5:
                self.show_error_msg("Sampling time has to be greater or equal than 5 seconds")
            else :
                print("correct input")
                self.sampling_time = int(sampling_time)
                self.hide()
        else:
            self.show_error_msg("Sampling time has to be an usigned integer")


    def get_sampling_time(self):
        return self.sampling_time

