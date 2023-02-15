# Mock robot designed to simulate all aspects of code except the physical
# turning of motors. This allows testing code without needing the robot
# with you, and no longer requires the brickpi3 module installed.
#
# The signatures of all functions are identical to that of the true robot
# class. As a result to simulate code without the robot, simply change 
# the following 2 lines of code:
#
# import robot        ===>   import mockRobot
# r = robot.robot()   ===>   r = mockRobot.robot()
#
# Since mockRobot no longer drives motors, many functions now do nothing,
# but they are still included and callable, specifically so no additional
# code changes are required.
#
# The mockRobot class must be kept up to date with the real robot class
# any changes to robot should be reflected in mockRobot as the exact same
# code but with any lines referencing self.BP removed
#
# This may be automated by running the Makefile with make mockRobot (or just make)

from math import pi as PI
from math import sin, cos, sqrt, atan2
import numpy as np
from statistics import median, mean
import time
import random

# Class specialised to our robot design

class robot:

    #=========== Constructor function ===========
    def __init__(self):

        # design constants

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


        # particle estimates for position
        num_particles = 100
        self.particles = [((0,0,0), 1/num_particles)] * num_particles
        self.sigma_e = 0.02   # standard deviation in cm      - error of driving too far/short, per unit forward movement
        self.sigma_f = 0.001  # standard deviation in radians - error of turning during forward motion, per unit forward movement
        self.sigma_g = 0.005  # standard deviation in radians - error of turning too far/short, per unit radian spin

        # sensor readings queue
        self.sensor_readings = []

    #========== Private methods - Do not call directly ===========
    def circmean(self, thetas):
        a = mean(np.sin(thetas))
        b = mean(np.cos(thetas))
        x = atan2(a, b)
        z = x if x >= 0 else x + 2 * PI
        return z

    def updateParticleForward(self, particle, distance):
        """
        Update particle prediction for forward movement of 10cm
        particle :: tuple ((x,y,theta),weight)
        """
        ((x,y,theta),weight) = particle

        e = random.gauss(0, distance * self.sigma_e)
        f = random.gauss(0, distance * self.sigma_f)
        #print("theta: " + str(theta) + " new theta: " +   str((theta + f) % (2*PI) ))
        return ((x + (distance + e) * cos(theta), y + (distance + e) * sin(theta), (theta + f) % (2*PI)), weight)


    def updateParticleSpin(self, particle, radians):
        """
        Update particle prediction for left spin PI/2 radians
        particle :: tuple ((x,y,theta),weight)
        """
        ((x,y,theta), weight) = particle

        g = random.gauss(0, radians * self.sigma_g)
        return ((x, y, (theta + radians + g) % (2*PI)), weight)


    def getX(self, particle):
        ((x,_,_),_) = particle
        return x

    def getY(self, particle):
        ((_,y,_),_) = particle
        return y

    def getTheta(self, particle):
        ((_,_,theta),_) = particle
        return theta


    #=========== Public methods ===========

    def setup(self):
        """
        Initialises the motors. Should be called before using other functions
        """

        try:
            #reset servo encoders

            # Set power limits on motors

            time.sleep(0.1)

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
        return

    def stop(self):
        """
        Stops both motors turning
        """
        return

    def forward(self, distance):
        """
        Drives straight forward 'distance' cm
        """
        direction = 1 if distance >=0 else -1
        t = abs(distance) / self.wheel_speed + self.forward_tuning

        time.sleep(max(0,t))
        self.stop()

        new_particles = [self.updateParticleForward(p,distance) for p in self.particles]
        self.particles = new_particles
        return
        

    def spin(self, radians):
        """
        Spins 'radians' radians in place\n
        A positive value for radians is a counter-clockwise (left) spin\n
        A negative value for radians is a clockwise (right) spin
        """

        # direction = 1 for spin left, -1 for spin right
        direction = 1 if radians >= 0 else -1
        distance = abs(radians) * self.robot_width / 2
        t = distance / self.wheel_speed + self.spin_tuning

        time.sleep(max(0,t))
        self.stop()

        new_particles = [self.updateParticleSpin(p,radians) for p in self.particles]
        self.particles = new_particles
        return

    def spinL(self, degrees):
        """
        Spins 'degrees' degrees to the left in place
        """
        self.spin(degrees * PI / 180)
        return

    def spinR(self, degrees):
        """
        Spins 'degrees' degrees to the right in place
        """
        self.spin(-degrees * PI / 180)
        return


    def navigateToWaypoint(self, Wx, Wy):   
        (x, y, theta), (_, _, _) = self.metrics()

        dx = Wx - x
        dy = Wy - y

        alpha = atan2(dy,dx)

        beta = (alpha - theta) % (2*PI)
        beta = beta if beta <= PI else beta - 2*PI
        
        d = sqrt(dx**2 + dy**2)
        
        self.spin(beta)
        self.forward(d)
        return


    def metrics(self):
        """
        Reports mean and standard deviation of particles position array
        particles :: list of tuples [((x,y,theta),weight)]
        Return ((mu_X, mu_y, mu_theta), (sigma_x, sigma_y, sigma_theta))
        """

        xs = list(map(self.getX, self.particles))
        ys = list(map(self.getY, self.particles))
        thetas = list(map(self.getTheta, self.particles))
        return ((mean(xs), mean(ys), self.circmean(thetas)),(np.std(xs), np.std(ys), np.std(thetas)))

    def get_sensor_reading(self):
        try:
            r = 0
            self.sensor_readings.append(r)
            if len(self.sensor_readings) > 5:
                self.sensor_readings.pop(0)
            return median(self.sensor_readings)

            print("Sensor Error: ", e)
            return

        except Exception as e:
            print(e)
            return

