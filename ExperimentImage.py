# Class to manipulate an actual image that the scientist want to use in the experiment.
#
# Do not forget that (0, 0) is the top left corner of the screen!

import os
import math

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

    def size(self):
        return (self.tk_image.width(), self.tk_image.height())

    def _not_in_screen_error(self, border, distance):
        return "Image " + self.id + " exits the screen on the " + border + " by " + str(abs(distance)) + " pixels."


class ImageCollection:
    def __init__(self, gui, base_path):
        max_x, max_y = gui.screen_size()  # Needed for image validation.
        self.max_x = max_x
        self.max_y = max_y
        self.base_path = base_path  # Here is where we can find the images.
        self.images = []  # The actual collection of images.
        self.gui_markers = [] # Opaque handles to the markers, to be provided by the GUI.
        self.marker_images = [] # Actual images - to be stored here to ensure they don't disappear.

    def load_image(self, name, centre_x, centre_y):
        new_image = self._load_single_image(name, centre_x, centre_y)
        self.images.append(new_image)
        return new_image

    def create_markers(self, marker_image_name):
        full_path = os.path.join(self.base_path, marker_image_name)
        marker_image = ExperimentImage(0, 0, full_path)  # Do not use the load image method: we don't know how big the
        size_x, size_y = marker_image.size()             # image is, can't position it to pass validation.

        # geometry looks like this:
        #
        #  |----------|   full screen
        #     |----|      row in the middle
        #  |--|    |--|   each side is 1/2 of the (screen - row) space
        needed_markers = len(self.images)  # One per each image.
        actual_row_length = size_x * needed_markers
        if actual_row_length > self.max_x:
            raise Exception("Too many markers to fit on the bottom of the screen.")
        left = (self.max_x - actual_row_length) / 2
        top = self.max_y - size_y # Bottom of the screen
        centre_x = left + size_x / 2
        centre_y = top + size_y / 2

        images = []
        for image in self.images:
            new_marker = self._load_single_image(marker_image_name, centre_x, centre_y)
            images.append(new_marker)
            centre_x += size_x

        self.marker_images = images
        return images


    def _load_single_image(self, name, centre_x, centre_y):
        full_path = os.path.join(self.base_path, name)
        new_image = ExperimentImage(centre_x, centre_y, full_path)
        new_image.validate(self.max_x, self.max_y)
        return new_image

    def find_distances(self):
        if len(self.marker_images) == 0:
            raise Exception("Can't compute result with no markers.")

        result = []
        for image in self.images:
            marker = self._find_closest_marker(image)
            result.append( {image.id, self._distance(image, marker) } )
            self.gui_markers.remove(marker)  # Avoid pathological cases like all the marker on a single image.
        return result


    def _find_closest_marker(self, image):
        min_distance = 1000000.0  # Assuming no one has a 1 000 000 pixel wide screen. TODO: find <climits>...
        closest_marker = None
        for marker in self.gui_markers:
            distance = self._distance(image, marker)
            if distance < min_distance:
                closest_marker = marker
                min_distance = distance
        return closest_marker


    def _distance(self, image, marker):
        size_x, size_y = self.marker_images[0].size()

        left, top = marker.position()
        marker_x = left + size_x / 2
        marker_y = top + size_y / 2

        img_x = image.centre_x
        img_y = image.centre_y

        delta_x = abs(img_x - marker_x)
        delta_y = abs(img_y - marker_y)

        return math.sqrt(delta_x * delta_x + delta_y * delta_y)
