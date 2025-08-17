import os
import sys
from PIL import Image, ImageDraw
import argparse
import numpy as np

from src.resterization import *
from src.helper import *

DIRECTORIES_TO_CREATE = [
    "src",
    "inputs",
    "outputs"
]

def render_scene(config, objects_to_render=None, debug=False, bb=False):
    """Renders the scene based on the provided configuration."""
    if not config or 'scene' not in config:
        print("Invalid or empty configuration.")
        return

    settings = config['scene']['image_settings']
    width = settings['width']
    height = settings['height']
    bg_color = tuple(settings['background_color'])

    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    draw_quadrant_boundaries(draw, width, height)

    all_objects = config['scene']['objects']
    
    if objects_to_render:
        render_list = {name: all_objects[name] for name in objects_to_render if name in all_objects}
    else:
        render_list = all_objects

    y_offset = 10
    for name, obj in render_list.items():
        if debug:
            print_debug_info(name, obj, width, height)
            y_offset = write_debug_info(draw, name, obj, width, height, y_offset)
        if bb:
            draw_bounding_box(obj, draw, width, height)
        if obj['type'] == 'triangle':
            verts = [Point(*world_to_screen(v[0], v[1], width, height)) for v in obj['vertices']]
            color = Colour(obj['color'][0], obj['color'][1], obj['color'][2])
            draw_triangle(verts[0], verts[1], verts[2], color, draw)
        elif obj['type'] == 'circle':
            center = Point(*world_to_screen(obj['center'][0], obj['center'][1], width, height))
            radius = obj['radius']
            color = Colour(obj['color'][0], obj['color'][1], obj['color'][2])
            #draw_circle_float(center, radius, color, draw)
            draw_circle_int(center, radius, color, draw)
        elif obj['type'] == 'line':
            start = Point(*world_to_screen(obj['start'][0], obj['start'][1], width, height))
            end = Point(*world_to_screen(obj['end'][0], obj['end'][1], width, height))
            color = Colour(obj['color'][0], obj['color'][1], obj['color'][2])
            draw_line_float_simple(start.x, start.y, end.x, end.y, color, draw)
            #draw_line(start.x, start.y, end.x, end.y, color, draw)

    output_path = os.path.join("outputs", "rendered_scene.png")
    image.save(output_path)
    print(f"Scene saved to {output_path}")
    image.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a scene from a config file.")
    parser.add_argument('--render', nargs='*', help='A list of object names to render.')
    parser.add_argument('--debug', action='store_true', help='Enable debug printing.')
    parser.add_argument('--bb', action='store_true', help='Draw bounding boxes.')
    args = parser.parse_args()

    create_directories(DIRECTORIES_TO_CREATE)
    config = load_config("inputs/config.yaml")
    render_scene(config, args.render, args.debug, args.bb)
