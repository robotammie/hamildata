from math import radians, cos, sin

num_points = 46


def find_points(circ, num_points):
    """
    Find coordinates of a given number of points arrayed equidistantly
    along the circumference of a circle
    """
    cx, cy, r = circ
    angle = (360 / num_points)
    for i in range(num_points):
        x = cx + (r * cos(radians(angle * i)))
        y = cy + (r * sin(radians(angle * i)))
        print "(%d, %d)" % (x, y)
