from ..helper import Colour, Point
from .line import draw_line_bresenham
# The edge function calculates the signed area of a triangle formed by three points.
# The sign of the result tells us which side of the line segment AB point C lies on.
def edge_function(A, B, C):
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)

# This is the main function to draw and rasterize the triangle.
# It takes the three vertices and a Pillow ImageDraw object as input.
def fill_triangle(A, B, C, colour, draw_context):
    ABC = edge_function(A, B, C)

    # Check if the triangle is clockwise or counter-clockwise
    is_clockwise = ABC < 0

    # Get the bounding box of the triangle to reduce the number of pixels to check.
    minX = min(A.x, B.x, C.x)
    minY = min(A.y, B.y, C.y)
    maxX = max(A.x, B.x, C.x)
    maxY = max(A.y, B.y, C.y)

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

def draw_triangle(A, B, C, colour, draw_context, fill=False):
    # Just draw the 3 edges of the triangle
    draw_line_bresenham(A.x, A.y, B.x, B.y, colour, draw_context)
    draw_line_bresenham(B.x, B.y, C.x, C.y, colour, draw_context)
    draw_line_bresenham(C.x, C.y, A.x, A.y, colour, draw_context)