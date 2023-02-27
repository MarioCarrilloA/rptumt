# Software to handle Sentron pH sensor

import serial
import time
import os
import numpy as np
import signal
import sys

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


class serialpHSensor():
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
        time.sleep(0.2)
        data = self.readline_cr()
        return data

    def start_calibration(self):
        msg = self.command("CLR!\r")
        return msg

    def end_calibration(self):
        msg = self.command("QIT!\r")
        return msg



    def start_redundant_calibration(self):
        data = self.loop_cmd("CLR!\r")
        if (len(data) != 0):
            print("Measured voltage: " + data)
        else:
            print("Measured voltage: UNKNOWN!")
    

    # Possible baudrate
    # - 9600
    # - 115200
    def init_control(self):
        print("Init device......")
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            bytesize=8,
            stopbits=1,
            timeout=5
        )
        self.print_id()


    def loop_cmd(self, cmd):
        found_flag = False
        data = ""
        for i in range(0, 5):
            msg = self.command(cmd)
            if (len(msg) != 0):
                data = msg
                break
        return data


def main():
    colorama_init()
    s = serialpHSensor()

    while True:
        print(f"{Fore.CYAN}1. Start Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}2. End Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}3. Init pH 7 calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}5. Measure pH values (loop){Style.RESET_ALL}!")
        print(f"{Fore.CYAN}5. Exit{Style.RESET_ALL}!\n")
        option = input("What would you like to do?: ")
        if option == "1":
            print(f"\n{Fore.GREEN}Starting calibration...{Style.RESET_ALL}!\n")
            msg = s.start_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: unsuccessful init calibration!{Style.RESET_ALL}!\n")
            else:
                print(msg)
                print("done")

        if option == "2":
            print(f"\n{Fore.GREEN}End calibration...{Style.RESET_ALL}!\n")
            msg = s.end_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: unsuccessful end calibration!{Style.RESET_ALL}!\n")
            else:
                print(msg)
                print("done")


        elif option == "2":
            print(f"\n{Fore.GREEN}Init pH 7{Style.RESET_ALL}!\n")

        elif option == "3":
            print(f"\n{Fore.GREEN}Startibg loop to measure values{Style.RESET_ALL}!\n")

        elif option == "4":
            print(f"\n{Fore.GREEN}Exit!{Style.RESET_ALL}!\n")
            break

        else:
            print(f"\n{Fore.RED}error: unknown option!{Style.RESET_ALL}!\n")



if __name__ == "__main__":
    main()

