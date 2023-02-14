from math import pi as PI
from math import sin, cos
from numpy import mean, std
import robot
import time

#global variables
pause = 1             # pause delay in seconds
num_particles = 100   # number of particle predictions
sigma_e = 0.01   # standard deviation in cm      - error of driving too far/short during forward movement
sigma_f = 0.006  # standard deviation in radians - error of turning during forward motion
sigma_g = 0.006  # standard deviation in radians - error of turning too far/short during spin

def main():
    r = robot.robot()
    r.setup()

    try:

        #draw ideal square
        drawLine((0,0,40,0))
        drawLine((40,0,40,40))
        drawLine((40,40,0,40))
        drawLine((0,40,0,0))
        #draw initial particles
        drawParticles(r.particles)
        printMetrics(r.metrics())

        for i in range(0,4):
            for j in range(0,4):

                # move robot forward
                r.forward(10)
                drawParticles(r.particles)
                printMetrics(r.metrics())
                time.sleep(pause)

            # spin robot
            r.spinL(90)
            drawParticles(r.particles)
            printMetrics(r.metrics())
            time.sleep(pause)

        


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    except Exception as e:
        print(e)

    finally:
        r.shutdown()
        return

    
def printMetrics(metrics):
    ((mu_x,mu_y,mu_theta),(sigma_x,sigma_y,sigma_theta)) = metrics
    mx = "{:.3f}".format(mu_x)
    my = "{:.3f}".format(mu_y)
    mt = "{:.3f}".format(mu_theta)
    sx = "{:.3f}".format(sigma_x)
    sy = "{:.3f}".format(sigma_y)
    st = "{:.3f}".format(sigma_theta)
    print(f"Mean position: (x={mx}, y={my}, theta={mt}), Standard Deviation: (x={sx}, y={sy}, theta={st})")


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
    point :: tuple ((x,y,theta),weight)
    """
    ((x,y,theta), _) = point

    return (10 * x + 100, -y * 10 + 500, theta)

def drawParticles(particles):
    """
    Wrapper for web interface\n
    particles :: list of tuples [((x,y,theta),weight)]
    """

    #transform from robot coordinates to screen coordinates
    transformed_particles = list(map(transformPoint, particles))
    print("drawParticles:" + str(transformed_particles))
    return


if __name__ == "__main__":
    #random.seed(17) # seed RNG for reproduceable results
    main()
