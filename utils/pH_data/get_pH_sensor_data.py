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


    def readline_cr(self):
        EOL = b'\r'
        #EOL = b'3'
        line = bytearray()
        while True:
            print("reading")
            c = self.serial_port.read(1)
            #print(c)
            if c:
                line += c
                if line[-len(EOL):] == EOL:
                    break
            else:
                break
        return line.decode("UTF-8")


    def command(self, cmd):
        print("Executed command: " + cmd)
        #self.serial_port.write(cmd.encode("UTF-8"))
        self.serial_port.write(cmd.encode())
        #self.serial_port.write(cmd)
        #time.sleep(60)
        #data = self.readline_cr()
        data = self.serial_port.readline()
        #return data.decode("UTF-8")
        return data.decode()
        #print(data)
        #data = self.serial_port.readline()
        #print(data)

        return data

    def start_calibration(self):
        msg = self.command('CLR!\r')
        return msg

    def init_pH7_calibration(self):
        msg = self.command('113!\r')
        return msg

    def retrive_single_pH_value(self):
        msg = self.command('999!\r')
        return msg


    def end_calibration(self):
        msg = self.command('QIT!\r')
        return msg


    # Possible baudrate
    # - 9600
    # - 115200
    def init_control(self):
        print("Init device......")
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            timeout=10
        )
        print("Serial port open:" + str(self.serial_port.is_open))
        print("\n")
        #self.print_id()


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
    s.init_control()

    while True:
        print(f"{Fore.CYAN}1. Start Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}2. End Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}3. Init pH 7 calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}4. Retrive single pH value{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}5. Measure pH values (loop){Style.RESET_ALL}!")
        print(f"{Fore.CYAN}6. Exit{Style.RESET_ALL}!\n")
        option = input("What would you like to do?: ")
        print("Selected option:" + option)
        if option == "1":
            print(f"\n{Fore.GREEN}Starting calibration...{Style.RESET_ALL}!\n")
            msg = s.start_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response init calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
            pass

        elif option == "2":
            print(f"\n{Fore.GREEN}End calibration...{Style.RESET_ALL}!\n")
            msg = s.end_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for end calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))

            pass

        elif option == "3":
            print(f"\n{Fore.GREEN}Init pH 7{Style.RESET_ALL}!\n")
            msg = s.init_pH7_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response from init ph7 calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))


        elif option == "4":
            print(f"\n{Fore.GREEN}Retrive pH value{Style.RESET_ALL}!\n")
            msg = s.retrive_single_pH_value()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for retrive pH value!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
            print("Waiting for stabilization")
            time.sleep(10)


        elif option == "5":
            print(f"\n{Fore.GREEN}Starting loop to measure values{Style.RESET_ALL}!\n")

        elif option == "6":
            s.serial_port.close()
            print(f"\n{Fore.GREEN}Exit!{Style.RESET_ALL}!\n")
            break

        else:
            print(f"\n{Fore.RED}error: unknown option!{Style.RESET_ALL}!\n")


        print("\n")
        x = input("press a key to continue...")
        click.clear()

if __name__ == "__main__":
    main()

