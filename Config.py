class Config(object):
    mapRatio = 1.33
    mappedWidth = 25 * mapRatio
    mappedHeight = 25
    pathTolerance = 1.3
    FrameWidth = 800 * mapRatio
    FrameHeight = 800
    obstacleRange = 3
    moveSpeed = 250
    turnSpeed = 240
    targetAngelRange = 6
    resourcePositionRange = 25

    #static DO NOT CHANGE !!!
    findPathOnce = True
    obstacleCount = 0
    resourceList = None
    obstacleBoundingPointList = []