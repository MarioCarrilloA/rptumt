# Reference for this code:
# https://gist.github.com/vsajip/a87bd7f4234510b4fd6bdcd4ffea376d

import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot


class Console(QPlainTextEdit):
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)
        f = QtGui.QFont('nosuchfont')
        f.setStyleHint(f.Monospace)
        self.setFont(f)
        self.setReadOnly(True)
        self.handler = QtHandler(self.update_status)
        fs = '%(asctime)-5s %(levelname)-8s %(message)s'
        formatter = logging.Formatter(fs)
        self.handler.setFormatter(formatter)
        logger.addHandler(self.handler)

        self.COLORS = {
            logging.DEBUG: 'black',
            logging.INFO: 'blue',
            logging.WARNING: 'orange',
            logging.ERROR: 'red',
            logging.CRITICAL: 'purple',
        }


    def start_thread(self):
        self.worker = Worker()
        self.worker_thread = QtCore.QThread()
        self.worker.setObjectName('Worker')
        self.worker_thread.setObjectName('WorkerThread')
        self.worker.moveToThread(self.worker_thread)
        # This will start an event loop in the worker thread
        self.worker_thread.start()


    def kill_thread(self):
        self.worker_thread.requestInterruption()
        if self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
        else:
            print('worker has already exited.')


    def force_quit(self):
        if self.worker_thread.isRunning():
            self.kill_thread()


    @Slot(str, logging.LogRecord)
    def update_status(self, status, record):
        color = self.COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.appendHtml(s)


    @Slot()
    def log_msg(self, level, msg):
        logger.log(level, msg)


    @Slot()
    def clear_display(self):
        self.console.clear()


# Allows object communication
class Communicator(QtCore.QObject):
    signal = Signal(str, logging.LogRecord)


class QtHandler(logging.Handler):
    def __init__(self, slotfunc, *args, **kwargs):
        super(QtHandler, self).__init__(*args, **kwargs)
        self.communicator = Communicator()
        self.communicator.signal.connect(slotfunc)

    def emit(self, record):
        s = self.format(record)
        self.communicator.signal.emit(s, record)


class Worker(QtCore.QObject):
    @Slot()
    def start(self):
        logger.debug('Started work')
        i = 1
        while not QtCore.QThread.currentThread().isInterruptionRequested():
            delay = 0.5 + random.random() * 2
            time.sleep(delay)
            level = random.choice(LEVELS)
            logger.log(level, 'Message after delay of %3.1f: %d', delay, i)
            i += 1






