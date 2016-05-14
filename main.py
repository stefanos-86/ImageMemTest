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


def main():
    gui = GuiFacade()
    loader = ExperimentLoader()
    events = loader.load(os.path.join("Demo", "ChangeColorOnKeyPress.txt"), gui)
    scheduler = Scheduler(events, gui)
    gui.main_loop()

if __name__ == "__main__":
    main()