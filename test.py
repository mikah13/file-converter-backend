from PIL import Image
import os

# Specify the dimensions of the collage
collage_width = 800
collage_height = 600

# Create a blank canvas for the collage
collage = Image.new("RGB", (collage_width, collage_height))

# List of image paths
image_paths = [
    "./test/pic1.png",
    "./test/pic2.png",
    "./test/pic3.png",
    "./test/pic4.png",
]

# Calculate the dimensions of each image in the collage
num_images = len(image_paths)
image_width = collage_width // num_images
image_height = collage_height

# Open and paste each image onto the collage
x = 0
for image_path in image_paths:
    image = Image.open(image_path)

    # Resize the image while maintaining its aspect ratio
    image.thumbnail((image_width, image_height))

    # Paste the resized image onto the collage
    collage.paste(image, (x, 0))

    x += image_width

# Save the collage
collage.save("image_collage.jpg")

# Show the collage
collage.show()
