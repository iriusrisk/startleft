from math import sqrt


def get_long(x1, y1, x2, y2):
    """
    Return the distance between two points
    """
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_limit(x1, y1, x2, y2, limit_min, limit_max):
    """
    Given two points, return the last point of the line inside one limit (x or y)
    """
    # The limit can be at left(MIN) or right(MAX)
    limit_x = limit_max if x1 < x2 else limit_min
    # The limit can be at bottom(MIN) or top(MAX)
    limit_y = limit_max if y1 < y2 else limit_min

    # Horizontal line
    if x1 == x2:
        return x1, limit_max
    # Vertical line
    if y1 == y2:
        return limit_max, y1

    # equation of the line: (x-x1)/(x2-x1)=(y-y1)/(y2-y1)
    # We get the y position on x limit
    x3, y3 = limit_x, y1 + ((limit_x - x1) * (y2 - y1) / (x2 - x1))

    # We get the x position on y limit
    x4, y4 = x1 + ((limit_y - y1) * (x2 - x1) / (y2 - y1)), limit_y

    # We return the longer
    long3 = get_long(x1, y1, x3, y3)
    long4 = get_long(x1, y1, x4, y4)
    return (x3, y3) if long3 > long4 else (x4, y4)
