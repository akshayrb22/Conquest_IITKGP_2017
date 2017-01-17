##Assign to Vasu
##Represents all the main points on the graph as resources , townhall, obstaacle
##Functionalities required-
##  contour
##  area
##  angle with respect townhall
##  define a function to locate contour position
##  class point to represent position i.e. x coordinate,y coordinate, point


class Checkpoint(object):
    global area 
    global center_point
    global cX
    global cY
    def __init__(self):
        
    def FindContour(self,image):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh)
        edgess = imutils.resize(edges, width=600)
        # find contours in the thresholded image and initialize the
        # shape detector
        contours = cv2.findContours(edgess.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]
        sd = ShapeDetector()
        return contours
    


