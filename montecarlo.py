from math import pi as PI
from math import sin, cos
from numpy import mean, std
import robot
import environment
import ioInterface

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

        walls = [(0,0,0,168),
                 (0,168,84,168),
                 (84,126,84,210),
                 (84,210,168,210),
                 (168,210,168,84),
                 (168,84,210,84),
                 (210,84,210,0),
                 (210,0,0,0)]
        map = environment.Environment(walls)
        r.setEnvironment(map)
        map.show()

        #draw initial particles
        ioInterface.drawParticles(r.particles)
        ioInterface.printMetrics(r.metrics())
        print("closest wall is " + str(r.getDistanceToWallFacing(168, 168, PI)))


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    except Exception as e:
        print(e)

    finally:
        r.shutdown()
        return



if __name__ == "__main__":
    main()
