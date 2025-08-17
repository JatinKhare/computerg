from ..helper import Colour, Point

def draw_line_wrong(x0, y0, x1, y1, colour, draw_context):
    """
    Rasterises a straight line between (x0, y0) and (x1, y1)
    """
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    while(x <= x1 and y <= y1):
        x = x + 1
        y = y + dy/dx
        draw_context.point((x, y), fill=(colour.r, colour.g, colour.b))

def draw_line_bresenham(x0, y0, x1, y1, colour, draw_context):
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
