import os
import random
from PIL import Image, ImageDraw

# Constants
DEFAULT_SIZE = (500, 500)  # Default size of the generated image
DEFAULT_COLOR_COUNT = 1    # Default number of colors in the image
OUTPUT_DIR = '/sdcard/downloads'  # Default output directory

def generate_random_color():
    """Generate a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def create_color_square(size, color):
    """Create an image with a single color square."""
    image = Image.new('RGB', size, color)
    return image

def save_image(image, filename):
    """Save the image to the specified filename."""
    try:
        image.save(filename)
        print(f"Image saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")

def generate_image(size=DEFAULT_SIZE, color_count=DEFAULT_COLOR_COUNT, output_dir=OUTPUT_DIR):
    """Generate an image with random color squares and save it to the specified directory."""
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"Error creating directory: {e}")
            return

    # Generate the image
    if color_count == 1:
        color = generate_random_color()
        image = create_color_square(size, color)
    else:
        # For multiple colors, divide the image into equal parts
        width, height = size
        part_width = width // color_count
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)
        for i in range(color_count):
            color = generate_random_color()
            left = i * part_width
            right = (i + 1) * part_width if i < color_count - 1 else width
            draw.rectangle([left, 0, right, height], fill=color)

    # Generate a unique filename
    filename = os.path.join(output_dir, f"color_square_{random.randint(1000, 9999)}.png")
    
    # Save the image
    save_image(image, filename)

if __name__ == "__main__":
    # Example usage
    generate_image(size=(600, 400), color_count=3)