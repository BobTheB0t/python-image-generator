import random
from typing import Tuple
from PIL import Image

class ImageGenerator:
    """Generates random color square images based on user prompts."""

    def __init__(self, output_dir: str = 'output'):
        """
        Initialize the image generator.

        Args:
            output_dir: Directory to save generated images
        """
        self.output_dir = output_dir
        # Ensure output directory exists
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def generate_random_color(self) -> Tuple[int, int, int]:
        """Generate a random RGB color tuple."""
        return tuple(random.randint(0, 255) for _ in range(3))

    def create_color_square(self, size: int, color: Tuple[int, int, int]) -> Image.Image:
        """
        Create a solid color square image.

        Args:
            size: Size of the square image (width = height)
            color: RGB color tuple

        Returns:
            PIL Image object
        """
        try:
            # Create a new image with the specified color
            img = Image.new('RGB', (size, size), color=color)
            return img
        except Exception as e:
            raise RuntimeError(f"Failed to create image: {str(e)}")

    def save_image(self, image: Image.Image, filename: str) -> None:
        """
        Save the image to the output directory.

        Args:
            image: PIL Image object to save
            filename: Name of the file to save (including extension)
        """
        try:
            filepath = f"{self.output_dir}/{filename}"
            image.save(filepath)
            print(f"Image saved: {filepath}")
        except Exception as e:
            print(f"Error saving image: {str(e)}")

    def generate_image(self, size: int = 500, filename: str = 'random_square.png') -> None:
        """
        Generate and save a random color square image.

        Args:
            size: Size of the square image (default: 500px)
            filename: Output filename (default: random_square.png)
        """
        color = self.generate_random_color()
        image = self.create_color_square(size, color)
        self.save_image(image, filename)

if __name__ == "__main__":
    # Example usage
    generator = ImageGenerator()
    generator.generate_image(size=300, filename='example_square.png')