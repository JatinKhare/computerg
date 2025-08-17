from ..helper import Colour, Point
import numpy as np

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
        draw_context.point((x, y_pos))
        draw_context.point((x, y_neg))
        x+=1
    
    if(fill):
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
