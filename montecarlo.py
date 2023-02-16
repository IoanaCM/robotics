from math import pi as PI
from math import sin, cos
from numpy import mean, std
import robot
import time

#global variables
pause = 1               # pause delay in seconds
clear_particles = True  # clear particles before drawing next set
draw_arrows = False     # draw arrows on particles to show theta
                        #  Unfortunately lines dont clear so recommend
                        #  draw_arrows True only if clear_particles is False

def main():
    r = robot.robot()
    r.setup()

    try:

        #draw ideal square
        drawLine((0,0,0,168))
        drawLine((0,168,84,168))
        drawLine((84,126,84,210))
        drawLine((84,210,168,210))
        drawLine((168,210,168,84))
        drawLine((168,84,210,84))
        drawLine((210,84,210,0))
        drawLine((210,0,0,0))

        #draw initial particles
        drawParticles(r.particles)
        printMetrics(r.metrics())


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
    map_size = 210
    margin = 10
    scale = 3

    x0,y0,x1,y1 = line
    #transform from robot coordinates to screen coordinates
    tx0 = (x0 + margin) * scale
    ty0 = (-y0 + margin + map_size) * scale
    tx1 = (x1 + margin) * scale
    ty1 = (-y1 + margin + map_size) * scale
    graphic = (tx0,ty0,tx1,ty1)
    print("drawLine:" + str(graphic))
    return


def transformPoint(point):
    """
    converts point from robot coordinates to screen coordinates
    point :: tuple ((x,y,theta),weight)
    """
    map_size = 210
    margin = 10
    scale = 3

    ((x,y,theta), _) = point

    return ((x + margin) * scale, (-y + margin + map_size) * scale, theta)

def drawParticles(particles):
    """
    Wrapper for web interface\n
    particles :: list of tuples [((x,y,theta),weight)]
    """

    #transform from robot coordinates to screen coordinates
    transformed_particles = list(map(transformPoint, particles))
    print("drawParticles:" + str(transformed_particles))

    if draw_arrows:
      for p in particles:
        ((x,y,theta),_) = p
        drawLine((x, y, x + 3*cos(theta), y + 3*sin(theta)))

    return


if __name__ == "__main__":
    #random.seed(17) # seed RNG for reproduceable results
    main()
