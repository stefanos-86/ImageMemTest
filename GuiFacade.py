# Facade in front of the Tkinter gui, with the "basic operations" I need.
# This module is coupled with Tkinter, and so not testable: keep it small.

import types

import Tkinter as tk

import tkFileDialog
import tkMessageBox

import sys

class GuiFacade:
    def __init__(self):
        window = tk.Tk()
        window.title("ImageMemoryTest")
        window.attributes("-fullscreen", True)

        self.window = window

        self.bind_key("<Escape>", self.quit_on_esc)

        tk.Tk.report_callback_exception = self._show_error

    def _show_error(self, *args):
        captured_exception, text, traceback_object = args
        tkMessageBox.showerror("Unrecoverable error", str(text) + "\n\n Press OK to close the program.")
        self.window.quit()

    def quit_on_esc(self, event):
        self.window.quit()

    def main_loop(self):
        self.window.mainloop()

    def background_color(self, r, g, b):
        background_color = self._color_rgb_to_hex(r, g, b)
        self.window.configure(background=background_color)

    def _color_rgb_to_hex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def register_event(self, when_milliseconds, what_callback):
        self.window.after(when_milliseconds, what_callback)

    def bind_key(self, key, what_callback):
        self.window.bind(key, what_callback)

    def free_key(self, key):
        self.window.unbind(key)

    def select_file(self):
        return tkFileDialog.askopenfilename()

    def screen_size(self):
        return (self.window.winfo_screenwidth(),
                self.window.winfo_screenheight())

    def show_image(self, top, left, tk_image):
        panel = tk.Label(self.window, image=tk_image)
        panel.place(x=left, y=top)
        return panel  # To be used as an opaque reference by the caller.

    def remove_image(self, image_handle):  # image_handle is the panel returned by show_image()
        image_handle.place_forget()

    def show_draggable_image(self, top, left, tk_image):
        panel = MobileLabel(self.window, tk_image)
        panel.place(x=left, y=top)
        return panel


class MobileLabel(tk.Label):
    def __init__(self, window, tk_image):
        #super(MobileLabel, self).__init__(window, image=tk_image) # Nope. tk.Label is old style class...
        tk.Label.__init__(self, window, image=tk_image)

        self.x = None
        self.y = None

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.on_motion)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.place(x=x, y=y)

    def position(self):
        """ Returns left and top! """
        return (self.winfo_rootx(), self.winfo_rooty())
