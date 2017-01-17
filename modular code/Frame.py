import numpy as np
import cv2
import PIL
from PIL import Image
import imutils

class Frame:
    global image,ratio,resized
    def __init__(self):
        self.elements=[]
    
        
        
        
    
    def cap_frame(self):
        baseheight = 570
        img = Image.open('as.jpg')
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        img.save('asia.jpg')
        self.image = cv2.imread('asia.jpg',1)
    def vid_cap(self):
        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)

    def find_ratio(self):
        self.resized = imutils.resize(self.image, width=600)
        self.ratio = self.image.shape[0] / float(self.resized.shape[0])
        return self.image,self.resized,self.ratio


                                       

