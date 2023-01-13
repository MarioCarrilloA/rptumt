import RPi.GPIO as GPIO
import time

# Do not confuse with number of pin
gpiono = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpiono, GPIO.OUT)

GPIO.output(gpiono, GPIO.HIGH)
print("LED on")
