from pHsensor import *

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

