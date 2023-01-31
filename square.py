#!/usr/bin/env python
#
# 
# Hardware:
#
# Results:

#uncomment these if they were actually needed, else im deleting them
#from __future__ import print_function # use python 3 syntax but make it compatible with python 2
#from __future__ import division

import time
from math import pi as PI
import brickpi3
from constants import *


def init(BP):
    try:
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D

        BP.set_motor_limits(BP.PORT_A, 50) # Set power limits on motors
        BP.set_motor_limits(BP.PORT_D, 50)

    except IOError as error:
        print(error)


def main():
    BP = brickpi3.BrickPi3()

    try:
        
        init(BP)
        
        error = 0.1
        square_side = 40 #cm
        dps = 360 #target degrees per second speed

        t1 = square_side / (wheel_circ * dps / 360) + error # time to walk a side

        rotate_distance = PI * robot_width / 4
        t2 = rotate_distance / (wheel_circ * dps / 360) - error/2 #time to spin 90 degrees

        while True:
            BP.set_motor_dps(BP.PORT_A, dps) #set the target speed for motor A in Degrees Per Second
            BP.set_motor_dps(BP.PORT_D, dps)
            
            time.sleep(t1)
            
            BP.set_motor_dps(BP.PORT_D, dps)
            BP.set_motor_dps(BP.PORT_A, -dps)
            
            time.sleep(t2)
            
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        return


if __name__ == "__main__":
    main()
