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


    def command(self, cmd):
        print("Executed command: " + str(cmd))
        self.serial_port.write(serial.to_bytes(cmd))
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


    def retrive_single_pH_value(self):
        cmd = [57, 57, 57, 33, 13]
        msg = self.command(cmd)
        return msg

    def retrive_temperature_value(self):
        cmd = [55, 55, 55, 33, 13]
        msg = self.command(cmd)
        return msg


    def decode_ph_signal_protocol(self, data):
        A = int(data[0])
        B = int(data[1])
        C = int(data[2])
        pH = float(int((A*4096) + (B*64) + C) * 0.001)
        return "{:.4f}".format(pH)

    def decode_temp_signal_protocol(self, data):
        A = int(data[0])
        B = int(data[1])
        temp_F = float(int((A*64) + B) * 0.1)
        temp_C = (temp_F - 32) * (5 / 9)
        return "{:.2f}".format(temp_C)


    def end_calibration(self):
        cmd = [81, 73, 84, 33, 13]
        msg = self.command(cmd)
        return msg


    def init_control(self):
        print("Init device......")
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            timeout=130
        )
        print("Serial port open:" + str(self.serial_port.is_open))
        print("\n")


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
        print(f"{Fore.CYAN}2. Init pH 7 calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}3. End Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}4. Retrive single pH value{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}5. Retrive temperature value(celsius){Style.RESET_ALL}!")
        print(f"{Fore.CYAN}6. Measure pH values (loop){Style.RESET_ALL}!")
        print(f"{Fore.CYAN}7. Exit{Style.RESET_ALL}!\n")
        option = input("What would you like to do?: ")
        print("Selected option:" + option)

        if option == "1":
            print(f"\n{Fore.GREEN}Starting calibration...{Style.RESET_ALL}!\n")
            msg = s.start_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response init calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))

        elif option == "2":
            print(f"\n{Fore.GREEN}Init pH 7{Style.RESET_ALL}!\n")
            msg = s.init_pH7_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response from init ph7 calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))

        elif option == "3":
            print(f"\n{Fore.GREEN}End calibration...{Style.RESET_ALL}!\n")
            msg = s.end_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for end calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))

        elif option == "4":
            print(f"\n{Fore.GREEN}Retrive pH value{Style.RESET_ALL}!\n")
            msg = s.retrive_single_pH_value()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for retrive pH value!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
                tmp = ""
                for i in range(0, len(msg)):
                    tmp = tmp + str(msg[i]) + "  "

                print("Response(dec): " + tmp)
                pH = s.decode_ph_signal_protocol(msg)
                print("\npH = " + pH)


        elif option == "5":
            print(f"\n{Fore.GREEN}Retrive temperature{Style.RESET_ALL}!\n")
            msg = s.retrive_temperature_value()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for retrive temperature value!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
                tmp = ""
                for i in range(0, len(msg)):
                    tmp = tmp + str(msg[i]) + "  "

                print("Response(dec): " + tmp)
                temp = s.decode_temp_signal_protocol(msg)
                print("\nTemperature (Celcius) = " + temp)



        elif option == "6":
            print(f"\n{Fore.GREEN}Starting loop to measure values{Style.RESET_ALL}!\n")


        elif option == "7":
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

