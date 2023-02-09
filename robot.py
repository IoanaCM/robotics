from math import pi as PI
from math import sin, cos, sqrt, atan2
from numpy import mean, std
from statistics import median
import time
import random
import brickpi3

# Class specialised to our robot design

class robot:

    #=========== Constructor function ===========
    def __init__(self):
        self.BP = brickpi3.BrickPi3()

        # design constants
        self.L = self.BP.PORT_A     # Port used for left wheel
        self.R = self.BP.PORT_D     # Port used for right wheel
        self.sonar = self.BP.PORT_2
        self.BP.set_sensor_type(self.sonar, self.BP.SENSOR_TYPE.NXT_ULTRASONIC)

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
        self.sigma_e = 0.1   # standard deviation in cm      - error of driving too far/short, per unit forward movement
        self.sigma_f = 0.01  # standard deviation in radians - error of turning during forward motion, per unit forward movement
        self.sigma_g = 0.01  # standard deviation in radians - error of turning too far/short, per unit radian spin

        # sensor readings queue
        self.sensor_readings = []

    #========== Private methods - Do not call directly ===========
    def updateParticleForward(self, particle, distance):
        """
        Update particle prediction for forward movement of 10cm
        particle :: tuple ((x,y,theta),weight)
        """
        ((x,y,theta),weight) = particle

        e = random.gauss(0, distance * self.sigma_e)
        f = random.gauss(0, distance * self.sigma_f)
        return ((x + (distance + e) * cos(theta), y + (distance + e) * sin(theta), theta + f), weight)


    def updateParticleSpin(self, particle, radians):
        """
        Update particle prediction for left spin PI/2 radians
        particle :: tuple ((x,y,theta),weight)
        """
        ((x,y,theta), weight) = particle

        g = random.gauss(0, radians * self.sigma_g)
        return ((x, y, (theta + radians + g) % (2*PI)), weight)


    def getX(self, particle):
        ((x,y,theta),weight) = particle
        return x

    def getY(self, particle):
        ((x,y,theta),weight) = particle
        return y

    def getTheta(self, particle):
        ((x,y,theta),weight) = particle
        return theta


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
        direction = 1 if distance >=0 else -1
        t = abs(distance) / self.wheel_speed + self.forward_tuning
        self.BP.set_motor_dps(self.L, direction * self.dps)
        self.BP.set_motor_dps(self.R, direction * self.dps)

        time.sleep(max(0,t))
        self.stop()

        new_particles = [self.updateParticleForward(p,distance) for p in self.particles]
        self.particles = new_particles
        return
        

    def spin(self, radians):

        # direction = 1 for spin left, -1 for spin right
        direction = 1 if radians >= 0 else -1
        distance = abs(radians) * self.robot_width / 2
        t = distance / self.wheel_speed + self.spin_tuning
        self.BP.set_motor_dps(self.L, direction * self.dps)
        self.BP.set_motor_dps(self.R, -direction * self.dps)

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

        beta = alpha - theta
        d = sqrt(dx**2 + dy**2)

        self.spin(beta)
        self.forward(d)
        return


    def metrics(self):
        """
        Reports mean and standard deviation of particles position array
        particles :: list of tuples [((x,y,theta),weight)]
        Return ((mu_X, mu_y), (sigma_x, sigma_y))
        """

        xs = list(map(self.getX, self.particles))
        ys = list(map(self.getY, self.particles))
        thetas = list(map(self.getTheta, self.particles))
        return ((mean(xs), mean(ys), mean(thetas)),(std(xs), std(ys), std(thetas)))

    def get_sensor_reading(self):
        try:
            r = self.BP.get_sensor(self.sonar)
            self.sensor_readings.append(r)
            if len(self.sensor_readings) > 5:
                self.sensor_readings.pop(0)
            return median(self.sensor_readings)                 
        except brickpi3.SensorError as error:
            print(error)
            return