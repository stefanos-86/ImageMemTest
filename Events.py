# Here we have the classes to deal with the scheduling of events.


class Event(object):
    """ Base of all the events, and also the no-op events."""
    def happen(self):
        """ Does nothing. """
        pass

    def register(self, gui):
        """ Tells the GUI when to activate this event. """
        gui.register_event(0, self.happen)  # TODO: durations!

class BackgroundColorEvent(Event):
    """ Orders the gui to change the background color. """
    def __init__(self, gui, rgb_triplet):
        super(BackgroundColorEvent, self).__init__()
        self.gui = gui
        self.rgb_triplet = rgb_triplet

    def happen(self):
        r, g, b = self.rgb_triplet
        self.gui.background_color(r, g, b)
