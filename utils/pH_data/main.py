import csv
import sys
import serial.tools.list_ports

from datetime import datetime
from pHsensor import *
from HM8143 import *
from textwrap import dedent

msg_help = dedent(
        """
        This program is designed for getting pH and temperature (celsius)
        values from the ISFET pH-sensor kit (from the company: Sentron) and control
        the voltage output from a power supply HM8143 in order to create a dataset.
        It is very important to follow sequentially these steps to work correctly:

        1) Connect the pH sensor to the board to obtain the /dev/ttyUSB0 device
        2) Conncet the power supply to the board to obtain the /dev/ttyUSB1 devide
        3) Select the option 1, 2, and 3 to calibarte the sensor
        4) Check the results using option 4 and 5\n
        """)

device_0 = "/dev/ttyUSB0"
device_1 = "/dev/ttyUSB1"

def check_connected_devs(connected_ports, dev):
    for p in connected_ports:
        if (dev in p):
            return True
    return False

def create_dataset_dir():
    now = datetime.now()
    dirname = "dataset_" + now.strftime("%d_%m_%Y-%H_%M_%S")
    try:
        os.mkdir(dirname)
        print("Output directory:" , dirname, " created ")
    except FileExistsError:
        print("Output directory:" , dirname,  " already exists")

    return dirname

def main():
    colorama_init()
    connected_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    if (check_connected_devs(connected_ports, device_0) == True):
        print(device_0 + " found!")
        pH_sensor = serialpHSensor()
        r = pH_sensor.init_control()
        print("pH sensor init: " + str(r))
    else:
        print(f"\n{Fore.RED}error: connected devices no detected{Style.RESET_ALL}!\n")
        sys.exit(1)


    if (check_connected_devs(connected_ports, device_1) == True):
        power_supply = serialPowerSupply()
        r = power_supply.init_control()
        print("Power supply device: " + str(r))
    else:
        print(f"\n{Fore.YELLOW}warning: /dev/ttyUSB1 no dtected{Style.RESET_ALL}!\n")


    print(msg_help)
    while True:
        print(f"{Fore.CYAN}1. Start Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}2. Init pH 7 calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}3. End Calibration{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}4. Retrive single pH value{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}5. Retrive temperature value(celsius){Style.RESET_ALL}!")
        print(f"{Fore.CYAN}6. Retrive actual voltage{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}7. Measure pH values (loop){Style.RESET_ALL}!")
        print(f"{Fore.CYAN}8. Collect full dataset{Style.RESET_ALL}!")
        print(f"{Fore.CYAN}9. Exit{Style.RESET_ALL}!\n")
        option = input("What would you like to do?: ")
        print("Selected option:" + option)

        if option == "1":
            print(f"\n{Fore.GREEN}Starting calibration...{Style.RESET_ALL}!\n")
            msg = pH_sensor.start_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response init calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))


        elif option == "2":
            print(f"\n{Fore.GREEN}Init pH 7{Style.RESET_ALL}!\n")
            msg = pH_sensor.init_pH7_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response from init ph7 calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))


        elif option == "3":
            print(f"\n{Fore.GREEN}End calibration...{Style.RESET_ALL}!\n")
            msg = pH_sensor.end_calibration()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for end calibration!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))


        elif option == "4":
            print(f"\n{Fore.GREEN}Retrive pH value{Style.RESET_ALL}!\n")
            msg = pH_sensor.retrive_single_pH_value()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for retrive pH value!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
                tmp = ""
                for i in range(0, len(msg)):
                    tmp = tmp + str(msg[i]) + "  "

                print("Response(dec): " + tmp)
                pH = pH_sensor.decode_ph_signal_protocol(msg)
                print("\npH = " + pH)


        elif option == "5":
            print(f"\n{Fore.GREEN}Retrive temperature{Style.RESET_ALL}!\n")
            msg = pH_sensor.retrive_temperature_value()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for retrive temperature value!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
                tmp = ""
                for i in range(0, len(msg)):
                    tmp = tmp + str(msg[i]) + "  "

                print("Response(dec): " + tmp)
                if len(msg) == 0:
                    print(f"\n{Fore.RED}error: no enough information to decode{Style.RESET_ALL}!\n")
                else:
                    temp = pH_sensor.decode_temp_signal_protocol(msg)
                    print("\nTemperature (Celcius) = " + temp)


        elif option == "6":
            print(f"\n{Fore.GREEN}Rertive actual voltage{Style.RESET_ALL}!\n")
            power_supply.enable_mixed_mode()
            msg = power_supply.get_voltage()
            if len(msg) == 0:
                print(f"\n{Fore.RED}error: no response for retrive temperature value!{Style.RESET_ALL}!\n")
            else:
                print("Response: " + str(msg))
            power_supply.disable_mixed_mode()

        elif option == "7":
            print(f"\n{Fore.GREEN}Retrive pH values into a loop{Style.RESET_ALL}!\n")
            outdir = create_dataset_dir()
            init_time = 0
            logfile = outdir + "/" + "pH.csv"
            with open(logfile, 'w') as f:
                header = ['time', 'pH']
                writer = csv.writer(f)
                writer.writerow(header)
                try:
                    while True:
                        msg = pH_sensor.retrive_single_pH_value(v=False)
                        if (len(msg) == 0):
                            print("read error")
                            pass
                        else:
                            pH = pH_sensor.decode_ph_signal_protocol(msg)
                            current_time = datetime.now()
                            if (init_time == 0):
                                init_time = current_time

                            sample_time = current_time - init_time
                            data = [sample_time, pH]
                            writer.writerow(data)
                            print("time: " + str(sample_time) + " pH: " + pH)
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("ctrl-c detected, stop to get values")
                    pass


        elif option == "8":
            print(f"\n{Fore.GREEN}Collect full dataset{Style.RESET_ALL}!\n")
            for i in range (0, 20):
                if i % 2:
                    msg = power_supply.set_voltage(7.2)
                    print(msg)
                else:
                    msg = power_supply.set_voltage(8.5)
                    print(msg)
                time.sleep(0.2)


        elif option == "9":
            pH_sensor.serial_port.close()
            print(f"\n{Fore.GREEN}Exit!{Style.RESET_ALL}!\n")
            break


        else:
            print(f"\n{Fore.RED}error: unknown option!{Style.RESET_ALL}!\n")


        print("\n")
        x = input("press a key to continue...")
        click.clear()

if __name__ == "__main__":
    main()

