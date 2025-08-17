import os
import yaml

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

def world_to_screen(x, y, width, height):
    """Converts world coordinates to screen coordinates."""
    screen_x = x + width / 2
    screen_y = -y + height / 2
    return screen_x, screen_y

def draw_quadrant_boundaries(draw, width, height):
    """Draws lines to represent the quadrants."""
    # Draw horizontal line
    draw.line([(0, height / 2), (width, height / 2)], fill="black", width=1)
    # Draw vertical line
    draw.line([(width / 2, 0), (width / 2, height)], fill="black", width=1)

def print_debug_info(obj_name, obj_data, width, height):
    """Prints debug information for a given object."""
    print(f"Rendering {obj_name} ({obj_data['type']}):")
    if obj_data['type'] == 'triangle':
        for i, v in enumerate(obj_data['vertices']):
            quadrant = get_quadrant(v[0], v[1], width, height)
            screen_coords = world_to_screen(v[0], v[1], width, height)
            print(f"  - Vertex {i}: World={v}, Screen=({screen_coords[0]:.2f}, {screen_coords[1]:.2f}), Quadrant: {quadrant}")
    elif obj_data['type'] == 'circle':
        quadrant = get_quadrant(obj_data['center'][0], obj_data['center'][1], width, height)
        screen_coords = world_to_screen(obj_data['center'][0], obj_data['center'][1], width, height)
        print(f"  - Center: World={obj_data['center']}, Screen=({screen_coords[0]:.2f}, {screen_coords[1]:.2f}), Radius: {obj_data['radius']}, Quadrant: {quadrant}")
    elif obj_data['type'] == 'line':
        start_quadrant = get_quadrant(obj_data['start'][0], obj_data['start'][1], width, height)
        start_screen_coords = world_to_screen(obj_data['start'][0], obj_data['start'][1], width, height)
        end_quadrant = get_quadrant(obj_data['end'][0], obj_data['end'][1], width, height)
        end_screen_coords = world_to_screen(obj_data['end'][0], obj_data['end'][1], width, height)
        print(f"  - Start: World={obj_data['start']}, Screen=({start_screen_coords[0]:.2f}, {start_screen_coords[1]:.2f}), Quadrant: {start_quadrant}")
        print(f"  - End: World={obj_data['end']}, Screen=({end_screen_coords[0]:.2f}, {end_screen_coords[1]:.2f}), Quadrant: {end_quadrant}")

def get_quadrant(x, y, width, height):
    """Determines the quadrant of a point in world coordinates."""
    if x >= 0 and y >= 0:
        return 1
    elif x < 0 and y >= 0:
        return 2
    elif x < 0 and y < 0:
        return 3
    elif x >= 0 and y < 0:
        return 4
    return "Origin"

def draw_bounding_box(obj, draw, width, height):
    """Draws the bounding box for a given object."""
    if obj['type'] == 'triangle':
        verts = [world_to_screen(v[0], v[1], width, height) for v in obj['vertices']]
        min_x = min(v[0] for v in verts)
        min_y = min(v[1] for v in verts)
        max_x = max(v[0] for v in verts)
        max_y = max(v[1] for v in verts)
        draw.rectangle([min_x, min_y, max_x, max_y], outline="green")
    elif obj['type'] == 'circle':
        center = world_to_screen(obj['center'][0], obj['center'][1], width, height)
        radius = obj['radius']
        draw.rectangle([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline="green")
    elif obj['type'] == 'line':
        start = world_to_screen(obj['start'][0], obj['start'][1], width, height)
        end = world_to_screen(obj['end'][0], obj['end'][1], width, height)
        draw.rectangle([min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]), max(start[1], end[1])], outline="green")

def write_debug_info(draw, obj_name, obj_data, width, height, y_offset):
    """Draws debug information for a given object on the image."""
    info_lines = []
    info_lines.append(f"Rendering {obj_name} ({obj_data['type']}):")
    if obj_data['type'] == 'triangle':
        for i, v in enumerate(obj_data['vertices']):
            quadrant = get_quadrant(v[0], v[1], width, height)
            screen_coords = world_to_screen(v[0], v[1], width, height)
            info_lines.append(f"  - Vertex {i}: World={v}, Screen=({screen_coords[0]:.2f}, {screen_coords[1]:.2f}), Quadrant: {quadrant}")
    elif obj_data['type'] == 'circle':
        quadrant = get_quadrant(obj_data['center'][0], obj_data['center'][1], width, height)
        screen_coords = world_to_screen(obj_data['center'][0], obj_data['center'][1], width, height)
        info_lines.append(f"  - Center: World={obj_data['center']}, Screen=({screen_coords[0]:.2f}, {screen_coords[1]:.2f}), Radius: {obj_data['radius']}, Quadrant: {quadrant}")
    elif obj_data['type'] == 'line':
        start_quadrant = get_quadrant(obj_data['start'][0], obj_data['start'][1], width, height)
        start_screen_coords = world_to_screen(obj_data['start'][0], obj_data['start'][1], width, height)
        end_quadrant = get_quadrant(obj_data['end'][0], obj_data['end'][1], width, height)
        end_screen_coords = world_to_screen(obj_data['end'][0], obj_data['end'][1], width, height)
        info_lines.append(f"  - Start: World={obj_data['start']}, Screen=({start_screen_coords[0]:.2f}, {start_screen_coords[1]:.2f}), Quadrant: {start_quadrant}")
        info_lines.append(f"  - End: World={obj_data['end']}, Screen=({end_screen_coords[0]:.2f}, {end_screen_coords[1]:.2f}), Quadrant: {end_quadrant}")

    x_pos = width - 600
    line_height = 15
    for i, line in enumerate(info_lines):
        y_pos = y_offset + (i * line_height)
        draw.text((x_pos, y_pos), line, fill="black")

    draw.text((width/2 + 5, height/2), f"{int(width/2)} x {int(height/2)}", fill="black")
    return y_offset + (len(info_lines) * line_height)
