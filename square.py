##!/usr/bin/env python
#
#
# Hardware:
#
# Results:

#uncomment these if they were actually needed, else im deleting them
#from __future__ import print_function # use python 3 syntax but make it compatible with python 2
#from __future__ import division


from math import pi as PI
import robot


def main():
    r = robot.robot()
    r.setup()

    try:
        for i in range(0,4):
            r.forward(40)
            r.spinL(90)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("Quitting early")

    finally:
        r.shutdown()
        return



if __name__ == "__main__":
    main()
