##Assign to Vasu
##Represents all the main points on the graph as resources , townhall, obstaacle
##Functionalities required-
##  contour
##  area
##  angle with respect townhall

from Point import Point
from HSV import Color
from Area import Area
import cv2


class Checkpoint(object):
    
    def __init__(self,area,position,distance,color,angle):
        self.area = area
        self.center = position
        self.distance = distance #distance from origin to resource
        self.color = color
        self.angle = angle
        
    def __lt__(self, other):
         return self.distance < other.distance

class CheckpointType(object):
    def __init__(self,checkpoint_type,color,contour_color):
        self.contour_color = contour_color
        self.area = Area(color)
        self.upper_color = Color.Color(color, 1)
        self.lower_color = Color.Color(color, 0)
        self.type = checkpoint_type


