from math import pi as PI
from math import sin, cos, atan2, sqrt
import time
import brickpi3

# Class specialised to our robot design

class robot:

    #=========== Constructor function ===========
    def __init__(self):
        self.BP = brickpi3.BrickPi3()

        # design constants
        self.L = self.BP.PORT_A     # Port used for left wheel
        self.R = self.BP.PORT_D     # Port used for right wheel

        # calibration constants
        self.wheel_radius = 2.8     # radius of robot wheels (cm)
        self.robot_width = 23       # width between wheels of robot (cm)
        self.dps = 360              # desired wheel speed (degrees per second)

        #manually calibrated tuning to adjust error
        self.forward_tuning = 0.0725    # increasing makes the robot drive further
        self.spin_tuning = -0.013       # increasing makes the robot turn more


        # constants calculated from configurable constants (should not be changed)
        self.wheel_circ = 2 * PI * self.wheel_radius            # circumference of robot wheels
        self.wheel_speed = self.wheel_circ * self.dps / 360     # speed wheels should turn


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
        self.stop()
        time.sleep(0.5)
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

    def spin(self, radians):

        # direction = 1 for spin left, -1 for spin right
        direction = 1 if radians >= 0 else -1
        distance = radians * self.robot_width / 2
        t = distance / self.wheel_speed + self.spin_tuning
        self.BP.set_motor_dps(self.L, direction * self.dps)
        self.BP.set_motor_dps(self.R, -direction * self.dps)

        time.sleep(t)

        self.stop()
        return

    def spinL(self, degrees):
        """
        Spins 'degrees' degrees to the left in place
        """
        self.private_spin(1, degrees * PI / 180)

        return

    def spinR(self, degrees):
        """
        Spins 'degrees' degrees to the right in place
        """
        self.private_spin(-1, degrees * PI / 180)

        return

    def navigateToWaypoint(self, Wx, Wy):        
        x = 0 # TODO: Replace with estimated positions
        y = 0
        theta = 0 

        dx = Wx - x
        dy = Wy - y

        alpha = atan2(dy,dx)

        beta = alpha - theta
        d = sqrt(dx**2 + dy**2)

        self.spin(beta)
        self.forward(d)
        return
