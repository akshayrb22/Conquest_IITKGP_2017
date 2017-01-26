class Config(object):
    
    
    #grid size > devide the arena into given value. Higher the value slower path finding and more resolution (Not required!! )
    gridSize = 25  #CHANGE THIS for new AREANA (3m X 3m) may be 35?

    #path optimizer value
    pathTolerance = 1.3
    # boundry of obtstacle
    obstacleRange = 3 #may be 4? for 3X3 arena

    #max speed 255
    # reduce for 200 RPM Motors!!!!!!
    moveSpeed = 250
    turnSpeed = 240

    # + or - angle for target
    targetAngleRange = 6

    resourcePositionRange = 25  # within 25X25, looks fine for current arena
    
    
    mapRatio = 1.33
    FrameWidth = 800 * mapRatio
    FrameHeight = 800

    #static DO NOT CHANGE !!!
    mappedWidth = gridSize * mapRatio
    mappedHeight = gridSize
    findPathOnce = True
    obstacleCount = 0
    resourceList = None
    obstacleBoundingPointList = []

    