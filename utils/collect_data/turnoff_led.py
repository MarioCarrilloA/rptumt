import RPi.GPIO as GPIO
import time

# Do not confuse with number of pin
gpiono = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpiono, GPIO.OUT)

print("LED off")
GPIO.output(gpiono, GPIO.LOW)
