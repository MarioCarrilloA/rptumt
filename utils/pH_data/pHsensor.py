# Software to handle Sentron pH sensor

import serial
import time
import os
import numpy as np
import signal
import sys
import click

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


class serialpHSensor():
    def __init__(self):
        self.serial_port = None


    def command(self, cmd, v=True):
        if (v == True):
            print("Executed command: " + str(cmd))
        self.serial_port.write(serial.to_bytes(cmd))
        time.sleep(1.5)
        data = self.serial_port.readline()
        return data


    def start_calibration(self):
        cmd = [67, 76, 82, 33, 13]
        msg = self.command(cmd)
        return msg


    def init_pH7_calibration(self):
        cmd = [1, 1, 3, 33, 13]
        msg = self.command(cmd)
        return msg


    def retrive_single_pH_value(self, v=True):
        cmd = [57, 57, 57, 33, 13]
        msg = self.command(cmd, v)
        return msg

    def retrive_temperature_value(self):
        cmd = [55, 55, 55, 33, 13]
        msg = self.command(cmd)
        return msg


    def decode_ph_signal_protocol(self, data):
        if (len(data) >= 3):
            A = int(data[0])
            B = int(data[1])
            C = int(data[2])

        elif (len(data) == 2):
            A = int(data[0])
            B = int(data[1])
            C = 0

        elif (len(data) == 1):
            A = int(data[0])
            B = 0
            C = 0

        pH = float(int((A * 4096) + (B * 64) + C) * 0.001)
        #return "{:.4f}".format(pH)
        return "{:.2f}".format(pH)

    def decode_temp_signal_protocol(self, data):
        if (len(data) >= 2):
            A = int(data[0])
            B = int(data[1])
        elif (len(data) == 1):
            A = int(data[0])
            B = 0
        temp_F = float(int((A * 64) + B) * 0.1)
        temp_C = (temp_F - 32) * (5 / 9)
        return "{:.2f}".format(temp_C)


    def end_calibration(self):
        cmd = [81, 73, 84, 33, 13]
        msg = self.command(cmd)
        return msg


    def init_control(self):
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            timeout=130
        )
        return self.serial_port.is_open


    def loop_cmd(self, cmd):
        found_flag = False
        data = ""
        for i in range(0, 5):
            msg = self.command(cmd)
            if (len(msg) != 0):
                data = msg
                break
        return data


#    def retrive_ph_loop(self):
#        try:
#            while True:
#                msg = self.retrive_single_pH_value(v=False)
#                if (len(msg) == 0):
#                    print("read error")
#                    pass
#                else:
#                    pH = self.decode_ph_signal_protocol(msg)
#                print("pH: " + pH)
#                time.sleep(1)
#        except KeyboardInterrupt:
#            print("ctrl-c detected, stop to get values")
#            return
