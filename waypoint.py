from math import pi as PI
from math import sin, cos
from numpy import mean, std
import robot
import time
import random

def main():
    r = robot.robot()
    r.setup()

    try:
        
        while True:
            (x,y,theta), (_,_,_) = r.metrics()
            print("I think I am at: " + str(x) + " " + str(y) + " Facing: " + str(theta))
            x = float(input("Enter x: "))
            y = float(input("Enter y: "))
            r.navigateToWaypoint(x, y)


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    except Exception as e:
        print(e)

    finally:
        r.shutdown()
        return

if __name__ == "__main__":
    main()