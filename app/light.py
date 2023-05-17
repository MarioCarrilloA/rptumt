import RPi.GPIO as GPIO

class Light():
    def __init__(self):
        # Default pin 18 (GPIO number 24)
        self.gpiono = 24

        # Init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpiono, GPIO.OUT)


    def on(self):
        GPIO.output(self.gpiono, GPIO.HIGH)


    def off(self):
        GPIO.output(self.gpiono, GPIO.LOW)


    def set_GPIO(self, gpiono):
        self.gpiono = gpiono
