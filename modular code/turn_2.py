def go_to_direction(current_angle,target_ang):

##    ang_2 = target_ang % 45
##    changed_ang = 0
##    
##    if(ang_2 >= 23 ):
##        orientation = "aclock"
##        changed_ang = 23 - target_ang % 23
##    else:
##        orientation = "clock"
##        changed_ang = target_ang % 23
##
##    turn_angle = changed_ang + target_ang
##
##    print turn_angle
##    direction = ""
##    if turn_angle in range(0,7) or turn_angle in range(355,360):
##        direction = "f"
##    elif turn_angle in range(40,50):
##        direction = "fr"
##    elif turn_angle in range(85,95):
##        direction = "r"
##    elif turn_angle in range(130,140):
##        direction = "br"
##    elif turn_angle in range(175,185):
##        direction = "b"
##    elif turn_angle in range(220,230):
##        direction = "bl"
##    elif turn_angle in range(265,275):
##        direction = "l"
##    elif turn_angle in range(310,320):
##        direction = "fl"
    
        
    


    
    if target_ang in range(0,23) or target_ang in range(45,68) or target_ang in range(90,103) or target_ang in range(135,158) or target_ang in range(180,203) or target_ang in range(225,248) or target_ang in range (270,293) or target_ang in range(315,338):
        orientation="clock"
        
        
        if target_ang in range (0,23):
            direction="f"
        elif target_ang in range (45,68):
            direction="fr"
        elif target_ang in range (90,113):
            direction="r"
        elif target_ang in range (135,158):
            direction="br"
        elif target_ang in range (180,203):
            direction="b"
        elif target_ang in range (225,248):
            direction="bl"
        elif target_ang in range (270,293):
            direction="l"
        elif target_ang in range (315,338):
            direction="fl"
                
            
        

    else:
        orientation="aclock"
        
        
        if target_ang in range (23,45):
            direction="fr"
        elif target_ang in range (68,90):
            direction="r"
        elif target_ang in range (113,135):
            direction="br"
        elif target_ang in range (158,180):
            direction="b"
        elif target_ang in range (203,225):
            direction="bl"
        elif target_ang in range (248,270):
            direction="l"
        elif target_ang in range (293,315):
            direction="fl"
        elif target_ang in range (338,360):
            direction="f"

    print(orientation,direction)
    return(orientation,direction)


find_angle(0,20)

            
    
    
    
    

    
    
    
    
    
    
