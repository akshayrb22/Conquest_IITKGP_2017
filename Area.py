class Area(object):
    def __init__(self,color):
        print 'Reading Area from file: '  + str(color)
        colorFile = open( color + ".txt","r")
        colorData = colorFile.read()
        colorFile.close()
        colorList = colorData.split(',')
        self.min = colorList[7]
        self.max = colorList[8]

if __name__ == '__main__':
    testArea = Area('red')
    print testArea.max
