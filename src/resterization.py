# Import the Image and ImageDraw modules from the Pillow library
# Pillow is a powerful image processing library for Python.
from PIL import Image, ImageDraw
import numpy as np
# Define our Colour class to hold RGB values.
# This makes it easy to pass color information around.
class Colour:
    def __init__(self, r, g, b):
        self.r = int(r)  # Ensure values are integers for the image library
        self.g = int(g)
        self.b = int(b)

# Define our Point class to hold 2D coordinates.
# This is a simple data structure to represent points on our canvas.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# The edge function calculates the signed area of a triangle formed by three points.
# The sign of the result tells us which side of the line segment AB point C lies on.
def edge_function(A, B, C):
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)

# This is the main function to draw and rasterize the triangle.
# It takes the three vertices and a Pillow ImageDraw object as input.
def draw_triangle(A, B, C, colour, draw_context):
    ABC = edge_function(A, B, C)

    # Check if the triangle is clockwise or counter-clockwise
    is_clockwise = ABC < 0

    # Get the bounding box of the triangle to reduce the number of pixels to check.
    minX = min(A.x, B.x, C.x)
    minY = min(A.y, B.y, C.y)
    maxX = max(A.x, B.x, C.x)
    maxY = max(A.y, B.y, C.y)

    # Loop through every pixel within the bounding box.
    P = Point(0, 0)
    for P.y in range(int(minY), int(maxY)):
        for P.x in range(int(minX), int(maxX)):
            # Calculate the edge functions for the point P with respect to each edge.
            # These values are proportional to the area of the sub-triangles (ABP, BCP, CAP).
            ABP = edge_function(A, B, P)
            BCP = edge_function(B, C, P)
            CAP = edge_function(C, A, P)

            # Check if the point is inside the triangle.
            if is_clockwise:
                if ABP <= 0 and BCP <= 0 and CAP <= 0:
                    draw_context.point((P.x, P.y), fill=(colour.r, colour.g, colour.b))
            else:
                if ABP >= 0 and BCP >= 0 and CAP >= 0:
                    draw_context.point((P.x, P.y), fill=(colour.r, colour.g, colour.b))


def draw_line_float_long(x0, y0, x1, y1, colour, draw_context):
    """
    Rasterises a straight line between (x0, y0) and (x1, y1)
    """
    dx = x1 - x0
    dy = -(y1 - y0)
    x = x0
    y = y0
    print(dx, dy)

    if((dx>=0) and (dy>=0)):
        while(x <= x1 and y >= y1):
            x = x + np.sign(dx)*1
            y = y - dy/dx
            draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))
    elif ((dx<=0) and (dy>=0)):
        while(x >= x1 and y >= y1):
            x = x + np.sign(dx)*1
            y = y + dy/dx
            draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))
    elif ((dx<=0) and (dy<=0)):
        while(x >= x1 and y <= y1):
            x = x + np.sign(dx)*1
            y = y + dy/dx
            draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))
    elif ((dx>=0) and (dy<=0)):
        while(x <= x1 and y <= y1):
            x = x + np.sign(dx)*1
            y = y - dy/dx
            draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))


def draw_line_float_simple(x0, y0, x1, y1, colour, draw_context):
    dx = x1 - x0
    dy = y1 - y0

    steps = int(max(abs(dx), abs(dy)))

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x0, y0
    for _ in range(steps + 1):
        draw_context.point((round(x), round(y)), fill=(colour.r, colour.g, colour.b))
        x += x_inc
        y += y_inc 


def draw_line_int(x0, y0, x1, y1, colour, draw_context):
    """
    Rasterises a straight line between (x0, y0) and (x1, y1)
    using Bresenham's algorithm.
    """
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy  # error term

    while True:
        draw_context.point((x0, y0), fill=(colour.r, colour.g, colour.b))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

def draw_circle_float(centre, radius, colour, draw_context, fill=False):
    """
    Rasterises a circle line with center (x0, y0) radius r
    """
    x0 = centre.x
    y0 = centre.y
    x = x0 - radius
    while (x <= x0 + radius):
        y_pos = np.sqrt(radius**2 - (x - x0)**2) + y0
        y_neg = y0 - np.sqrt(radius**2 - (x - x0)**2)
        draw_context.point((x, y_pos), fill=(colour.r, colour.g, colour.b))
        draw_context.point((x, y_neg), fill=(colour.r, colour.g, colour.b))
        x+=1

    if(fill):
        x = x0 - radius
        while(x <= x0 + radius):
            y_pos = np.sqrt(radius**2 - (x - x0)**2) + y0
            y_neg = y0 - np.sqrt(radius**2 - (x - x0)**2)

            angle_pos = np.arctan(y_pos/x)
            #colourP = Colour(255*angle_pos, 255*(np.pi/2 - angle_pos), 255*(np.pi/2 + angle_pos))
            for y in range (int(y0), int(y_pos)):
                draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))
            for y in range (int(y_neg), int(y0)):
                draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))
            x+=1



def draw_circle_int(centre, radius, colour, draw_context, fill=False):
    xc = centre.x
    yc = centre.y
    x, y = 0, radius
    p = 1 - radius
    while x <= y:
        # 8 symmetric points
        points = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x),
        ]
        for px, py in points:
            draw_context.point((px, py), fill=(colour.r, colour.g, colour.b))

        if p < 0:
            p += 2*x + 3
        else:
            p += 2*(x - y) + 5
            y -= 1
        x += 1

    if fill:
        for y_fill in range(int(yc - radius), int(yc + radius) + 1):
            for x_fill in range(int(xc - radius), int(xc + radius) + 1):
                if (x_fill - xc)**2 + (y_fill - yc)**2 <= radius**2:
                    draw_context.point((x_fill, y_fill), fill=(colour.r, colour.g, colour.b))