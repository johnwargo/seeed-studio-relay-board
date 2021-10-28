# =========================================================
# Seeed Studio Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
#
# Modified from the sample code on the Seeed Studio Wiki
# http://wiki.seeed.cc/Raspberry_Pi_Relay_Board_v1.0/
#
# 2021-10-28: modified by Krystof Remes for remote usage over ethernet
# =========================================================

from __future__ import print_function
import pigpio

# The number of relay ports on the relay board.
# This value should never change!
NUM_RELAY_PORTS = 4

# Change the following value if your Relay board uses a different I2C address.
I2C_BUS = 1
DEVICE_ADDRESS = 0x21  # 7 bit address (will be left shifted to add the read write bit)
DEVICE_IP = "192.168.0.68"

# Don't change the values, there's no need for that.
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff

def relay_on(relay_num):
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num <= NUM_RELAY_PORTS:
            pi = pigpio.pi(DEVICE_IP)
            print('Turning relay', relay_num, 'ON')
            DEVICE_REG_DATA &= ~(0x1 << (relay_num - 1))
            i2c_handle = pi.i2c_open(I2C_BUS, DEVICE_ADDRESS, 0)
            pi.i2c_write_byte_data(i2c_handle, DEVICE_REG_MODE1, DEVICE_REG_DATA)
            pi.i2c_close(i2c_handle)
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
        if 0 < relay_num <= NUM_RELAY_PORTS:
            pi = pigpio.pi(DEVICE_IP)
            print('Turning relay', relay_num, 'OFF')
            DEVICE_REG_DATA |= (0x1 << (relay_num - 1))
            i2c_handle = pi.i2c_open(I2C_BUS, DEVICE_ADDRESS, 0)
            pi.i2c_write_byte_data(i2c_handle, DEVICE_REG_MODE1, DEVICE_REG_DATA)
            pi.i2c_close(i2c_handle)
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
    print(DEVICE_IP)
    pi = pigpio.pi(DEVICE_IP)
    i2c_handle = pi.i2c_open(I2C_BUS, DEVICE_ADDRESS, 0)
    pi.i2c_write_byte_data(i2c_handle, DEVICE_REG_MODE1, DEVICE_REG_DATA)
    pi.i2c_close(i2c_handle)


def relay_all_off():
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    print('Turning all relays OFF')
    DEVICE_REG_DATA |= (0xf << 0)
    print(DEVICE_IP)
    pi = pigpio.pi(DEVICE_IP)
    i2c_handle = pi.i2c_open(I2C_BUS, DEVICE_ADDRESS, 0)
    pi.i2c_write_byte_data(i2c_handle, DEVICE_REG_MODE1, DEVICE_REG_DATA)
    pi.i2c_close(i2c_handle)


def relay_toggle_port(relay_num):
    print('Toggling relay:', relay_num)
    if relay_get_port_status(relay_num):
        # it's on, so turn it off
        relay_off(relay_num)
    else:
        # it's off, so turn it on
        relay_on(relay_num)


def relay_get_port_status(relay_num):
    # determines whether the specified port is ON/OFF
    global DEVICE_REG_DATA
    print('Checking status of relay', relay_num)
    res = relay_get_port_data(relay_num)
    if res > 0:
        mask = 1 << (relay_num - 1)
        # return the specified bit status
        # return (DEVICE_REG_DATA & mask) != 0
        return (DEVICE_REG_DATA & mask) == 0
    else:
        # otherwise (invalid port), always return False
        print("Specified relay port is invalid")
        return False


def relay_get_port_data(relay_num):
    # gets the current byte value stored in the relay board
    global DEVICE_REG_DATA
    print('Reading relay status value for relay', relay_num)
    # do we have a valid port?
    if 0 < relay_num <= NUM_RELAY_PORTS:
        pi = pigpio.pi(DEVICE_IP)
        # read the memory location
        i2c_handle = pi.i2c_open(I2C_BUS, DEVICE_ADDRESS, 0)
        DEVICE_REG_DATA = pi.i2c_read_byte_data(i2c_handle, DEVICE_REG_MODE1)
        pi.i2c_close(i2c_handle)
        # return the specified bit status
        return DEVICE_REG_DATA
    else:
        # otherwise (invalid port), always return 0
        print("Specified relay port is invalid")
        return 0
