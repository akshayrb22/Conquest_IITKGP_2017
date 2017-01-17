import numpy as np
class Color():
    
    def __init__(self,color="red", type=1):
        colorFile = open(color + ".txt","r")
        colorData = colorFile.read()
        colorFile.close()
        colorList = colorData.split(',')
        if type == 1:
            self.H = colorList[0]
            self.S = colorList[1]
            self.V = colorList[2]
        if type == 0:
            self.H = colorList[3]
            self.S = colorList[4]
            self.V = colorList[5]


    def toString(self):
        return str(self.H)  + "," + str(self.S)  + "," + str(self.V)
    
    def get_array(self):
        return np.array([int(self.H), int(self.S), int(self.V)])

