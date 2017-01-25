class Config(object):
    mapRatio = 1.33
    mappedWidth = 30 * mapRatio
    mappedHeight = 30
    pathTolerance = 1.3
    FrameWidth = 800 * mapRatio
    FrameHeight = 800
    obstacleRange = 4
    moveSpeed = 50
    turnSpeed = 30
    targetAngelRange = 6
    resourcePositionRange = 25

    #static DO NOT CHANGE !!!
    findPathOnce = True
    obstacleCount = 0
    resourceList = None
    obstacleBoundingPointList = []