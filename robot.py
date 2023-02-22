from math import pi as PI
from math import sin, cos, sqrt, atan2
import numpy as np
from statistics import median, mean
import time
import random
import ioInterface
#import environment
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
        self.sonar_offset = -1.5      # offset to account for sonar not being at robot centre
                                    #  positive value if sonar is in front of center
                                    #  measured in cm

        #manually calibrated tuning to adjust error
        self.forward_tuning = 0.0725    # increasing makes the robot drive further
        self.spin_tuning = -0.002       # increasing makes the robot turn more ## maybe 0.015 is better???


        # constants calculated from configurable constants (should not be changed)
        self.wheel_circ = 2 * PI * self.wheel_radius            # circumference of robot wheels
        self.wheel_speed = self.wheel_circ * self.dps / 360     # speed wheels should turn


        # particle estimates for position
        num_particles = 100
        self.particles = [((84,30,0), 1/num_particles)] * num_particles
        self.sigma_e = 0.015   # standard deviation in cm      - error of driving too far/short, per unit forward movement
        self.sigma_f = 0.0015  # standard deviation in radians - error of turning during forward motion, per unit forward movement
        self.sigma_g = 0.006   # standard deviation in radians - error of turning too far/short, per unit radian spin

        self.sonar_sigma = 2.5  # standard deviation in cm - error in sonar reading
        self.sonar_K = 0.1      # scalar offset in cm - error in sonar reading

        # set with robot.setEnvironment(environment.Map)
        self.map = None

    #========== Private methods - Do not call directly ===========
    def circmean(self, thetas):
        a = mean(np.sin(thetas))
        b = mean(np.cos(thetas))
        x = atan2(a, b)
        z = x if x >= 0 else x + 2 * PI
        return z

    def moveParticleForward(self, particle, distance):
        """
        Update particle prediction for forward movement of distance cm
        particle :: tuple ((x,y,theta),weight)
        """
        ((x,y,theta),weight) = particle

        e = random.gauss(0, distance * self.sigma_e)
        f = random.gauss(0, distance * self.sigma_f)
        return ((x + (distance + e) * cos(theta), y + (distance + e) * sin(theta), (theta + f) % (2*PI)), weight)


    def moveParticleSpin(self, particle, radians):
        """
        Update particle prediction for left spin radians radians
        particle :: tuple ((x,y,theta),weight)
        """
        ((x,y,theta), weight) = particle

        g = random.gauss(0, radians * self.sigma_g)
        return ((x, y, (theta + radians + g) % (2*PI)), weight)


    def updateParticles(self,particles):
        z = self.get_sensor_reading() #step 2

        for i in range(len(particles)):
            ((x,y,theta),weight) = particles[i]
            particles[i] = ((x,y,theta), weight * self.calculate_likelihood(x,y,theta,z))

        #normalise so sum of weights = 1 #step 3
        total = 0
        for (_, weight) in particles:
            total += weight

        for i in range(len(particles)):
            ((x,y,theta),weight) = particles[i]
            particles[i] = ((x,y,theta),weight / total)
        
        ioInterface.drawParticles(particles)
        time.sleep(1)
        #resample particles #step 4
        self.particles = self.resample(particles)
        ioInterface.drawParticles(self.particles)
     

    def resample(self, particles):
        bins = []
        acc = 0
        for i in range(len(particles)):
            acc+=particles[i][1]
            bins.append(acc)
        new_particles = []
        for _ in range(len(particles)):
            k = 0
            x = random.uniform(0, 1)
            while(x<bins[k] and k < len(particles) - 1):
                k=k+1
            new_particles.append((particles[k][0], 1 / len(particles)))
        return new_particles

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
        Initialises the motors. Must be called before using other functions
        """

        try:
            #reset servo encoders
            self.BP.offset_motor_encoder(self.L, self.BP.get_motor_encoder(self.L))
            self.BP.offset_motor_encoder(self.R, self.BP.get_motor_encoder(self.R))

            # Set power limits on motors
            self.BP.set_motor_limits(self.L, 50)
            self.BP.set_motor_limits(self.R, 50)

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
        self.BP.reset_all()
        return

    def setEnvironment(self, environment):
        """
        Sets the world map the robot is running within\n
        Must be set before calling getDistanceToWallFacing
        """
        self.map = environment

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

        new_particles = [self.moveParticleForward(p,distance) for p in self.particles] # step1
        self.updateParticles(new_particles)

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
        self.BP.set_motor_dps(self.L, direction * self.dps)
        self.BP.set_motor_dps(self.R, -direction * self.dps)

        time.sleep(max(0,t))
        self.stop()

        new_particles = [self.moveParticleSpin(p,radians) for p in self.particles]
        self.updateParticles(new_particles)

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
        """
        Travel to the the point Wx,Wy in world coordinates
        """   


        (x, y, theta), (_, _, _) = self.metrics()

        dx = Wx - x
        dy = Wy - y

        alpha = atan2(dy,dx)

        beta = (alpha - theta) % (2*PI)
        beta = beta if beta <= PI else beta - 2*PI

        d = sqrt(dx**2 + dy**2)
        self.spin(beta)
        print("Turning: " + str(180/PI * beta))
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

    def calculate_likelihood(self, x, y, theta, z):
        """
        implemented yet
        """
        # find out which wall the sonar beam would hit first and
        # calculate expected depth measurement m that should be recorded
        m = self.getDistanceToWallFacing(x, y, theta)
        return np.random.normal(z-m, self.sonar_sigma) + self.sonar_K

    def getDistanceToWallFacing(self, x, y, theta):
        """
        Get the distance to the wall the robot is currently facing\n
        Requires robot environment map to be set with robot.setEnvironment(environment.Map)
        """
        if not self.map:
            raise NoEnvironmentException("No environment map set. Use robot.setEnvironment(environment.Map)")
            
        minM = 256 # max sonar reading is 255
        for (Ax,Ay,Bx,By) in self.map.walls:
            try:
                m = self.getDistanceToWall(x,y,theta,Ax,Ay,Bx,By)
                minM = min(m, minM)
            except CantSeeWallException as e:
                pass #do nothing, just try the next wall in loop

        return minM

    def getDistanceToWall(self, x, y, theta, Ax, Ay, Bx, By):
        """
        Given a position x, y, theta, calculate the distance to the
        wall defined by endpoints Ax,Ay and Bx,By
        """
        try:
            m = ((By-Ay)*(Ax-x) - (Bx-Ax)*(Ay-y)) / ((By-Ay)*cos(theta) - (Bx-Ax)*sin(theta))
            if m < 0:
                raise CantSeeWallException("Wall is behind robot")
                #
                #    ⦽
                #  ------

            intersectX = x + m*cos(theta)
            intersectY = y + m*sin(theta)

            #----------------------------------
            #veretice wall
            if(Ax == Bx):
                #check intersection
                if(min(Ay, By) <= intersectY <= max(Ay, By)):
                    return m
            #horizontal wall
            if (Ay == By):
                #check intersection
                if (min(Ax, Bx) <= intersectX <= max(Ax, Bx)):
                    return m

            raise CantSeeWallException("Wall does not extend far enough for robot to see")
            #  ---
            #      ⦽
            #  


            #-----------------------------------
            #should this block just be checking that 
            # if( (min(Ay,By) <= intersectY <= max(Ay,By)) and
            # (min(Ax,Bx) <= intersectX <= max(Ax,Bx)) ):
            #   return m
            # else:
            #   raise CantSeeWallException("Wall does not extend far enough for robot to see")
            #
            # then it isnt limited to orthogonal walls
            
        except ZeroDivisionError:
            raise CantSeeWallException("robot is parallel to wall")
            #      |
            #  ⦽  |
            #      |
        
    def get_sensor_reading(self):
        """
        Set sonar reading to objcts infront of sonar sensor\n
        Returns value in range 0-255 cm
        """
        try:
            sensor_readings = []
            for i in range (0,5):
                r = self.BP.get_sensor(self.sonar)
                sensor_readings.append(r + self.sonar_offset)
            
            return median(sensor_readings)

        except brickpi3.SensorError as e:
            print("Sensor Error: ", e)
            return

        except Exception as e:
            print(e)
            return
            
    
        



class NoEnvironmentException(Exception):
    pass

class CantSeeWallException(Exception):
    pass
