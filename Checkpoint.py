##Assign to Vasu
##Represents all the main points on the graph as resources , townhall, obstaacle
##Functionalities required-
##  contour
##  area
##  angle with respect townhall

from Point import Point
import cv2

class Checkpoint(object):
    def __init__(self,area,position,distance,color,angle,quad):
        self.area = area
        self.center = position
        self.distance = distance #distance from origin to resource
        self.color = color
        self.angle = angle
        self.quad = quad
    def __lt__(self, other):
         return self.distance < other.distance
    #def FindCenter(contour):
    #    Frame.get_center_from_contour(contour)
    #def FindAngle(self):
    #    angle_for_marker(Point(0,0), self.center_point)
    