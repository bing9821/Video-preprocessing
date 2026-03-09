'''LOGO CREATION'''

from matplotlib import pyplot as pt
import numpy as np
import cv2

# Define rgb color 
light_yellow = [255, 255, 153]
purple = [234, 155, 242]
light_purple = [243, 194, 234]
dark_purple = [196, 115, 210]

# Create a blank image with dimensions 11x12 and 3 color channels (RGB), initialized to white
logo = np.ones((16, 16, 3), dtype=np.uint8) 

# Background
logo[0:16, 0:16] = light_yellow
logo[0:2, 2:4] = purple
logo[2:4, 14:16] = purple
logo[13:15, 2:4] = purple
logo[15:16, 12:13] = purple
logo[11:12, 15:16] = purple
logo[9:10, 0:1] = purple

# Fill specific regions with the colors to form a heart shape
logo[3:4, 4:7] = dark_purple
logo[3:4, 9:12] = dark_purple

logo[4:5, 3:13] = dark_purple
logo[4:5, 4:5] = purple
logo[4:5, 5:7] = light_purple
logo[4:5, 9:12] = light_purple

logo[5:9, 2:14] = dark_purple
logo[5:9, 4:13] = light_purple
logo[5:9, 3:4] = purple
logo[8:9, 4:5] = purple

logo[9:10, 3:13] = dark_purple
logo[9:10, 4:6] = purple
logo[9:10, 6:12] = light_purple

logo[10:11, 4:12] = dark_purple
logo[10:11, 5:7] = purple
logo[10:11, 7:11] = light_purple

logo[11:12, 5:11] = dark_purple
logo[11:12, 6:8] = purple
logo[11:12, 8:10] = light_purple

logo[12:13, 6:10] = dark_purple
logo[12:13, 7:9] = purple

logo[13:14, 7:9] = dark_purple

# Define scale factor to make the image larger
scale_factor = 4

# Create a larger version of the logo
larger_logo = np.repeat(np.repeat(logo, scale_factor, axis=0), scale_factor, axis=1)

# Display the logo using matplotlib
# pt.imshow(logo)
# pt.title('Purple Heart Logo')
# pt.axis('off')  # Hide the axis
# pt.show()
pt.imsave("logo.png",larger_logo)