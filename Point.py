##This is a file to define a class point which will return the coordinate
##It can also return the x & y coordinates separately

class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def get_coordinate(self):
        return (self.x, self.y)
    def toString(self):
        return "(" + str(self.x + "," + str(self.y + ")"))

    
