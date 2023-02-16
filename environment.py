import ioInterface

class Environment:
    def __init__(self, walls=[]):
        """
        Walls :: List of 4-tuple [(x0,y0,x1,y1)]
        """
        self.walls = walls


    def show(self):
        for wall in self.walls:
            ioInterface.drawLine(wall)



    #def inside(x, y):
    #    if ((x < 0) or (y < 0)):
    #        return False
    #    
    #    ...
    #    return True

class Wall:
    def __init__(self, line):
        (x0,y0,x1,y1) = line
        self.Ax = x0
        self.Ay = y0
        self.Bx = x1
        self.By = y1

    #def intersect(self, point):
    #    (x,y) = point
    #    m = (self.Ay - self.By) / (self.Ax - self.Bx)
        