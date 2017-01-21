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
        angleInDegrees = round(atan2(deltaY, deltaX) * float(180) / 3.14)
        if angleInDegrees < 0: 
            #angle is in I and II Quad, ie between 0 to -180, so map it to 0,180
            angleInDegrees = Utils.map(angleInDegrees,0,-180,0,180)
        else:
            #angle is in III and IV Quad, ie between 0 to -180, so map it to 360,180
            angleInDegrees = Utils.map(angleInDegrees,0,180,360,180)
        return angleInDegrees, Utils.distance(origin, position)

    @staticmethod
    def distance(pt1,pt2):
        dist = sqrt(((pt1.x-pt2.x)*(pt1.x-pt2.x))+((pt1.y-pt2.y)*(pt1.y-pt2.y)))
        return dist
    @staticmethod
    def map(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    @staticmethod
    def midPoint(point1,point2):
        return Point((point1.x + point2.x)/2,(point1.y + point2.y)/2)
    
    
if __name__ == '__main__':
    angle, dist= Utils.angleBetweenPoints(Point(0,0),Point(5,0))
    print angle,dist
    angle, dist = Utils.angleBetweenPoints(Point(200,200),Point(190,190))
    print angle, dist
    angle, dist = Utils.angleBetweenPoints(Point(200,200),Point(190,210))
    print angle, dist
    angle, dist =  Utils.angleBetweenPoints(Point(200,200),Point(210,210))
    print angle, dist
        
    
    
    
    
    
    
    
    
    
    # angle,_  = Utils.angleBetweenPoints(Point(388,333),Point(301,476))
    # #angle = Utils.map(-170,-180,0,180,360)
    # print angle
    # angle,_  = Utils.angleBetweenPoints(Point(388,333),Point(240,233))
    # #angle = Utils.map(-170,-180,0,180,360)
    # print angle
    # angle,_  = Utils.angleBetweenPoints(Point(388,333),Point(496,195))
    # #angle = Utils.map(-170,-180,0,180,360)
    # print angle
    # angle,_  = Utils.angleBetweenPoints(Point(200,200),Point(190,210))
    # #angle = Utils.map(-170,-180,0,180,360)



 

    




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