import argparse

import os

from Events import Scheduler
from GuiFacade import GuiFacade
from ExperimentLoader import ExperimentLoader

def parse_command_line(): # TODO: may be eliminated once the GUI is used...
    parser = argparse.ArgumentParser()
    parser.add_argument('--experimentFile', help='path to the file with the experiment description', required=True)
    args = parser.parse_args()
    return args.experimentFile


# Stupid trick to start the gui before doing work, to display error messages, if the need be, while initializing things.
gui = GuiFacade()
def start_experiment():
    loader = ExperimentLoader()
    filename = gui.select_file()
    events = loader.load(filename, gui)
    scheduler = Scheduler(events, gui)


def main():
    gui.register_event(0, start_experiment)
    gui.main_loop()

if __name__ == "__main__":
    main()