import cv2
from ImageProcess import Frame
from Utils import Utils
from Point import Point

class Draw(object):
    @staticmethod
    def path(simplified):
        i = 0
        
        while(i < (len(simplified) - 1)):
            cv2.arrowedLine(Frame.resized, simplified[i],simplified[i + 1],(0,0,255),1,8,0,0.1)
            #print str(simplified[i]) + " & " +  str(simplified[i + 1])
            i += 1
    @staticmethod
    def line(box,remap = False):
        if remap:
            for point in box:
                point = Utils.remapPoint(Point(point[0],point[1])).get_coordinate()
        cv2.arrowedLine(Frame.resized,box[0],box[1],(255,255,25), 1,0,0,0.1)
        cv2.arrowedLine(Frame.resized,box[2],box[3],(255,255,25), 1,0,0,0.1)
        cv2.arrowedLine(Frame.resized,box[0],box[2],(255,255,25), 1,0,0,0.1)
        cv2.arrowedLine(Frame.resized,box[1],box[3],(255,255,25), 1,0,0,0.1)

if __name__ == "__main__":
    path = []
    path.append((10,10))
    path.append((20,20))
    Draw.path(path)
