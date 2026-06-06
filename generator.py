import os
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import random

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DALLE_ENDPOINT = "https://api.openai.com/v1/images/generations"
RANDOM_COLOR_MODE = "random_color"
DALLE_MODE = "dalle"

def generate_image(prompt, mode=DALLE_MODE, output_path="output", file_name="generated_image"):
    """
    Generate an image based on the given prompt and mode.

    Args:
        prompt (str): The prompt to generate the image from.
        mode (str): The mode to use for image generation. Can be 'dalle' or 'random_color'.
        output_path (str): The path to save the generated image.
        file_name (str): The name of the generated image file.

    Returns:
        str: The path to the generated image file.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_path = os.path.join(output_path, f"{file_name}.png")

    try:
        if mode == DALLE_MODE:
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            image_data = generate_image_with_dalle(prompt)
        elif mode == RANDOM_COLOR_MODE:
            image_data = generate_random_color_image()
        else:
            raise ValueError(f"Invalid mode: {mode}")

        with open(file_path, "wb") as f:
            f.write(image_data)
        return file_path
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def generate_image_with_dalle(prompt):
    """
    Generate an image using OpenAI's DALL·E.

    Args:
        prompt (str): The prompt to generate the image from.

    Returns:
        bytes: The image data in bytes.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(DALLE_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    image_url = response.json()["data"][0]["url"]
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    return image_response.content

def generate_random_color_image():
    """
    Generate a random color image.

    Returns:
        bytes: The image data in bytes.
    """
    width, height = 1024, 1024
    image = Image.new("RGB", (width, height), color=get_random_color())
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()

def get_random_color():
    """
    Generate a random color.

    Returns:
        tuple: A tuple representing the RGB color.
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate images from prompts.")
    parser.add_argument("prompt", type=str, help="The prompt to generate the image from.")
    parser.add_argument("--mode", type=str, choices=[DALLE_MODE, RANDOM_COLOR_MODE], default=DALLE_MODE, help="The mode to use for image generation.")
    parser.add_argument("--output", type=str, default="output", help="The path to save the generated image.")
    parser.add_argument("--file_name", type=str, default="generated_image", help="The name of the generated image file.")

    args = parser.parse_args()
    generate_image(args.prompt, args.mode, args.output, args.file_name)