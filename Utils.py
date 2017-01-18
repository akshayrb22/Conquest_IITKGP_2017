##Open to everyone
##Any person who creates a helper function can place it here
##After adding a function please menrion it in the intital comments
##Contains-
##  Angle for marker()
##  distance formula()

import math
import numpy as np
def angle_for_marker(p1,p2):
    
    opp=float((((p1.x-p1.x)*(p1.x-p1.x))+((p1.y-p2.y)*(p1.y-p2.y)))^(1/2))
    hyp=float((((p1.x-p2.x)*(p1.x-p2.x))+((p1.y-p2.y)*(p1.y-p2.y)))^(1/2))
    sinn=float(opp/hyp)
    angle = math.acos(float(sinn))
    ang=round(math.degrees(angle),2)

    

    '''
    cv2.drawContours(resized, [c2], -1, (0, 255, 0), 2)#cv2.drawContours(source,contours_to_be_passed_as_list,index_of_contours,colour,thickness)
    cv2.circle(resized, (cX2, cY2), 3, (0,0,255), -1)#index_of_contours=>no of contours i guess... -1 means all
    cv2.putText(resized, shape3+'y', (cX2, cY2), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
    cv2.line(resized,(cX,cY),(cX2,cY2),(255,cyan,0),2)#draws line from one point to the other, last arg means thickness
    cyan=cyan-1'''
    return ang

def distance(pt1,pt2):
    
    dist=float((((pt1.x-pt2.x)*(pt1.x-pt2.x))+((pt1.y-pt2.y)*(pt1.y-pt2.y)))^(1/2))
    return dist
    
    
    
