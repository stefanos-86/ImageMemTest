# This file has the classes to represent all the objects involved in the experiment,
# like images, collections of images, distances... I will put there the timer too.
#
# Do not forget that (0, 0) is the top left corner of the screen!
#

import os
import math
import time
import datetime

from PIL import ImageTk, Image


class ExperimentImage:  # Can't be just "Image" because that name is taken by a dependency.
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

    def centre_position(self):
        """ Keep it consistent with the gui markers. """
        return (self.centre_x, self.centre_y)


class ImageCollection:
    def __init__(self, gui, base_path):
        max_x, max_y = gui.screen_size()  # Needed for image validation.
        self.max_x = max_x
        self.max_y = max_y
        self.base_path = base_path  # Here is where we can find the images.
        self.images = []  # The actual collection of images.
        self.gui_markers = [] # Opaque handles to the markers, to be provided by the GUI.
        self.marker_images = [] # Actual images - to be stored here to ensure they don't disappear.

    def add_image(self, name, centre_x, centre_y):
        new_image = self.create_image(name, centre_x, centre_y)
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
        top = self.max_y - size_y  # Bottom of the screen
        centre_x = left + size_x / 2
        centre_y = top + size_y / 2

        images = []
        for image in self.images:
            new_marker = self.create_image(marker_image_name, centre_x, centre_y)
            images.append(new_marker)
            centre_x += size_x

        self.marker_images = images
        return images

    def create_image(self, name, centre_x, centre_y):
        """ Factory method for the images - ensure vailidity with respect to the screen. """
        full_path = os.path.join(self.base_path, name)
        new_image = ExperimentImage(centre_x, centre_y, full_path)
        new_image.validate(self.max_x, self.max_y)
        return new_image

    def find_distances(self):
        if len(self.marker_images) == 0:
            raise Exception("Can't compute result with no markers.")
            # This triggers if the PrepareMarkers event was not called before.

        result = []
        for image in self.images:
            marker = self._find_closest_marker(image)
            result.append(
                DecoratedDistance(
                    self._distance(image, marker),
                    image.centre_position(),
                    marker.centre_position(),
                    image.id )
            )
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
        marker_x, marker_y = marker.centre_position()
        img_x, img_y = image.centre_position()

        delta_x = abs(img_x - marker_x)
        delta_y = abs(img_y - marker_y)

        return math.sqrt(delta_x * delta_x + delta_y * delta_y)


class DecoratedDistance:
    """ Simple data object to keep togheter the data of the results of interest. """
    def __init__(self, distance, image_centre, marker_centre, image_id):
        self.distance = distance
        self.image_centre = image_centre
        self.marker_centre = marker_centre
        self.image_id = image_id

        # Screens reasonably top at 1500 pixels, more or less.
        # Pixel fields are accordingly 6 chars wide, and couples twice as big (bigger than needed).
        # In some cases we have to account for formatting (e.g. the "( ,)" chars in a couple).
        # IDs may be unlimited.
        self.distance_line_format = "{distance:>6} {image_centre:>16} {marker_centre:>16} {image_id}\n"

    def dump(self, output_file):
        """ Assumes that the file is already opened. """
        attributes = self.__dict__
        attributes["distance"] = int(attributes["distance"])  # Truncate decimals.
        self._dump_fields(output_file, attributes)

    def header(self, output_file):
        """ Assumes that the file is already opened. """
        field_names = {}
        for key in self.__dict__:
            field_names[key] = key

        field_names["distance"] = "dist"  # Truncate long name (can't rely on format - in dump this is a number).
        self._dump_fields(output_file, field_names)

    def _dump_fields(self, output_file, dictionary):
        filled_text = self.distance_line_format.format(**dictionary)
        output_file.write(filled_text)


class RecallTimer:
    """ Class to record the amount of time. """
    # I can only find "how to time the execution of code"-type of tips on the web, but it should do.
    # Precision requirement is the second, but on a possibly long time (several minutes).
    # I assume that the clock won't go back during an experiment (and don't care for leap seconds).

    def __init__(self):
        self.experiment_duration_seconds = -1  # Obvious bad value.
        self.start_time = None
        self.end_time = None

    def markers_placed(self):
        self.start_time = time.time()

    def experiment_complete(self):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.experiment_duration_seconds = int(duration)  # Brutal truncation.

    def dump(self, output_file):
        text = "Start:    {start_time}\n" \
               "End:      {end_time}\n" \
               "Duration: {experiment_duration_seconds} seconds"

        formatted_times = \
            {
                "start_time" : self._to_date(self.start_time),
                "end_time": self._to_date(self.end_time),
                "experiment_duration_seconds": self.experiment_duration_seconds
            }

        output_file.write(text.format(**formatted_times))

    def _to_date(self, unix_time):
        return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
