import os
import sys
from PIL import Image, ImageDraw
import argparse

from src.resterization import Point, Colour, draw_triangle, draw_circle_wrong, draw_circle_right, draw_line
from src.helper import create_directories, load_config

DIRECTORIES_TO_CREATE = [
    "src",
    "inputs",
    "outputs"
]

def render_scene(config, objects_to_render=None):
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

    all_objects = config['scene']['objects']
    
    if objects_to_render:
        render_list = {name: all_objects[name] for name in objects_to_render if name in all_objects}
    else:
        render_list = all_objects

    for name, obj in render_list.items():
        if obj['type'] == 'triangle':
            verts = [Point(v[0], v[1]) for v in obj['vertices']]
            colors = [Colour(c[0], c[1], c[2]) for c in obj['colors']]
            draw_triangle(verts[0], verts[1], verts[2], colors[0], colors[1], colors[2], draw)
        elif obj['type'] == 'circle':
            center = Point(obj['center'][0], obj['center'][1])
            radius = obj['radius']
            #draw_circle_wrong(center, radius, obj['color'], draw)
            draw_circle_right(center, radius, obj['color'], draw)
        elif obj['type'] == 'line':
            start = Point(obj['start'][0], obj['start'][1])
            end = Point(obj['end'][0], obj['end'][1])
            color = Colour(obj['color'][0], obj['color'][1], obj['color'][2])
            draw_line(start.x, start.y, end.x, end.y, color, draw)

    output_path = os.path.join("outputs", "rendered_scene.png")
    image.save(output_path)
    print(f"Scene saved to {output_path}")
    image.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a scene from a config file.")
    parser.add_argument('--render', nargs='*', help='A list of object names to render.')
    args = parser.parse_args()

    create_directories(DIRECTORIES_TO_CREATE)
    config = load_config("inputs/config.yaml")
    render_scene(config, args.render)
