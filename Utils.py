##Open to everyone
##Any person who creates a helper function can place it here
##After adding a function please menrion it in the intital comments
##Contains-
##  Angle for marker()
##  distance formula()

from math import *
import numpy as np
from Point import Point
class Utils(object):

    @staticmethod
    def angleBetweenPoints(origin,position):
        deltaY = position.y - origin.y
        deltaX = position.x - origin.x
        angleInDegrees = atan2(deltaY, deltaX) * float(180) / 3.14
        
        angleInDegrees =  round((angleInDegrees + 360 ) % 360)
        return angleInDegrees,None

    @staticmethod
    def distance(pt1,pt2):
        dist = float((((pt1.x-pt2.x)*(pt1.x-pt2.x))+((pt1.y-pt2.y)*(pt1.y-pt2.y)))^(1/2))
        return dist
    @staticmethod
    def map(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    
    
if __name__ == '__main__':
    angle,_  = Utils.angleBetweenPoints(Point(0,0),Point(10, 10))
    print angle




'''
    @staticmethod
    def angleBetweenPoints(origin,position):
        # adj=float((((p1.x-p2.x)*(p1.x-p2.x))+((p1.y-p1.y)*(p1.y-p1.y)))^(1/2))
        # print adj
        # hyp=float((((p1.x-p2.x)*(p1.x-p2.x))+((p1.y-p2.y)*(p1.y-p2.y)))^(1/2))
        # print hyp
        # cos=float(adj/hyp)
        # print cos
        # angle = math.acos(float(cos))
        # ang=round(math.degrees(angle),2)
        dist2 = math.sqrt(float(abs((origin.y - position.y )*(origin.y - position.y ))))
        dist = math.sqrt(float(abs(((origin.x - position.x)*(origin.x - position.x))+((origin.y - position.y )*(origin.x - position.y)))))
        sinn = float(dist2/dist)
        
        if sinn > 1:
            sinn = 1
        if sinn < 0:
            sinn = 0        angle = math.asin(float(sinn))
        angle = round(math.degrees(angle), 2)
        if position.x > origin.x and position.y > origin.y:
            angle = 270 + angle
        elif position.x < origin.x and position.y > origin.y:
            angle = 270 - angle
        elif position.x < origin.x and position.y < origin.y:
            angle = angle + 90
        elif origin.x < position.x and origin.y > position.y:
            angle = 90 - angle
        return angle,dist
'''