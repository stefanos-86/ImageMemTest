# Class to manipulate an actual image that the scientist want to use in the experiment.
#
# Do not forget that (0, 0) is the top left corner of the screen!

import os

from PIL import ImageTk, Image


class ExperimentImage:  # Can't be just "Image" because that name is taken by a dependengcy.
    def __init__(self, centre_x_pixels, centre_y_pixels, filename):
        self.id = filename
        self.centre_x = centre_x_pixels
        self.centre_y = centre_y_pixels

        # Slight breach of the GUI encapsulation. This class "knows" that it has to use Tkinter images.
        self.tk_image = None
        self._load_image(filename)

        # Compute where the left/top corner goes (needed to verify if the image fits the screen and as coordinates
        # for the GUI). Notice that we do a integer division: may lose a pixel if the size is odd.
        self.left = centre_x_pixels - (self.tk_image.width()  / 2)
        self.top  = centre_y_pixels - (self.tk_image.height() / 2)

    def _load_image(self, filename):
        image = Image.open(filename)
        # image = image.resize((h, sw), Image.ANTIALIAS) Do NOT resize. The scientists prepared the image beforehand.
        self.tk_image = ImageTk.PhotoImage(image)

    def validate(self, max_x, max_y):
        # An image is good if it fits the screen.
        assert self.left >= 0, self._not_in_screen_error("left", self.left)
        assert self.top >= 0, self._not_in_screen_error("top", self.top)
        bottom = self.top + self.tk_image.height()
        right = self.left + self.tk_image.width()
        assert bottom <= max_x, self._not_in_screen_error("bottom", bottom - max_x)
        assert right <= max_y, self._not_in_screen_error("rigth", right - max_y)

    def _not_in_screen_error(self, border, distance):
        return "Image " + self.id + " exits the screen on the " + border + " by " + str(abs(distance)) + " pixels."


class ImageCollection:
    def __init__(self, gui, base_path):
        max_x, max_y = gui.screen_size()  # Needed for image validation.
        self.max_x = max_x
        self.max_y = max_y
        self.base_path = base_path  # Here is where we can find the images.
        self.images = []  # The actual collection of images.

    def load_image(self, name, centre_x, centre_y):
        full_path = os.path.join(self.base_path, name)
        new_image = ExperimentImage(centre_x, centre_y, full_path)
        new_image.validate(self.max_x, self.max_y)
        self.images.append(new_image)
        return new_image