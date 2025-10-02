from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])

def scanline_fill(vertices, color, draw_func, z_buffer=None):
    """Fills a polygon using the scanline algorithm, with Z-buffer support."""
    if len(vertices) < 3:
        return

    # Separate x, y, z coordinates. Assumes vertices are Point3D objects.
    verts_2d = [(v.x, v.y) for v in vertices]
    z_coords = [v.z for v in vertices]

    min_y = int(min(verts_2d, key=lambda p: p[1])[1])
    max_y = int(max(verts_2d, key=lambda p: p[1])[1])

    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(verts_2d)):
            p1 = verts_2d[i]
            p2 = verts_2d[(i + 1) % len(verts_2d)]

            if p1[1] == p2[1]: # Horizontal line
                continue
            if min(p1[1], p2[1]) <= y < max(p1[1], p2[1]):
                x = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                intersections.append(x)

        intersections.sort()

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start = int(intersections[i])
                x_end = int(intersections[i+1])
                for x in range(x_start, x_end):
                    if z_buffer is not None:
                        # Simplified depth check using average Z.
                        avg_z = sum(z_coords) / len(z_coords)
                        if 0 <= x < z_buffer.shape[0] and 0 <= y < z_buffer.shape[1]:
                           if avg_z < z_buffer[x, y]:
                               z_buffer[x, y] = avg_z
                               draw_func.point((x, y), fill=color.to_tuple())
                    else:
                        # Fallback for 2D shapes without a z_buffer
                        draw_func.point((x, y), fill=color.to_tuple())