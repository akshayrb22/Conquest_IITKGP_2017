"""
the_code.py
A code which will solve a scenario where a resource is kept at a particular angle,
and the bot has to go and fetch it.

THIS CODE COMES WITH ABSOLUTELY NO WARRANTY. DO WHATEVER YOU WANT TO DO WITH IT,
AS LONG AS YOU HAVE GOT BACKUP.
"""

from math import ceil


class Direction(object):
    """
    Constant values for direction of movement.
    """
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    FORWARD_LEFT = 'FORWARD_LEFT'  # 135 deg
    FORWARD_RIGHT = 'FORWARD_RIGHT'  # 45 deg
    BACKWARD_LEFT = 'BACKWARD_LEFT'  # 225 deg
    BACKWARD_RIGHT = 'BACKWARD_RIGHT'  # 315 deg


class Orientation(object):
    CLOCKWISE = 'CLOCKWISE'
    ANTI_CLOCKWISE = 'ANTI_CLOCKWISE'


def get_sector(angle_of_resource):
    """
    Calculate the sector in which resource is lying,
    Assuming that there are 8 sectors in circle, each with 45 degree separation.
    :param angle_of_resource: Angle in degrees where the resource is lying.
    :return: sector(int)
    """

    # To make sure angle_of_resource is within (0, 360)
    angle_of_resource %= 360

    sector = ceil(angle_of_resource / 45.0)

    return sector


def get_orientation(angle_of_resource):
    """
    Calculate angle to turn and where to turn(clockwise or anti-clockwise).
    Returns a tuple of angle in degrees and Turn direction(clock or anti clock)
    :param angle_of_resource:
    :return: (Angle, orientation)
    """

    sector = get_sector(angle_of_resource)

    # Calculate whether to turn clockwise or anti clock wise.

    min_angle_of_sector = (sector - 1) * 45
    max_angle_of_sector = sector * 45

    # print 'min max', min_angle_of_sector, max_angle_of_sector

    mid_angle = (max_angle_of_sector + min_angle_of_sector) / float(2)

    if angle_of_resource < mid_angle:
        orientation = Orientation.ANTI_CLOCKWISE
        degree_to_turn = angle_of_resource - min_angle_of_sector
    else:
        orientation = Orientation.CLOCKWISE
        degree_to_turn = max_angle_of_sector - angle_of_resource

    # print 'orientation', degree_to_turn

    result = (degree_to_turn, orientation)

    return result


def get_direction(angle_of_resource):
    """
    Determine in which direction the bot has to move in order to grab the resource
    :param angle_of_resource: angle at which the resource is located(in degrees)
    :return: tuple(angle, orientation, direction)
    """

    sector = get_sector(angle_of_resource)
    (angle, orientation) = get_orientation(angle_of_resource)

    if sector == 1:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.RIGHT
        else:
            direction = Direction.FORWARD_RIGHT
    elif sector == 2:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.FORWARD_RIGHT
        else:
            direction = Direction.FORWARD
    elif sector == 3:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.FORWARD
        else:
            direction = Direction.FORWARD_LEFT
    elif sector == 4:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.FORWARD_LEFT
        else:
            direction = Direction.LEFT
    elif sector == 5:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.LEFT
        else:
            direction = Direction.BACKWARD_LEFT
    elif sector == 6:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.BACKWARD_LEFT
        else:
            direction = Direction.BACKWARD
    elif sector == 7:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.BACKWARD
        else:
            direction = Direction.BACKWARD_RIGHT
    else:
        if orientation == Orientation.ANTI_CLOCKWISE:
            direction = Direction.BACKWARD_RIGHT
        else:
            direction = Direction.RIGHT

    msg = "Resource is at {resource} degree. Turn the bot by {angle} degree {motion}, and move {direction}"
    msg = msg.format(resource=angle_of_resource, angle=angle, motion=orientation, direction=direction)
    print(msg)

    result = (angle, orientation, direction)
    return result


if __name__ == '__main__':
    print get_direction(45)