class Config(object):
    
    
    #grid size > devide the arena into given value. Higher the value slower path finding and more resolution (Not required!! )
    gridSize = 35 #CHANGE THIS for new AREANA (3m X 3m) may be 35?

    #path optimizer value
    pathTolerance = 1.3
    # boundry of obtstacle
    obstacleRange =  4 #may be 4? for 3X3 arena | Reduce this if you get came_from[target] error!

    #max speed 255
    # reduce for 200 RPM Motors!!!!!!
    moveSpeed = 250
    moveSpeedNear = moveSpeed - 70 #When bot is closer to the target
    turnSpeed = 240

    reduceSpeedAt = 150
    # + or - angle for target
    targetAngleRange = 8

    goToResourceTwice = False   #if True Bot will go to resource twice

    resourcePositionRange = 25  # within 25X25, looks fine for current arena
    
    
    mapRatio = 1.33
    FrameWidth = 800 * mapRatio
    FrameHeight = 800

    #static DO NOT CHANGE !!!
    mappedWidth = gridSize * mapRatio
    mappedHeight = gridSize
    findPathOnce = True
    obstacleCount = 0
    obstacleList = None
    resourceList = None
    obstacleBoundingPointList = []
    startTime = None
    endTime = None

    