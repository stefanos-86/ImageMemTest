import argparse

import os

from Steps import Scheduler
from GuiFacade import GuiFacade
from ExperimentLoader import ExperimentLoader
from Elements import ImageCollection
from Elements import RecallTimer

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', metavar="experiment_file",
                        help='path to the file with the experiment description', required=False)
    args = parser.parse_args()
    return args.e


def select_file(gui):
    filename = parse_command_line()
    while filename is None or len(filename) == 0:  # Loop until we get something: we must have a file to read.
        filename = os.path.abspath(gui.select_file_open())
    return filename


# Stupid trick to start the gui before doing work, to display error messages, if the need be, while initializing things.
def start_experiment(gui):
    filename = select_file(gui)
    loader = ExperimentLoader()
    timer = RecallTimer()
    image_collection = ImageCollection(gui, os.path.dirname(filename))
    events = loader.load(filename, gui, image_collection, timer)
    scheduler = Scheduler(events, gui)


def main():
    gui = GuiFacade()
    start_experiment(gui)
    gui.main_loop()

if __name__ == "__main__":
    main()