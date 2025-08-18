import numpy as np

def create_translation_matrix(tx, ty):
    """Creates a 3x3 translation matrix."""
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

def create_scaling_matrix(sx, sy):
    """Creates a 3x3 scaling matrix."""
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def create_rotation_matrix(angle_degrees):
    """Creates a 3x3 rotation matrix."""
    angle_radians = np.radians(angle_degrees)
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    return np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])

# --- 3D Transformation Matrices ---

def create_3d_translation_matrix(tx, ty, tz):
    """Creates a 4x4 translation matrix."""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def create_3d_scaling_matrix(sx, sy, sz):
    """Creates a 4x4 scaling matrix."""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def create_3d_rotation_matrix_x(angle_degrees):
    """Creates a 4x4 rotation matrix around the X-axis."""
    angle_radians = np.radians(angle_degrees)
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def create_3d_rotation_matrix_y(angle_degrees):
    """Creates a 4x4 rotation matrix around the Y-axis."""
    angle_radians = np.radians(angle_degrees)
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

def create_3d_rotation_matrix_z(angle_degrees):
    """Creates a 4x4 rotation matrix around the Z-axis."""
    angle_radians = np.radians(angle_degrees)
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
