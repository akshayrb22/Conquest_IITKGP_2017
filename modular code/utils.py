import math
import numpy as np
def angle_for_marker():
    opp=float((((cX-cX)*(cX-cX))+((cY-cY2)*(cY-cY2)))^(1/2))
    hyp=float((((cX-cX2)*(cX-cX2))+((cY-cY2)*(cY-cY2)))^(1/2))
    sinn=float(opp/hyp)
    angle = math.acos(float(sinn))
    ang=round(math.degrees(angle),2)

    

    
    cv2.drawContours(resized, [c2], -1, (0, 255, 0), 2)#cv2.drawContours(source,contours_to_be_passed_as_list,index_of_contours,colour,thickness)
    cv2.circle(resized, (cX2, cY2), 3, (0,0,255), -1)#index_of_contours=>no of contours i guess... -1 means all
    cv2.putText(resized, shape3+'y', (cX2, cY2), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
    cv2.line(resized,(cX,cY),(cX2,cY2),(255,cyan,0),2)#draws line from one point to the other, last arg means thickness
    cyan=cyan-1
    return ang

def distance(pt1,pt2):
    (x1,y1)=pt1
    (x2,y2)=pt2
    dist=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
    return dist
    
    
    
