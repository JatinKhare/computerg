from src.raster.line import draw_line_bresenham
from ..helper import Colour, Point
from src.canvas import Canvas

import numpy as np


def scanline_fill_custom(polygon, color, draw_context):
    """
    Fills a polygon using the scanline fill algorithm. 
    """
    num_vertices = len(polygon)
    for i in range(num_vertices):
        polygon[i] = (int(polygon[i].x), int(polygon[i].y))
    ymin = min(y for _, y in polygon)
    ymax = max(y for _, y in polygon)
    print(ymin, ymax)
    # For each scanline
    for y in range(ymin, ymax+1):
        intersections = []
        for i in range(len(polygon)):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i+1) % len(polygon)]

            # check if edge crosses scanline
            if y1 <= y < y2 or y2 <= y < y1:
                # compute x intersection
                x = int(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
                intersections.append(x)

        intersections.sort()
        # fill pairs
        for i in range(0, len(intersections), 2):
            x_start = intersections[i]
            x_end = intersections[i+1]
            if(y==300):
                print(x_start, x_end)
            draw_line_bresenham(x_start, y, x_end, y, color, draw_context)