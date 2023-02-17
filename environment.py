import ioInterface

class Environment:
    def __init__(self, walls):
        """
        Walls :: List of 4-tuple [(x0,y0,x1,y1)]
        """
        self.walls = walls


    def show(self):
        for wall in self.walls:
            ioInterface.drawLine(wall)

