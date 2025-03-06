import time
import gpiozero.output_devices as GPIO

class Fan:
    fan = GPIO(18)

    @staticmethod
    def on():
        Fan.fan.on()

    @staticmethod
    def off():
        Fan.fan.off()

"""Fan.setupFan()
Fan.on()
time.sleep(5)
Fan.off()"""