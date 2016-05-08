import argparse
import Tkinter as tk
import os

from Experiment import Experiment


class ImageMemoryTestRunner():
    def __init__(self, experiment_file):
        window = tk.Tk()
        window.title("ImageMemoryTest")
        window.attributes("-fullscreen", True)
        window.configure(background='white')

        window.bind("<Escape>", self.quit_on_esc)

        self.window = window
        self.experiment = Experiment.from_file(os.path.abspath(experiment_file))

    def quit_on_esc(self, event):
        self.window.quit()

    def start(self):
        self.window.mainloop()



def main_loop():
    experiment_file = parse_command_line()
    imt = ImageMemoryTestRunner(experiment_file)
    imt.start()

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experimentFile', help='path to the file with the experiment description', required=True)
    args = parser.parse_args()
    return args.experimentFile


    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
  #  panel = tk.Label(window, image=img)

   # def hideImage():
   #     panel.pack_forget()

    # The Pack geometry manager packs widgets in rows or columns.
   # panel.pack(side="bottom", fill="both", expand="yes")

    #window.after(2000, hideImage)
    #window.after(3000, hideImage)

    # Start the GUI



if __name__ == "__main__":
    main_loop()