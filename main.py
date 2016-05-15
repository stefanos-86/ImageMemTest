import argparse

import os

from Events import Scheduler
from GuiFacade import GuiFacade
from ExperimentLoader import ExperimentLoader


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', metavar="experiment_file",
                        help='path to the file with the experiment description', required=False)
    args = parser.parse_args()
    return args.e


def select_file():
    filename = parse_command_line()
    while filename is None or len(filename) == 0:  # Loop until we get something: we must have a file to read.
        filename = gui.select_file()
    return filename


# Stupid trick to start the gui before doing work, to display error messages, if the need be, while initializing things.
gui = GuiFacade()
def start_experiment():
    filename = select_file()
    loader = ExperimentLoader()
    events = loader.load(filename, gui)
    scheduler = Scheduler(events, gui)


def main():
    gui.register_event(0, start_experiment)
    gui.main_loop()

if __name__ == "__main__":
    main()