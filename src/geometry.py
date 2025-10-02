import numpy as np

def generate_sphere_mesh(radius=1.0, sectors=36, stacks=18):
    """
    Generates vertices and triangular faces for a sphere mesh.
    The sphere is centered at the origin (0, 0, 0).
    
    Args:
        radius (float): The radius of the sphere.
        sectors (int): The number of divisions around the Z-axis (longitude).
        stacks (int): The number of divisions along the Z-axis (latitude).

    Returns:
        tuple: A tuple containing:
            - list: A list of vertex coordinates [x, y, z, 1.0].
            - list: A list of faces, where each face is a list of vertex indices.
    """
    vertices = []
    pi = np.pi
    sector_step = 2 * pi / sectors
    stack_step = pi / stacks

    for i in range(stacks + 1):
        stack_angle = pi / 2 - i * stack_step
        xy = radius * np.cos(stack_angle)
        z = radius * np.sin(stack_angle)

        for j in range(sectors + 1):
            sector_angle = j * sector_step
            x = xy * np.cos(sector_angle)
            y = xy * np.sin(sector_angle)
            vertices.append([x, y, z, 1.0])

    faces = []
    for i in range(stacks):
        k1 = i * (sectors + 1)
        k2 = k1 + sectors + 1
        for j in range(sectors):
            if i != 0:
                faces.append([k1, k2, k1 + 1])
            if i != (stacks - 1):
                faces.append([k1 + 1, k2, k2 + 1])
            
            k1 += 1
            k2 += 1
            
    # The above logic creates triangles, but our polygon filler can handle quads,
    # which is simpler to define. Let's redefine faces as quads.
    faces = []
    for i in range(stacks):
        k1 = i * (sectors + 1)
        k2 = k1 + sectors + 1
        for j in range(sectors):
            # Define a quad face
            faces.append([k1, k1 + 1, k2 + 1, k2])
            k1 += 1
            k2 += 1

    return vertices, faces
