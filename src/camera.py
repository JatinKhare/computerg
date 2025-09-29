import numpy as np
from src.transform import create_3d_rotation_matrix_x, create_3d_rotation_matrix_y, create_3d_rotation_matrix_z

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

class Camera:
    def __init__(self, position, target, up, fov, aspect_ratio, near, far, ortho_bounds=None):
        self.position = np.array(position, dtype=float)
        self.target = np.array(target, dtype=float)
        self.up = normalize(np.array(up, dtype=float))
        
        # Perspective properties
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        # General properties
        self.near = near
        self.far = far

        # Orthographic properties
        self.ortho_bounds = ortho_bounds # Should be [left, right, bottom, top]

    def get_view_matrix(self):
        # Create a coordinate system for the camera
        forward = normalize(self.target - self.position)
        right = normalize(np.cross(forward, self.up))
        up = normalize(np.cross(right, forward))

        # Create the rotation matrix to align world coordinates with camera coordinates
        rotation = np.array([
            [right[0], right[1], right[2], 0],
            [up[0], up[1], up[2], 0],
            [-forward[0], -forward[1], -forward[2], 0],
            [0, 0, 0, 1]
        ])

        # Create the translation matrix to move the world to the camera's position
        translation = np.array([
            [1, 0, 0, -self.position[0]],
            [0, 1, 0, -self.position[1]],
            [0, 0, 1, -self.position[2]],
            [0, 0, 0, 1]
        ])

        # The view matrix is the combination of translation and rotation
        return np.dot(rotation, translation)

    def get_projection_matrix(self, projection_type='perspective'):
        if projection_type == 'perspective':
            f = 1.0 / np.tan(np.radians(self.fov) / 2)
            return np.array([
                [f / self.aspect_ratio, 0, 0, 0],
                [0, f, 0, 0],
                [0, 0, (self.far + self.near) / (self.near - self.far), (2 * self.far * self.near) / (self.near - self.far)],
                [0, 0, -1, 0]
            ])
        elif projection_type == 'orthographic':
            if self.ortho_bounds:
                left, right, bottom, top = self.ortho_bounds
            else:
                # Fallback to a default view if not specified
                right = self.aspect_ratio * 10
                left = -right
                top = 10
                bottom = -top
            
            return np.array([
                [2 / (right - left), 0, 0, -(right + left) / (right - left)],
                [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
                [0, 0, -2 / (self.far - self.near), -(self.far + self.near) / (self.far - self.near)],
                [0, 0, 0, 1]
            ])
        else:
            return np.identity(4)
