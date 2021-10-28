from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import remote_relay_lib_seeed as rls


while True:
    rls.DEVICE_IP = "192.168.0.68"
    rls.relay_all_on()
    sleep(2)
    rls.relay_all_off()
    sleep(2)