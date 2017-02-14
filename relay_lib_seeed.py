# =========================================================
# Seeed Studio Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
#
# Modified from the sample code on the Seeed Studio Wiki
# http://wiki.seeed.cc/Raspberry_Pi_Relay_Board_v1.0/
# =========================================================

from __future__ import print_function

import smbus

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

# Change the following value if your Relay board uses a different I2C address. 
DEVICE_ADDRESS = 0x20  # 7 bit address (will be left shifted to add the read write bit)

# Don't change the values, there's no need for that.
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff


def relay_on(relay_num):
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num < 5:
            print('Turning relay', relay_num, 'ON')
            DEVICE_REG_DATA &= ~(0x1 << (relay_num - 1))
            bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
        else:
            print('Invalid relay #:', relay_num)
    else:
        print('Relay number must be an Integer value')


def relay_off(relay_num):
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num < 5:
            print('Turning relay', relay_num, 'OFF')
            DEVICE_REG_DATA |= (0x1 << (relay_num - 1))
            bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
        else:
            print('Invalid relay #:', relay_num)
    else:
        print('Relay number must be an Integer value')


def relay_all_on():
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    print('Turning all relays ON')
    DEVICE_REG_DATA &= ~(0xf << 0)
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)


def relay_all_off():
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    print('Turning all relays OFF')
    DEVICE_REG_DATA |= (0xf << 0)
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
