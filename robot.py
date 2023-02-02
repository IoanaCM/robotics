from math import pi as PI
import time
import brickpi3

# Class specialised to our robot design

class robot:

    #=========== Constructor function ===========
    def __init__(self):
        self.BP = brickpi3.BrickPi3()

        # design constants
        self.L = self.BP.PORT_A     #Port used for left wheel
        self.R = self.BP.PORT_D     #Port used for right wheel

        # calibration constants
        self.wheel_radius = 2.8     #radius of robot wheels (cm)
        self.robot_width = 24       #width between wheels of robot (cm)
        self.dps = 360              #desired wheel speed (degrees per second)     

        self.forward_tuning = 0.0725    #manually calibrated error
        self.spin_tuning = 0.018


        #constants calculated from configurable constants (should not be changed)
        self.wheel_circ = 2 * PI * self.wheel_radius            #circumference of robot wheels
        self.wheel_speed = self.wheel_circ * self.dps / 360     #speed wheels should turn


    #========== Private methods - Do not call directly ===========
    def private_spin(self, direction, radians):
        """
        PRIVATE METHOD - DO NOT CALL THIS METHOD\n
        Use spinL and spinR instead
        """

        #direction = 1 for spin left, -1 for spin right
        t = radians / self.wheel_speed + self.spin_tuning
        self.BP.set_motor_dps(self.L, -direction * self.dps)
        self.BP.set_motor_dps(self.R, direction * self.dps)

        time.sleep(t)

        self.BP.set_motor_dps(self.L, 0)
        self.BP.set_motor_dps(self.R, 0)

        self.stop()
        return


    #=========== Public methods ===========

    def setup(self):
        """
        Initialises the motors. Should be called before using other functions
        """

        try:
            #reset servo encoders
            self.BP.offset_motor_encoder(self.L, self.BP.get_motor_encoder(self.L))
            self.BP.offset_motor_encoder(self.R, self.BP.get_motor_encoder(self.R))

            # Set power limits on motors
            self.BP.set_motor_limits(self.L, 50) 
            self.BP.set_motor_limits(self.R, 50)

        except IOError as error:
            print(error)

        return

    def shutdown(self):
        """
        Should be called at end of code\n
        Unconfigures the sensors, disables the motors, and restores the LED to the control of the BrickPi3 firmware
        """
        self.BP.reset_all() 

    def stop(self):
        """
        Stops both motors turning
        """
        self.BP.set_motor_dps(self.L, 0)
        self.BP.set_motor_dps(self.R, 0)
        return

    def forward(self, distance):
        """
        Drives straight forward 'distance' cm
        """
        t = distance / self.wheel_speed + self.forward_tuning
        self.BP.set_motor_dps(self.L, self.dps)
        self.BP.set_motor_dps(self.R, self.dps)
            
        time.sleep(t)

        self.stop()
        return

    def spinL(self, radians):
        """
        Spins 'radians' radians to the left in place
        """
        self.private_spin(1, radians)
        return

    def spinR(self, radians):
        """
        Spins 'radians' radians to the right in place
        """
        self.private_spin(-1, radians)
        return

