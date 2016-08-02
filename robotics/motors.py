import Adafruit_BBIO.GPIO as GPIO
import time

class Motor:
    """Motor class"""
    def __init__(self, gpiopin1, gpiopin2):
        self.gpiopin1 = gpiopin1
        self.gpiopin2 = gpiopin2
        # set gpio pins as outputs and set to 0V
        GPIO.setup(gpiopin1, GPIO.OUT)
        GPIO.output(gpiopin1, GPIO.LOW)
        GPIO.setup(gpiopin2, GPIO.OUT)
        GPIO.output(gpiopin2, GPIO.LOW)

    def start(self, forward=True):
        if forward:
            GPIO.output(gpiopin1, GPIO.HIGH)
            GPIO.output(gpiopin2, GPIO.LOW)
        else:
            GPIO.output(gpiopin1, GPIO.LOW)
            GPIO.output(gpiopin2, GPIO.HIGH)

    def stop(self):
        GPIO.output(gpiopin1, GPIO.LOW)
        GPIO.output(gpiopin2, GPIO.LOW)

    def test(self):
        for i in range(10):
            self.start(forward=True)
            time.sleep(1)
            self.start(forward=False)
            time.sleep(2)
        self.stop()






