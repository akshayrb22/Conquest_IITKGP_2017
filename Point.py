##This is a file to define a class point which will return the coordinate
##It can also return the x & y coordinates separately
from Config import Config


class Point(object):
    value = 40
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def get_coordinate(self):
        return (self.x, self.y)
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    def __lt__(self, other):
        if self.x <= other.x:
            return True
        return False
    @staticmethod
    def inRange(point1,point2):
        if point1.x in range(point2.x - Config.resourcePositionRange ,point2.x + Config.resourcePositionRange) and point1.y in range(point2.y - Config.resourcePositionRange ,point2.y + Config.resourcePositionRange) :
            return True
        else:
            return False
if __name__ == '__main__':
    p1 = Point(0,0)
    p2 = Point(10,10)
    print p2.get_coordinate()
