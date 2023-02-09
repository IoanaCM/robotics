from math import pi as PI
from math import sin, cos
from numpy import mean, std
import robot
import time
import random

#global variables
pause = 1             # pause delay in seconds
num_particles = 100   # number of particle predictions
sigma_e = 0.1   # standard deviation in cm      - error of driving too far/short
sigma_f = 0.01  # standard deviation in radians - error of turning during forward motion
sigma_g = 0.01  # standard deviation in radians - error of turning too far/short

def main():
    r = robot.robot()
    r.setup()

    try:
        # initialise particles array
        particles = [(0,0,0)] * num_particles

        #draw ideal square
        drawLine((0,0,40,0))
        drawLine((40,0,40,40))
        drawLine((40,40,0,40))
        drawLine((0,40,0,0))
        #draw initial particles
        drawParticles(particles)
        printMetrics(particles)

        for i in range(0,4):
            for j in range(0,4):

                # move robot forward
                r.forward(10)
                
                # update particle predictions for forward movement
                particles = list(map(updateParticleForward, particles))
                drawParticles(particles)
                printMetrics(particles)

                time.sleep(pause)

            # spin robot
            r.spinL(90)

            #update particle predictions for spin
            particles = list(map(updateParticleSpin, particles))
            drawParticles(particles)
            printMetrics(particles)

            time.sleep(pause)

        


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    except Exception as e:
        print(e)

    finally:
        r.shutdown()
        return


def updateParticleForward(particle):
    """
    Update particle prediction for forward movement of 10cm
    particle :: 3-tuple (x,y,theta)
    """
    x,y,theta = particle

    e = random.gauss(0,sigma_e)
    f = random.gauss(0,sigma_f)
    return (x + (10 + e) * cos(theta), y + (10 + e) * sin(theta), theta + f)

def updateParticleSpin(particle):
    """
    Update particle prediction for left spin PI/2 radians
    particle :: 3-tuple (x,y,theta)
    """
    x,y,theta = particle

    g = random.gauss(0,sigma_g)
    return (x, y, (theta + PI/2 + g) % (2*PI))
    
def printMetrics(particles):
    (mu_x,mu_y),(sigma_x,sigma_y) = metrics(particles)
    mx = "{:.3f}".format(mu_x)
    my = "{:.3f}".format(mu_y)
    sx = "{:.3f}".format(sigma_x)
    sy = "{:.3f}".format(sigma_y)
    print(f"Mean position: ({mx},{my}), Standard Deviation: ({sx},{sy})")

def metrics(particles):
    """
    Reports mean and standard deviation of particles position array
    particles :: list of 3-tuple [(x,y,theta)]
    Return ((mu_X, mu_y), (sigma_x, sigma_y))
    """

    xs = list(map(fst, particles))
    ys = list(map(snd, particles))
    return ((mean(xs), mean(ys)),(std(xs), std(ys)))

def drawLine(line):
    """
    Wrapper for web interface\n
    line :: 4-tuple (x0,y0,x1,y1) - robot coordinates of line
    """
    x0,y0,x1,y1 = line
    #transform from robot coordinates to screen coordinates
    tx0 =  x0 * 10 + 100
    ty0 = -y0 * 10 + 500
    tx1 =  x1 * 10 + 100
    ty1 = -y1 * 10 + 500
    graphic = (tx0,ty0,tx1,ty1)
    print("drawLine:" + str(graphic))
    return


def transformPoint(point):
    """
    converts point from robot coordinates to screen coordinates
    point :: 3-tuple (x,y,theta)
    """
    x,y,theta = point

    return (10 * x + 100, -y * 10 + 500, theta)

def drawParticles(particles):
    """
    Wrapper for web interface\n
    particles :: list of 3-tuples [(x,y,theta)]
    """

    #transform from robot coordinates to screen coordinates
    transformed_particles = list(map(transformPoint, particles))
    print("drawParticles:" + str(transformed_particles))
    return

def fst(particle):
    x,y,theta = particle
    return x

def snd(particle):
    x,y,theta = particle
    return y


if __name__ == "__main__":
    #random.seed(17) # seed RNG for reproduceable results
    main()
