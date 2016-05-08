import os
from PIL import ImageTk, Image

class TrialImage:
    def __init__(self,
                 width_pixels,
                 height_pixels,
                 centre_x_pixels,
                 centre_y_pixels,
                 duration_seconds,
                 file_path):
        self.width = width_pixels
        self.height = height_pixels
        self.centre_x = centre_x_pixels
        self.centre_y = centre_y_pixels
        self.duration = duration_seconds
        self.file_path = os.path.abspath(file_path)

        image = Image.open(self.file_path)
        image = image.resize((self.height, self.width), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(image)