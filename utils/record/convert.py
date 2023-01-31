import subprocess

process = subprocess.Popen(['python', '/home/pi/Documents/Thesis/rptumt/utils/serial/serial_HM8143_power_supply.py'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

stdout, stderr = process.communicate()

print(stdout)
print(stderr)
