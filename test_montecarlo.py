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
            for i in range(10):
                ((x, y, theta), _) = r.particles[i]
                print(r.calculate_likelihood(x, y, theta, r.get_sensor_reading()))
                print('\n')


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    except Exception as e:
        print(e)

    finally:
        r.shutdown()
        return

if __name__ == "__main__":
    main()