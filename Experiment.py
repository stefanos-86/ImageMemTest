import re

from TrialImage import TrialImage

class Experiment:
    image_line = re.compile("([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+) +(.+)")

    def __init__(self, experiment_description):
        self.images = []
        self.textDescription = experiment_description

        self._parse_experiment_description()

    def _parse_experiment_description(self):
        for line in self.textDescription.split("\n"):
            elements = re.match(Experiment.image_line, line)

            if elements is None:
                raise Exception("Unrecognized experiment line [" + str(line) + "]")

            width = int(elements.group(1))
            heigth = int(elements.group(2))
            centre_x = int(elements.group(3))
            centre_y = int(elements.group(4))
            duration = int(elements.group(5))
            path = str(elements.group(6))

            self.images.append(TrialImage(width, heigth, centre_x, centre_y, duration, path))

