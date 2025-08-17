# My Personal Computer Graphics Project

This is a personal project dedicated to learning the fundamentals of computer graphics from scratch. I am building a simple 2D renderer to explore concepts like rasterization, coordinate systems, and scene configuration.

## Features

- **Rasterization**: Implements line, triangle, and circle drawing algorithms.
- **Scene Configuration**: Uses a `config.yaml` file to define scenes, objects, and materials.
- **Coordinate System**: A simple world-to-screen coordinate system with quadrant visualization.
- **Debug Tools**: Command-line flags for debugging and drawing object bounding boxes.

## Getting Started

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Renderer

To render the default scene defined in `inputs/config.yaml`, run the following command:

```bash
python main.py
```

The output will be saved to `outputs/rendered_scene.png` and will also be displayed in a new window.

#### Command-Line Arguments

- `--render <obj1> <obj2> ...`: Renders only the specified objects from the configuration file.
- `--debug`: Enables debug printing, which outputs detailed information about each object to the console and on the rendered image.
- `--bb`: Draws the bounding box for each rendered object.

**Example:**

```bash
python main.py --render test_circle_q1 test_circle_q4 --debug --bb
```

## Scene Configuration (`inputs/config.yaml`)

The scene is defined in a YAML file with the following structure:

- **`image_settings`**: Defines the canvas size and background color.
- **`camera`**: Specifies the camera type (currently `2d_orthographic`).
- **`renderer`**: Defines the rendering pipeline and options (e.g., `shading`).
- **`lights`**: A list of light sources in the scene (for future use with shading).
- **`materials`**: A dictionary of reusable materials, which define an object's visual properties.
- **`objects`**: A list of objects to be rendered, each with a name, type, material, and geometric properties.
    
## Future Plans

### 1. 2D Transformations and Viewing

Now that you can draw static shapes, the next step is to make them move and fit them into a scene.

*   **Transformations:** Learn how to manipulate your shapes. This involves applying mathematical operations (usually with matrices) to the vertices of your shapes. The core transformations are:
    *   **Translation:** Moving an object from one position to another.
    *   **Rotation:** Rotating an object around a point (like the origin or its center).
    *   **Scaling:** Changing the size of an object.
*   **Polygon Filling:** You've been drawing the outlines of shapes. The next challenge is to fill them with solid color. The classic method to learn is the **Scan-line Algorithm**, which fills a polygon row by row.
*   **Clipping:** In most scenes, you only want to draw what's inside a specific window or "viewport." Clipping algorithms determine which parts of your shapes are inside this view and discard the parts that are outside. For lines, you can study the **Cohen-Sutherland** or **Liang-Barsky** algorithms.

### 2. Moving into 3D Graphics

This is the most exciting leap. You'll extend the 2D concepts you've learned into three-dimensional space.

*   **3D Coordinate Systems & Transformations:** You'll start working with (x, y, z) coordinates. Your transformation matrices will expand from 3x3 (in homogeneous 2D coordinates) to 4x4 to handle 3D translation, rotation (now around X, Y, and Z axes), and scaling.
*   **Projections:** This is the crucial process of converting your 3D world back into a 2D image that can be displayed on your screen. There are two main types:
    *   **Orthographic Projection:** A direct, blueprint-like view where objects have the same size regardless of their distance from the camera.
    *   **Perspective Projection:** This is more realistic. Objects that are farther away appear smaller, creating a sense of depth.
*   **The 3D Rendering Pipeline (Basic):** You'll learn about the sequence of steps required to render a 3D scene, which includes modeling transformations (placing objects in the world), view transformation (placing the camera), projection, and finally, mapping to the screen (viewport transformation).

### 3. Making 3D Scenes Look Realistic

Once you can get a 3D wireframe object onto the screen, the next step is to make it look solid and real.

*   **Hidden Surface Removal:** In a 3D scene, some objects will be behind others. You need a way to determine which surfaces are visible to the camera and which are hidden. The most fundamental and widely used algorithm for this is **Z-buffering** (or Depth-buffering).
*   **Lighting and Shading:** This is where the magic happens. You'll simulate how light interacts with the surfaces of your objects to give them volume and texture. Key concepts include:
    *   **Light Types:** Directional lights (like the sun), point lights (like a lightbulb), and spotlights.
    *   **Shading Models:** You'll learn how to calculate the color of each pixel on a surface. You can start with **Flat Shading** (one color per triangle), then move to **Gouraud Shading** and **Phong Shading**, which create much smoother and more realistic lighting effects by considering how light reflects off a surface (diffuse and specular reflections).

---
*This project is for educational purposes and is a work in progress.*
