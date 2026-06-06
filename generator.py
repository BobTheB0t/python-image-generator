import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ImageGenerator:
    def __init__(self, output_dir="generated_images", font_path="fonts/arial.ttf", font_size=40, text_color=(0, 0, 0)):
        """
        Initialize the ImageGenerator with default settings.

        :param output_dir: Directory to save generated images
        :param font_path: Path to the font file
        :param font_size: Font size for the text
        :param text_color: Text color in RGB format
        """
        self.output_dir = output_dir
        self.font_path = font_path
        self.font_size = font_size
        self.text_color = text_color

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Load the font
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            raise FileNotFoundError(f"Font file not found at {self.font_path}")

    def generate_image(self, prompt, size=500, background_color=(255, 255, 255)):
        """
        Generate a square image with the given prompt.

        :param prompt: Text to be displayed on the image
        :param size: Size of the square image
        :param background_color: Background color in RGB format
        :return: Path to the saved image
        """
        try:
            # Create a new image with the specified size and background color
            image = Image.new("RGB", (size, size), background_color)
            draw = ImageDraw.Draw(image)

            # Wrap the text to fit within the image
            lines = textwrap.wrap(prompt, width=20)

            # Calculate the total height of the text
            total_height = len(lines) * self.font_size

            # Calculate the starting y-coordinate to center the text
            y = (size - total_height) // 2

            # Draw each line of text
            for line in lines:
                text_width, text_height = draw.textsize(line, font=self.font)
                x = (size - text_width) // 2
                draw.text((x, y), line, font=self.font, fill=self.text_color)
                y += text_height

            # Save the image
            image_path = os.path.join(self.output_dir, f"{prompt[:20]}_{size}.png")
            image.save(image_path)
            return image_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate image: {e}")

# Example usage
if __name__ == "__main__":
    generator = ImageGenerator()
    prompt = "Hello, this is a test image generated using Python!"
    image_path = generator.generate_image(prompt)
    print(f"Image saved at: {image_path}")