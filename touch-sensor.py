from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.


BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)

BP.set_motor_limits(BP.PORT_A, 50, 250) 
BP.set_motor_limits(BP.PORT_D, 50, 250) 

try:
    while True:
        # read and display the sensor value
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
        # BP.get_sensor returns the sensor value (what we want to display).
        try:
            right_value = BP.get_sensor(BP.PORT_1)
            left_value = BP.get_sensor(BP.PORT_4) 

            if left_value == 0 and right_value == 0: #move forward
                BP.set_motor_dps(BP.PORT_A, 250)
                BP.set_motor_dps(BP.PORT_D, 250)
            elif left_value == 1: #maybe right_value == 1 turn right
                BP.set_motor_dps(BP.PORT_A, -250)
                BP.set_motor_dps(BP.PORT_D, -250)
                time.sleep(3)
                BP.set_motor_dps(BP.PORT_A, 0)
                BP.set_motor_dps(BP.PORT_D, 200)
                time.sleep(1.5)
            elif right_value == 1:# turn left
                BP.set_motor_dps(BP.PORT_A, -250)
                BP.set_motor_dps(BP.PORT_D, -250)
                time.sleep(3)
                BP.set_motor_dps(BP.PORT_A, 200)
                BP.set_motor_dps(BP.PORT_D, 0)
                time.sleep(1.5)
            
            

            print(str(left_value) + " " + str(right_value))
            time.sleep(0.02)
        except brickpi3.SensorError as error:
            print(error)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()  
