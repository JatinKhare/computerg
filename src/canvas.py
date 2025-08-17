from PIL import Image, ImageDraw

class Canvas:
    def __init__(self, width, height, bg_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.image = Image.new("RGB", (self.width, self.height), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

    def save(self, output_path):
        self.image.save(output_path)
        print(f"Scene saved to {output_path}")

    def show(self):
        self.image.show()

    def world_to_screen(self, x, y):
        """Converts world coordinates to screen coordinates."""
        screen_x = int(x + self.width / 2)
        screen_y = int(-y + self.height / 2)
        return screen_x, screen_y

    def draw_quadrant_boundaries(self):
        """Draws lines to represent the quadrants."""
        self.draw.line([(0, self.height / 2), (self.width, self.height / 2)], fill="black", width=1)
        self.draw.line([(self.width / 2, 0), (self.width / 2, self.height)], fill="black", width=1)

    def get_quadrant(self, x, y):
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
