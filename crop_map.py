"""
This file can help with creating the map file.

It crops the image
"""

# Importing Image class from PIL module
from PIL import Image
 
# Opens a image in RGB mode
im = Image.open("data/map/catalunya.tiff")
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image
left = 5000
top = 5000
right = 8000
bottom = 8000
 
# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))
 
# Shows the image in image viewer
im1.show()

im1.save("result.tiff")