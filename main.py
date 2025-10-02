import os
import sys
from PIL import Image, ImageDraw
import argparse
import numpy as np
from collections import namedtuple

from src.helper import *
from src.canvas import Canvas
from src.raster.triangle import *
from src.raster.circle import *
from src.raster.line import *
from src.raster.polygon import *
from src.transform import *
from src.raster.raster_help import *
from src.camera import Camera
from src.geometry import generate_sphere_mesh

Point3D = namedtuple('Point3D', ['x', 'y', 'z'])
DIRECTORIES_TO_CREATE = ["src", "inputs", "outputs"]

class Scene:
    """Parses and holds the scene configuration."""
    def __init__(self, config_path):
        config = load_config(config_path)
        if not config or 'scene' not in config:
            raise ValueError("Invalid or empty configuration.")
        
        scene_data = config['scene']
        self.settings = scene_data['image_settings']
        self.materials = scene_data['materials']
        self.objects = scene_data['objects']
        self.lights = scene_data.get('lights', []) # Use .get for safety
        
        cam_config = scene_data['camera']
        self.camera_type = cam_config['type']
        aspect_ratio = self.settings['width'] / self.settings['height']
        self.camera = Camera(
            position=cam_config['position'],
            target=cam_config['target'],
            up=cam_config['up'],
            fov=cam_config.get('fov', 60),
            aspect_ratio=aspect_ratio,
            near=cam_config['near'],
            far=cam_config['far'],
            ortho_bounds=cam_config.get('ortho_bounds')
        )

    def get_render_list(self, objects_to_render):
        if objects_to_render:
            return [obj for obj in self.objects if obj['name'] in objects_to_render]
        return self.objects

def render_scene(scene, objects_to_render=None, debug=False, bb=False):
    """Renders the scene based on the provided configuration."""
    width = scene.settings['width']
    height = scene.settings['height']
    bg_color = tuple(scene.settings['background_color'])
    
    canvas = Canvas(width, height, bg_color)
    canvas.draw_quadrant_boundaries()

    render_list = scene.get_render_list(objects_to_render)

    view_matrix = scene.camera.get_view_matrix()
    projection_matrix = scene.camera.get_projection_matrix(scene.camera_type)
    view_projection_matrix = np.dot(projection_matrix, view_matrix)

    # Extract light information from the scene
    ambient_light = next((l for l in scene.lights if l['type'] == 'ambient'), None)
    directional_light = next((l for l in scene.lights if l['type'] == 'directional'), None)

    y_offset = 10
    for obj in render_list:
        name = obj['name']
        if debug:
            print_debug_info(name, obj, canvas)
            y_offset = write_debug_info(name, obj, canvas, y_offset)
        if bb:
            draw_bounding_box(obj, canvas)
        
        try:
            material_name = obj['material']
            material = scene.materials[material_name]
            color = Colour(*material['color'])
        except KeyError:
            print(f"Warning: Material '{obj.get('material', 'N/A')}' not found or invalid for object '{name}'. Skipping.")
            continue

        # Process transformations
        final_transform_matrix = np.identity(3)
        if 'transform' in obj:
            for t in reversed(obj['transform']):
                m = np.identity(3)
                if t['type'] == 'translate':
                    m = create_translation_matrix(*t['offset'])
                elif t['type'] == 'rotate':
                    m = create_rotation_matrix(t['angle'])
                elif t['type'] == 'scale':
                    m = create_scaling_matrix(*t['factor'])
                final_transform_matrix = np.dot(final_transform_matrix, m)

        if obj['type'] == 'triangle':
            original_vertices = obj['vertices']
            transformed_vertices = []
            for v in original_vertices:
                homogeneous_v = np.array([v[0], v[1], 1])
                transformed_v = np.dot(final_transform_matrix, homogeneous_v)
                transformed_vertices.append([transformed_v[0], transformed_v[1]])
            
            verts = [Point(*canvas.world_to_screen(v[0], v[1])) for v in transformed_vertices]
            draw_triangle(verts[0], verts[1], verts[2], color, canvas.draw, fill=True)
        elif obj['type'] == 'circle':
            # Note: Transformations on circles require more care.
            # Scaling can make it an ellipse, and rotation is only visible if it's not a solid color.
            # For now, we apply transformations only to the center.
            original_center = obj['center']
            homogeneous_c = np.array([original_center[0], original_center[1], 1])
            transformed_c = np.dot(final_transform_matrix, homogeneous_c)
            
            center = Point(*canvas.world_to_screen(transformed_c[0], transformed_c[1]))
            radius = obj['radius']
            draw_circle_int(center, radius, color, canvas.draw, fill=True)
        elif obj['type'] == 'line':
            original_vertices = [obj['start'], obj['end']]
            transformed_vertices = []
            for v in original_vertices:
                homogeneous_v = np.array([v[0], v[1], 1])
                transformed_v = np.dot(final_transform_matrix, homogeneous_v)
                transformed_vertices.append([transformed_v[0], transformed_v[1]])

            start = Point(*canvas.world_to_screen(transformed_vertices[0][0], transformed_vertices[0][1]))
            end = Point(*canvas.world_to_screen(transformed_vertices[1][0], transformed_vertices[1][1]))
            draw_line_bresenham(start.x, start.y, end.x, end.y, color, canvas.draw)
        elif obj['type'] == 'polygon':
            original_vertices = obj['vertices']
            transformed_vertices = []
            for v in original_vertices:
                homogeneous_v = np.array([v[0], v[1], 1])
                transformed_v = np.dot(final_transform_matrix, homogeneous_v)
                transformed_vertices.append([transformed_v[0], transformed_v[1]])
                
            verts = [Point(*canvas.world_to_screen(v[0], v[1])) for v in transformed_vertices]
            scanline_fill_custom(verts, color, canvas.draw)
        
        elif obj['type'] == 'sphere':
            # 1. Generate the sphere mesh
            radius = obj.get('radius', 1)
            sectors = obj.get('sectors', 36)
            stacks = obj.get('stacks', 18)
            local_vertices, faces = generate_sphere_mesh(radius, sectors, stacks)
            
            # 2. Apply transformations (same as cube)
            model_matrix = np.identity(4)
            # Apply a translation for the sphere's center
            center = obj.get('center', [0, 0, 0])
            center_translation = create_3d_translation_matrix(*center)
            model_matrix = np.dot(center_translation, model_matrix)

            if 'transform' in obj:
                for t in reversed(obj['transform']):
                    m = np.identity(4)
                    if t['type'] == 'translate_3d':
                        m = create_3d_translation_matrix(*t['offset'])
                    elif t['type'] == 'rotate_x':
                        m = create_3d_rotation_matrix_x(t['angle'])
                    elif t['type'] == 'rotate_y':
                        m = create_3d_rotation_matrix_y(t['angle'])
                    elif t['type'] == 'rotate_z':
                        m = create_3d_rotation_matrix_z(t['angle'])
                    elif t['type'] == 'scale_3d':
                        m = create_3d_scaling_matrix(*t['factor'])
                    model_matrix = np.dot(model_matrix, m)
            
            mvp_matrix = np.dot(view_projection_matrix, model_matrix)
            transformed_vertices_3d = [np.dot(mvp_matrix, v) for v in local_vertices]

            projected_vertices = []
            for v in transformed_vertices_3d:
                depth_z = v[2]
                if v[3] != 0:
                    v /= v[3]
                screen_x = (v[0] + 1) * 0.5 * width
                screen_y = (1 - v[1]) * 0.5 * height
                projected_vertices.append(Point3D(int(screen_x), int(screen_y), depth_z))

            # 3. Render faces with lighting (same as cube)
            for face in faces:
                face_world_verts = [np.dot(model_matrix, local_vertices[i]) for i in face]
                v0, v1, v2 = face_world_verts[0][:3], face_world_verts[1][:3], face_world_verts[2][:3]
                normal = np.cross(v1 - v0, v2 - v0)
                if np.linalg.norm(normal) == 0:
                    continue
                normal = normal / np.linalg.norm(normal)

                final_color = color
                if directional_light:
                    light_dir = np.array(directional_light['direction'])
                    light_dir = light_dir / np.linalg.norm(light_dir)
                    diffuse_intensity = max(0, np.dot(normal, light_dir))
                    ambient_intensity = ambient_light['intensity'] if ambient_light else 0.1
                    total_intensity = ambient_intensity + (diffuse_intensity * directional_light.get('intensity', 1.0))
                    final_color = Colour(
                        min(255, color.r * total_intensity),
                        min(255, color.g * total_intensity),
                        min(255, color.b * total_intensity)
                    )

                face_vertices = [projected_vertices[i] for i in face]
                scanline_fill(face_vertices, final_color, canvas.draw, canvas.z_buffer)

        elif obj['type'] == 'cube_3d':
            center = obj['center']
            size = obj['size']
            s = size / 2
            
            vertices_3d = [
                np.array([center[0] - s, center[1] - s, center[2] - s, 1]),
                np.array([center[0] + s, center[1] - s, center[2] - s, 1]),
                np.array([center[0] + s, center[1] + s, center[2] - s, 1]),
                np.array([center[0] - s, center[1] + s, center[2] - s, 1]),
                np.array([center[0] - s, center[1] - s, center[2] + s, 1]),
                np.array([center[0] + s, center[1] - s, center[2] + s, 1]),
                np.array([center[0] + s, center[1] + s, center[2] + s, 1]),
                np.array([center[0] - s, center[1] + s, center[2] + s, 1]),
            ]

            model_matrix = np.identity(4)
            if 'transform' in obj:
                for t in reversed(obj['transform']):
                    if t['type'] == 'translate_3d':
                        m = create_3d_translation_matrix(*t['offset'])
                    elif t['type'] == 'rotate_x':
                        m = create_3d_rotation_matrix_x(t['angle'])
                    elif t['type'] == 'rotate_y':
                        m = create_3d_rotation_matrix_y(t['angle'])
                    elif t['type'] == 'rotate_z':
                        m = create_3d_rotation_matrix_z(t['angle'])
                    elif t['type'] == 'scale_3d':
                        m = create_3d_scaling_matrix(*t['factor'])
                    model_matrix = np.dot(model_matrix, m)
            
            mvp_matrix = np.dot(view_projection_matrix, model_matrix)
            
            transformed_vertices_3d = [np.dot(mvp_matrix, v) for v in vertices_3d]

            projected_vertices = []
            for v in transformed_vertices_3d:
                # Store the original z value for depth testing
                depth_z = v[2]

                # Perspective divide (convert from homogeneous to Cartesian coordinates)
                if v[3] != 0:
                    v /= v[3]
                
                # Map from Normalized Device Coordinates (NDC) to screen coordinates
                screen_x = (v[0] + 1) * 0.5 * width
                screen_y = (1 - v[1]) * 0.5 * height # Y is inverted in screen space
                projected_vertices.append(Point3D(int(screen_x), int(screen_y), depth_z))
            
            # 1. Fill the faces (with Z-buffering and shading)
            if 'faces' in obj:
                for face in obj['faces']:
                    # Get the vertices of the face in world space (before projection)
                    face_world_verts = [np.dot(model_matrix, vertices_3d[i]) for i in face]

                    # Calculate the face normal in world space
                    v0, v1, v2 = face_world_verts[0][:3], face_world_verts[1][:3], face_world_verts[2][:3]
                    normal = np.cross(v1 - v0, v2 - v0)
                    normal = normal / np.linalg.norm(normal)

                    # --- Lighting Calculation ---
                    final_color = color
                    if directional_light:
                        light_dir = np.array(directional_light['direction'])
                        light_dir = light_dir / np.linalg.norm(light_dir)
                        
                        # Calculate diffuse intensity (dot product)
                        diffuse_intensity = max(0, np.dot(normal, light_dir))
                        
                        # Combine with ambient light
                        ambient_intensity = ambient_light['intensity'] if ambient_light else 0.1
                        total_intensity = ambient_intensity + (diffuse_intensity * directional_light.get('intensity', 1.0))
                        
                        # Apply to the material color
                        final_color = Colour(
                            min(255, color.r * total_intensity),
                            min(255, color.g * total_intensity),
                            min(255, color.b * total_intensity)
                        )

                    face_vertices = [projected_vertices[i] for i in face]
                    scanline_fill(face_vertices, final_color, canvas.draw, canvas.z_buffer)

            # 2. Draw the edges on top
            if 'edges' in obj and 'edge_color' in obj:
                try:
                    edge_material_name = obj['edge_color']
                    edge_material = scene.materials[edge_material_name]
                    edge_color = Colour(*edge_material['color'])
                    
                    for edge in obj['edges']:
                        p1 = projected_vertices[edge[0]]
                        p2 = projected_vertices[edge[1]]
                        draw_line_bresenham(p1.x, p1.y, p2.x, p2.y, edge_color, canvas.draw)
                except KeyError:
                    # Silently fail if edge material is missing
                    pass

    output_path = os.path.join("outputs", "rendered_scene.png")
    canvas.save(output_path)
    canvas.show()

def main():
    """Main function to parse arguments and render the scene."""
    parser = argparse.ArgumentParser(description="Render a scene from a config file.")
    parser.add_argument('--render', nargs='*', help='A list of object names to render.')
    parser.add_argument('--debug', action='store_true', help='Enable debug printing.')
    parser.add_argument('--bb', action='store_true', help='Draw bounding boxes.')
    args = parser.parse_args()

    create_directories(DIRECTORIES_TO_CREATE)
    
    try:
        scene = Scene("inputs/config.yaml")
        render_scene(scene, args.render, args.debug, args.bb)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
