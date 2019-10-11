import imageio
from PIL import Image, ImageTk
import os

list_of_files = os.listdir(".//Radio//")
for x in list_of_files:
    updated_image = Image.open(".//Radio//" + x)
    updated_image = updated_image.resize((300, 250), Image.ANTIALIAS)
    updated_image.save(".//Radio//" + x)
