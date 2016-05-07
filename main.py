import Tkinter as tk
from PIL import ImageTk, Image


class ImageMemoryTest():
    def __init__(self):
        window = tk.Tk()
        window.title("ImageMemoryTest")
        window.attributes("-fullscreen", True)
        window.configure(background='white')

        window.bind("<Escape>", self.quit_on_esc)

        self.window = window

    def quit_on_esc(self, event):
        self.window.quit()

    def start(self):
        self.window.mainloop()


def main_loop():
    imt = ImageMemoryTest()
    imt.start()


   # path = "TulipanoJPEG100.jpg"

    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
  #  img = ImageTk.PhotoImage(Image.open(path))

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