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

        if obj['type'] == 'triangle':
            verts = [Point(*canvas.world_to_screen(v[0], v[1])) for v in obj['vertices']]
            draw_triangle(verts[0], verts[1], verts[2], color, canvas.draw)
        elif obj['type'] == 'circle':
            center = Point(*canvas.world_to_screen(obj['center'][0], obj['center'][1]))
            radius = obj['radius']
            draw_circle_int(center, radius, color, canvas.draw, fill=True)
        elif obj['type'] == 'line':
            start = Point(*canvas.world_to_screen(obj['start'][0], obj['start'][1]))
            end = Point(*canvas.world_to_screen(obj['end'][0], obj['end'][1]))
            draw_line_bresenham(start.x, start.y, end.x, end.y, color, canvas.draw)

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
