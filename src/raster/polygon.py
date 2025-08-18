from ..helper import Colour, Point
from .line import draw_line_bresenham

def draw_polygon(vertices, colour, draw_context):
    # Draw the edges of the polygon
    num_vertices = len(vertices)
    for i in range(num_vertices):
        A = vertices[i]
        B = vertices[(i + 1) % num_vertices]  # Wrap around to the first vertex
        draw_line_bresenham(A.x, A.y, B.x, B.y, colour, draw_context)