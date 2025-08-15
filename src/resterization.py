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
def draw_triangle(A, B, C, colourA, colourB, colourC, draw_context):
    # Calculate the edge function for the entire triangle (ABC).
    # This value represents the total area of the triangle and is used for normalization.
    ABC = edge_function(A, B, C)

    # Our "back-face culling" trick: if the area is negative, the vertices are
    # ordered clockwise. We can skip drawing it, which is an optimization in 3D.
    if ABC < 0:
        print("Warning: Skipping a back-facing triangle.")
        return

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

            # Normalise the edge functions to get the barycentric coordinates (weights).
            # These weights tell us how much each vertex's color contributes to the pixel's color.
            weightA = BCP / ABC
            weightB = CAP / ABC
            weightC = ABP / ABC

            # Check if the point is inside the triangle.
            # If all edge functions are non-negative, the point is inside or on an edge.
            if ABP >= 0 and BCP >= 0 and CAP >= 0:
                # Interpolate the colours at point P using the barycentric coordinates.
                r = colourA.r * weightA + colourB.r * weightB + colourC.r * weightC
                g = colourA.g * weightA + colourB.g * weightB + colourC.g * weightC
                b = colourA.b * weightA + colourB.b * weightB + colourC.b * weightC
                colourP = Colour(r, g, b)

                # Draw the pixel on the canvas using the interpolated color.
                # Pillow's point function expects a tuple for color (r, g, b).
                draw_context.point((P.x, P.y), fill=(colourP.r, colourP.g, colourP.b))

def draw_line(x0, y0, x1, y1, colour, draw_context):
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

def draw_circle_wrong(centre, radius, colour, draw_context):
    """
    Rasterises a circle line with center (x0, y0) radius r
    """
    # x = x0 - rad
    # while (x <= x0 + rad):
    #     y_pos = np.sqrt(rad**2 - (x - x0)**2) + y0
    #     y_neg = -np.sqrt(rad**2 - (x - x0)**2) + y0
    #     angle_pos = np.arctan(y_pos/x)
    #     if(angle_pos<np.pi/3):
    #         r = colourA.r * ((y_neg - y0)**2 + (x - x0)**2)/rad**2
    #     g = 0
    #     b = 0
    #     colourP = Colour(r, g, b)
    #     draw_context.point((x, y_pos), fill=(colourP.r, colourP.g, colourP.b))
    #     draw_context.point((x, y_neg), fill=(colourP.r, colourP.g, colourP.b))
    #     x+=1
    x0 = centre.x
    y0 = centre.y
    x = x0 - radius
    while(x <= x0 + radius):
        y_pos = np.sqrt(radius**2 - (x - x0)**2) + y0
        y_neg = y0 - np.sqrt(radius**2 - (x - x0)**2)

        angle_pos = np.arctan(y_pos/x)
        angle_neg = np.arctan(y_neg/x)
        colourP = Colour(255*angle_pos, 255*(np.pi/2 - angle_pos), 255*(np.pi/2 + angle_pos))
        for y in range (y0, int(y_pos)):
            draw_context.point((x, y), fill=(colourP.r, colourP.g, colourP.b))
        for y in range (int(y_neg), y0):
            draw_context.point((x, y), fill=(colourP.r, colourP.g, colourP.b))
        x+=1

# Main execution block
if __name__ == "__main__":
    # Create our vertex colours
    colourA = Colour(255, 0, 0)  # Red
    colourB = Colour(0, 255, 0)  # Green
    colourC = Colour(0, 0, 255)  # Blue

    # Set up our image canvas
    image_width = 800
    image_height = 600
    # Create a new RGB image with a black background
    image = Image.new("RGB", (image_width, image_height), "black")
    # Get a drawing context for the image
    draw = ImageDraw.Draw(image)

    vertexA1 = Point(222, 100)
    vertexB1 = Point(467, 200)
    vertexC1 = Point(422, 500)
    draw_triangle(vertexA1, vertexB1, vertexC1, colourA, colourB, colourC, draw)

    white = Colour(255, 255, 255)
    #draw_line(0, 0, 60, 200, white, draw)

    draw_circle_wrong(250, 250, 100, draw)

    print("Triangle saved to triangle.png")

    image.show()
