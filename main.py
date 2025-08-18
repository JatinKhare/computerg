import os
import sys
from PIL import Image, ImageDraw
import argparse
import numpy as np

from src.helper import *
from src.canvas import Canvas
from src.raster.triangle import *
from src.raster.circle import *
from src.raster.line import *
from src.raster.polygon import *
from src.transform import *

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
            draw_polygon(verts, color, canvas.draw, fill=True)
            
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

            final_transform_matrix_3d = np.identity(4)
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
                    final_transform_matrix_3d = np.dot(final_transform_matrix_3d, m)
            
            transformed_vertices_3d = [np.dot(final_transform_matrix_3d, v) for v in vertices_3d]

            projected_vertices = []
            for v in transformed_vertices_3d:
                screen_x = v[0] + v[2] * 0.5
                screen_y = v[1] - v[2] * 0.5
                projected_vertices.append(Point(*canvas.world_to_screen(screen_x, screen_y)))
            
            for edge in obj['edges']:
                p1 = projected_vertices[edge[0]]
                p2 = projected_vertices[edge[1]]
                draw_line_bresenham(p1.x, p1.y, p2.x, p2.y, color, canvas.draw)

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
