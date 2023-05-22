import RPi.GPIO as GPIO

class Light():
    """
    This class sets the status for GPIOs on Raspberry Pi 4 board
    in order to handle a lamp to illuminate the bioreactor chamber.
    """
    def __init__(self):
        # Default pin 18 (GPIO number 24)
        self.gpiono = 24

        # Init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpiono, GPIO.OUT)


    def on(self):
        """
        Sets GPIO on high state to turn on the lamp
        """
        GPIO.output(self.gpiono, GPIO.HIGH)


    def off(self):
        """
        Sets GPIO on low state to turn off the lamp
        """
        GPIO.output(self.gpiono, GPIO.LOW)


    def set_GPIO(self, gpiono):
        """
        Changes another GPIO
        """
        self.gpiono = gpiono
