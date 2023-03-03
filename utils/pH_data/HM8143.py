# Software to handle HAMEG Instruments,HM8143,2.41
# power supply in remote mode

import serial
import time
import os
import numpy as np
import signal
import sys


DEFAULT_CURRENT = 0.20
DEFAULT_VOLTAGE = 7.40
INIT_VOLTAGE_SEQ = 7.80
STOP_VOLTAGE_SEQ = 9.00
STEP_VOLTAGE_SEQ = 0.24

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
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB1',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            bytesize=8,
            stopbits=1,
            timeout=1
        )
        return self.get_id()


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
        format_voltage = "{:.2f}".format(voltage)
        cmd = "SU1:" + format_voltage
        msg = self.command(cmd)
        return msg


    def loop_cmd(self, cmd):
        found_flag = False
        data = ""
        for i in range(0, 5):
            msg = self.command(cmd)
            if (len(msg) != 0):
                data = msg
                break
        return data


    def get_id(self):
        data = self.loop_cmd("*IDN?")
        if (len(data) != 0):
            return data
        else:
            return "error: device does not answer"


    def get_voltage(self):
        data = self.loop_cmd("MU1")
        if (len(data) != 0):
            return data
        return


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
        for v in np.arange(INIT_VOLTAGE_SEQ, STOP_VOLTAGE_SEQ, STEP_VOLTAGE_SEQ):
            strv = "{:.2f}".format(v)
            voltage = "SU1:" + strv
            print("Set voltage: " + strv)
            self.set_voltage(voltage)
            if flag_output == False:
                flag_output = True
                self.enable_output()
            self.get_voltage()
            time.sleep(1)


    def set_default_current(self):
        strcurr = str(DEFAULT_CURRENT)
        print("Set default current: " + strcurr)
        current = "SI1:" + strcurr
        msg = self.command(current)


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


    def clear_device(self):
        """ This funcion cleans all configurations in the
        device. The voltage and currnet are set to 0 and the
        outputs are switched off.
        """
        print("Clear device")
        msg = self.command("CLR")


def main():
    s = serialPowerSupply()
    s.init_control()
    s.enable_mixed_mode()
    s.set_default_current()
    s.run_voltage_sequence()
    s.disable_output()
    s.finish()

if __name__ == "__main__":
    main()

