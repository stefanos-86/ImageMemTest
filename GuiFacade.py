# Facade in front of the Tkinter gui, with the "basic operations" I need.
# This module is coupled with Tkinter, and so not testable: keep it small.

import Tkinter as tk

class GuiFacade:
    def __init__(self):
        window = tk.Tk()
        window.title("ImageMemoryTest")
        window.attributes("-fullscreen", True)
        window.configure(background='white')

        window.bind("<Escape>", self.quit_on_esc)

        self.window = window

    def quit_on_esc(self, event):
        self.window.quit()

    def main_loop(self):
        self.window.mainloop()