# TODO: deprecate!

import re
import os

from TrialImage import TrialImage


class Experiment:
    image_line = re.compile(" *([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+) +(.+)")

    def __init__(self, experiment_description, file_path):
        self.images = []
        self.text_description = experiment_description
        self.path = file_path

        self._parse_experiment_description()

    def _parse_experiment_description(self):
        for line in self.text_description.split("\n"):

            # Strip comments.
            comment_sign = "#"
            if comment_sign in line:
                line = line[0:line.find("#")].strip()

            # Skip empty lines.
            if len(line) > 0:
                elements = re.match(Experiment.image_line, line)

                if elements is None:
                    raise Exception("Unrecognized experiment line [" + str(line) + "]")

                width = int(elements.group(1))
                height = int(elements.group(2))
                centre_x = int(elements.group(3))
                centre_y = int(elements.group(4))
                duration = int(elements.group(5))
                path = str(elements.group(6))

                base_directory = os.path.dirname(self.path)
                real_image_path = os.path.join(base_directory, path)
                self.images.append(TrialImage(width, height, centre_x, centre_y, duration, real_image_path))

    @staticmethod
    def from_file(file_path):
        with open(file_path) as actual_file:
            experiment_description = actual_file.read()
            return Experiment(experiment_description, file_path)