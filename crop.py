from PIL import Image
 
# Opens a image in RGB mode
im = Image.open('test/pic1.png')
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image
left = width / 2
top = 0
right = 3 *  width / 2 
bottom = height
 
# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))
 
# Shows the image in image viewer
im1.show()