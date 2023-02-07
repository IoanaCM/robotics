##!/usr/bin/env python
#
#
# Hardware:
#
# Results:


from math import pi as PI
import robot
import time


pause = 1 # pause delay in seconds

def main():
    r = robot.robot()
    r.setup()

    try:
        for i in range(0,4):
            for j in range(0,4):
                r.forward(10)
                time.sleep(pause)

            r.spinL(90)
            time.sleep(pause)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    finally:
        r.shutdown()
        return



def drawLine(x0,y0,x1,y1):
  """
  Wrapper for web interface\n
  x0,y0,x1,y1 : robot coordinates
  """

  #transform from robot coordinates to screen coordinates
  line = (x0+10, -y0 + 50, x1+10, -y0+50)
  print("drawLine:" + str(line))

def drawparticles(particles):
  """
  Wrapper for web interface\n
  particles :: list of 3-tuples [(x,y,theta)]
  """
  print("drawParticles:" + str(particles))



if __name__ == "__main__":
    main()
