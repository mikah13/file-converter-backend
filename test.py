from PIL import Image
import os

# Specify the dimensions of the collage
collage_width = 800
collage_height = 600

# Create a blank canvas for the collage
collage = Image.new('RGB', (collage_width, collage_height))

# List of image paths
image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]

# Open and paste each image onto the collage
x, y = 0, 0
for image_path in image_paths:
    image = Image.open(image_path)
    collage.paste(image, (x, y))
    
    # Update the x and y coordinates for the next image
    x += image.width
    if x >= collage_width:
        x = 0
        y += image.height

# Save the collage
collage.save("image_collage.jpg")

# Show the collage
collage.show()
