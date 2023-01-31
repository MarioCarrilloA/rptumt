# Software to handle HAMEG Instruments,HM8143,2.41
# power supply in remote mode

import serial
import time
import os
import numpy as np
import signal
import sys

class serialPowerSupply():
    def __init__(self):
        self.serial_port = None

    def readline_cr(self):
        EOL = b'\r'
        line = bytearray()
        while True:
            c = self.serial_port.read(1)
            if c:
                line += c
                if line[-len(EOL):] == EOL:
                    break
            else:
                break
        return line.decode("UTF-8")

    def command(self, cmd):
        self.serial_port.write(cmd.encode("UTF-8"))
        time.sleep(0.5)
        data = self.readline_cr()
        self.serial_port.flush()

        return data

    def init_control(self):
        print("Init device......")
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            bytesize=8,
            stopbits=1,
            timeout=1
        )
        self.print_id()

    def enable_mixed_mode(self):
        print("Enable mixed mode")
        msg = self.command("MX1")

    def disable_mixed_mode(self):
        print("Disable mixed mode")
        msg = self.command("MX0")


    def enable_remote_mode(self):
        print("Enable remote mode")
        msg = self.command("RM1")


    def disable_remote_mode(self):
        print("Disable remote mode")
        msg = self.command("RM0")


    def finish(self):
        print("Finish")
        self.disable_mixed_mode()
        self.serial_port.flush()
        self.serial_port.close()
        sys.exit(0)


    def set_voltage(self, voltage):
        print("Set voltage")
        msg = self.command(voltage)


    def loop_cmd(self, cmd):
        found_flag = False
        data = ""
        for i in range(0, 5):
            msg = self.command(cmd)
            if (len(msg) != 0):
                found_flag = True
                print(msg)
                break
        if (found_flag == False):
            print("error: no possible to get an answer")


    def print_id(self):
        print("Looking for device id")
        self.loop_cmd("*IDN?")


    def get_voltage(self):
        print("Voltage:")
        self.loop_cmd("MU1")

    def print_status(self):
        found_flag = False
        for i in range(0, 10):
            msg = self.command("STA?")
            if (len(msg) != 0):
                found_flag = True
                print(msg)
                break
        if (found_flag == False):
            print("error: Unknown device id")


    def run_voltage_sequence(self):
        flag_output = False
        for v in np.arange(7.80, 9.00, 0.24):
            voltage = "SU1:{:.2f}".format(v)
            print(voltage)
            self.set_voltage(voltage)
            if flag_output == False:
                self.enable_output()
            self.get_voltage()
            time.sleep(1)


    def enable_output(self):
        print("Enable output")
        msg = self.command("OP1")


    def disable_output(self):
        print("Disable output")
        msg = self.command("OP0")


    def finish(self):
        print("Finish")
        self.disable_mixed_mode()
        self.serial_port.flush()
        self.serial_port.close()
        sys.exit(0)

def main():
    s = serialPowerSupply()
    s.init_control()
    s.enable_mixed_mode()
    s.run_voltage_sequence()
    s.set_voltage("SU1:9.00")
    s.enable_output()
    s.get_voltage()
    time.sleep(5)
    s.print_status()
    s.disable_output()
    s.finish()

if __name__ == "__main__":
    main()

