import os
import yaml

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Colour:
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

def create_directories(dirs_to_create):
    """Creates the necessary directories for the project."""
    for directory in dirs_to_create:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory '{directory}' created successfully.")
            except OSError as e:
                print(f"Error creating directory '{directory}': {e}")
        else:
            return

def load_config(config_path):
    """Loads the YAML configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def print_debug_info(obj_name, obj_data, canvas):
    """Prints debug information for a given object."""
    width = canvas.width
    height = canvas.height
    print(f"Rendering {obj_name} ({obj_data['type']}):")
    if obj_data['type'] == 'triangle':
        for i, v in enumerate(obj_data['vertices']):
            quadrant = canvas.get_quadrant(v[0], v[1])
            screen_coords = canvas.world_to_screen(v[0], v[1])
            print(f"  - Vertex {i}: World={v}, Screen=({screen_coords[0]:.0f}, {screen_coords[1]:.0f}), Quadrant: {quadrant}")
    elif obj_data['type'] == 'circle':
        quadrant = canvas.get_quadrant(obj_data['center'][0], obj_data['center'][1])
        screen_coords = canvas.world_to_screen(obj_data['center'][0], obj_data['center'][1])
        print(f"  - Center: World={obj_data['center']}, Screen=({screen_coords[0]:.0f}, {screen_coords[1]:.0f}), Radius: {obj_data['radius']}, Quadrant: {quadrant}")
    elif obj_data['type'] == 'line':
        start_quadrant = canvas.get_quadrant(obj_data['start'][0], obj_data['start'][1])
        start_screen_coords = canvas.world_to_screen(obj_data['start'][0], obj_data['start'][1])
        end_quadrant = canvas.get_quadrant(obj_data['end'][0], obj_data['end'][1])
        end_screen_coords = canvas.world_to_screen(obj_data['end'][0], obj_data['end'][1])
        print(f"  - Start: World={obj_data['start']}, Screen=({start_screen_coords[0]}, {start_screen_coords[1]:.0f}), Quadrant: {start_quadrant}")
        print(f"  - End: World={obj_data['end']}, Screen=({end_screen_coords[0]:.0f}, {end_screen_coords[1]:.0f}), Quadrant: {end_quadrant}")

def draw_bounding_box(obj, canvas):
    """Draws the bounding box for a given object."""
    draw = canvas.draw
    if obj['type'] == 'triangle':
        verts = [canvas.world_to_screen(v[0], v[1]) for v in obj['vertices']]
        min_x = min(v[0] for v in verts)
        min_y = min(v[1] for v in verts)
        max_x = max(v[0] for v in verts)
        max_y = max(v[1] for v in verts)
        draw.rectangle([min_x, min_y, max_x, max_y], outline="green")
    elif obj['type'] == 'circle':
        center = canvas.world_to_screen(obj['center'][0], obj['center'][1])
        radius = obj['radius']
        draw.rectangle([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline="green")
    elif obj['type'] == 'line':
        start = canvas.world_to_screen(obj['start'][0], obj['start'][1])
        end = canvas.world_to_screen(obj['end'][0], obj['end'][1])
        draw.rectangle([min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]), max(start[1], end[1])], outline="green")

def write_debug_info(obj_name, obj_data, canvas, y_offset):
    """Draws debug information for a given object on the image."""
    draw = canvas.draw
    width = canvas.width
    height = canvas.height
    info_lines = []
    info_lines.append(f"Rendering {obj_name} ({obj_data['type']}):")
    if obj_data['type'] == 'triangle':
        for i, v in enumerate(obj_data['vertices']):
            quadrant = canvas.get_quadrant(v[0], v[1])
            screen_coords = canvas.world_to_screen(v[0], v[1])
            info_lines.append(f"  - Vertex {i}: World={v}, Screen=({screen_coords[0]:.0f}, {screen_coords[1]:.0f}), Quadrant: {quadrant}")
    elif obj_data['type'] == 'circle':
        quadrant = canvas.get_quadrant(obj_data['center'][0], obj_data['center'][1])
        screen_coords = canvas.world_to_screen(obj_data['center'][0], obj_data['center'][1])
        info_lines.append(f"  - Center: World={obj_data['center']}, Screen=({screen_coords[0]:.0f}, {screen_coords[1]:.0f}), Radius: {obj_data['radius']}, Quadrant: {quadrant}")
    elif obj_data['type'] == 'line':
        start_quadrant = canvas.get_quadrant(obj_data['start'][0], obj_data['start'][1])
        start_screen_coords = canvas.world_to_screen(obj_data['start'][0], obj_data['start'][1])
        end_quadrant = canvas.get_quadrant(obj_data['end'][0], obj_data['end'][1])
        end_screen_coords = canvas.world_to_screen(obj_data['end'][0], obj_data['end'][1])
        info_lines.append(f"  - Start: World={obj_data['start']}, Screen=({start_screen_coords[0]:.0f}, {start_screen_coords[1]:.0f}), Quadrant: {start_quadrant}")
        info_lines.append(f"  - End: World={obj_data['end']}, Screen=({end_screen_coords[0]:.0f}, {end_screen_coords[1]:.0f}), Quadrant: {end_quadrant}")

    x_pos = width - 600
    line_height = 15
    for i, line in enumerate(info_lines):
        y_pos = y_offset + (i * line_height)
        draw.text((x_pos, y_pos), line, fill="black")

    draw.text((width/2 + 5, height/2), f"{int(width/2)} x {int(height/2)}", fill="black")
    return y_offset + (len(info_lines) * line_height)
