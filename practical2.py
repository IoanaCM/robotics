##!/usr/bin/env python
#
#
# Hardware:
#
# Results:

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import math
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

try:
    try:
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
    except IOError as error:
        print(error)

    # BP.set_motor_power(BP.PORT_D, BP.MOTOR_FLOAT)                          # float motor D
    BP.set_motor_limits(BP.PORT_A, 70)                                     # optionally set a power limit
    BP.set_motor_limits(BP.PORT_D, 70)                                     # optionally set a power limit
    wheel_radius = 2.8
    robot_width = 22.5
    wheel_circ = 2 * math.pi * wheel_radius
    dps = 360
    dps2 = 360
    square_side = 40
    stop_distance = 10
    error = 0.0725
    error2 = -0.0565
    t1 = stop_distance / (wheel_circ * dps / 360) + error # time to walk 10cm
    rotate_distance = 2 * math.pi * robot_width / 8
    t2 = rotate_distance / (wheel_circ * dps / 360) + error2 # time to rotate
    i = 0
    BP.set_motor_dps(BP.PORT_A, 0)
    BP.set_motor_dps(BP.PORT_D, 0)
    print("Motor D Status: ", BP.get_motor_status(BP.PORT_D))
    print("Motor A Status: ", BP.get_motor_status(BP.PORT_A))
    while i<4:
        i=i+1
        print("Side: ", i, "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))
        print("Side: ", i, "  Motor D Status: ", BP.get_motor_status(BP.PORT_D))
        BP.set_motor_dps(BP.PORT_A, dps)             # set the target speed for motor A in Degrees Per Second
        BP.set_motor_dps(BP.PORT_D, dps2)
        time.sleep(t1)
        BP.set_motor_dps(BP.PORT_D, 0)
        BP.set_motor_dps(BP.PORT_A, 0)
        print("Side: ", i, "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))
        print("Side: ", i, "  Motor D Status: ", BP.get_motor_status(BP.PORT_D))
        BP.set_motor_dps(BP.PORT_A, dps)             # set the target speed for motor A in Degrees Per Second
        BP.set_motor_dps(BP.PORT_D, dps2)
        time.sleep(t1)
        BP.set_motor_dps(BP.PORT_D, 0)
        BP.set_motor_dps(BP.PORT_A, 0)
        print("Side: ", i, "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))
        print("Side: ", i, "  Motor D Status: ", BP.get_motor_status(BP.PORT_D))
        BP.set_motor_dps(BP.PORT_A, dps)             # set the target speed for motor A in Degrees Per Second
        BP.set_motor_dps(BP.PORT_D, dps2)
        time.sleep(t1)
        BP.set_motor_dps(BP.PORT_D, 0)
        BP.set_motor_dps(BP.PORT_A, 0)
        print("Side: ", i, "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))
        print("Side: ", i, "  Motor D Status: ", BP.get_motor_status(BP.PORT_D))
        BP.set_motor_dps(BP.PORT_A, dps)             # set the target speed for motor A in Degrees Per Second
        BP.set_motor_dps(BP.PORT_D, dps2)
        time.sleep(t1)
        BP.set_motor_dps(BP.PORT_D, 0)
        BP.set_motor_dps(BP.PORT_A, 0)
        print("Side: ", i, "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))
        print("Side: ", i, "  Motor D Status: ", BP.get_motor_status(BP.PORT_D))
        BP.set_motor_dps(BP.PORT_A, dps2)
        BP.set_motor_dps(BP.PORT_D, -dps)             # set the target speed for motor A in Degrees Per Second
        time.sleep(t2)
        BP.set_motor_dps(BP.PORT_D, 0)
        BP.set_motor_dps(BP.PORT_A, 0)
    print("Motor A Status: ", BP.get_motor_status(BP.PORT_A))
    print("Motor D Status: ", BP.get_motor_status(BP.PORT_D))
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

