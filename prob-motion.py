from math import pi as PI
import robot
import time

#global variables
pause = 1 # pause delay in seconds
num_Particles = 100


def main():
    r = robot.robot()
    r.setup()

    try:

        drawLine(0,0,40,0)
        drawLine(40,0,40,40)
        drawLine(40,40,0,40)
        drawLine(0,40,0,0)

        drawParticles([(r.x,r.y,r.theta)])

        for i in range(0,4):
            for j in range(0,4):

                r.forward(10)
                time.sleep(pause)

                drawParticles([(r.x,r.y,r.theta)])

            r.spinL(90)
            time.sleep(pause)

            drawParticles([(r.x,r.y,r.theta)])


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")


    except Exception as e:
        print(e)

    finally:
        print("finally")
        r.shutdown()
        return



def drawLine(x0,y0,x1,y1):
    """
    Wrapper for web interface\n
    x0,y0,x1,y1 : robot coordinates
    """

    #transform from robot coordinates to screen coordinates
    tx0 =  x0 * 10 + 100
    ty0 = -y0 * 10 + 500
    tx1 =  x1 * 10 + 100
    ty1 = -y1 * 10 + 500
    line = (tx0,ty0,tx1,ty1)
    print("drawLine:" + str(line))
    return


def transformPoint(point):
    """
    converts point from robot coordinates to screen coordinates
    point :: 3-tuple (x,y,theta)
    """
    x = point[0]
    y = point[1]
    theta = point[2]

    return (10 * x + 100, -y * 10 + 500, theta * PI/180)

def drawParticles(particles):
    """
    Wrapper for web interface\n
    particles :: list of 3-tuples [(x,y,theta)]
    """

    #transform from robot coordinates to screen coordinates
    transformed_particles = list(map(transformPoint, particles))
    print("drawParticles:" + str(transformed_particles))
    return


if __name__ == "__main__":
    main()
