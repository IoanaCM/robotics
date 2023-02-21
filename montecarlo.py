from math import pi as PI
from math import sin, cos, sqrt
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

        waypoints = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84),  (84, 84), (84, 30)]
        for (Wx, Wy) in waypoints:
            ioInterface.drawCross(Wx,Wy)

        for i in range(len(waypoints)):
            (x,y,theta), (_,_,_) = r.metrics()
            print("I think I am at: " + str(x) + " " + str(y) + " Facing: " + str(theta))

            (Wx,Wy) = waypoints[i]

            dx = Wx - x
            dy = Wy - y
            d = sqrt(dx**2 + dy**2)
            if(d > 20):
                dx = (dx * 20) / d
                dy = (dy * 20) / d
                r.navigateToWaypoint(x + dx, y + dy)
            else: #distance less than 20, navigate in one step
                r.navigateToWaypoint(Wx, Wy)
                i+=1


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    except Exception as e:
        print(e)

    finally:
        r.shutdown()
        return



if __name__ == "__main__":
    main()
