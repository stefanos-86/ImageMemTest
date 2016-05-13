import argparse

import os

from Experiment import Experiment

#Includes above this line may be useless.
from Events import ChangeBackgroundColor
from Events import PressKeyToContinue
from Events import Scheduler
from GuiFacade import GuiFacade
from ExperimentLoader import ExperimentLoader


class ImageMemoryTestRunner(): #Deprecated
    def __init__(self, experiment_file):


        self.window = window
        self.experiment = Experiment.from_file(os.path.abspath(experiment_file))

        event_time_milliseconds = 0
        for image in self.experiment.images:
            panel = tk.Label(window, image=image.tk_image)
            image.tk_panel = panel
            window.after(event_time_milliseconds, image.emplace)
            event_time_milliseconds += image.duration * 1000
            window.after(event_time_milliseconds, image.remove)




def main_loop(): # Unused, to be replaced by main()
    experiment_file = parse_command_line()
    imt = ImageMemoryTestRunner(experiment_file)
    imt.start()

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experimentFile', help='path to the file with the experiment description', required=True)
    args = parser.parse_args()
    return args.experimentFile

def main():
    gui = GuiFacade()
    loader = ExperimentLoader()
    events = loader.load(os.path.join("Demo", "ChangeColorOnKeyPress.txt"), gui)

    if events is not None:
        scheduler = Scheduler(events, gui)

        gui.main_loop()

if __name__ == "__main__":
    main()