# Here we have the classes to deal with the scheduling of events.


class Event(object):
    """ Base of all the events, and also the no-op events."""
    def __init__(self, gui):
        self.gui = gui  # All the events have to register with and manipulate the GUI.

    def happen(self):
        """ Does nothing. """
        pass

    def onKey(self):
        print "base"
        return False


class BackgroundColorEvent(Event):
    """ Orders the gui to change the background color. """
    def __init__(self, gui, rgb_triplet):
        super(BackgroundColorEvent, self).__init__(gui)
        self.rgb_triplet = rgb_triplet

    def happen(self):
        r, g, b = self.rgb_triplet
        self.gui.background_color(r, g, b)



class PressAKeyToContinueEvent(Event):
    """ Does nothing until the user press the specified key. """
    def __init__(self, gui, key_to_wait):
        super(PressAKeyToContinueEvent, self).__init__(gui)
        self.key_to_wait = key_to_wait

        #self.gui.bind_key(self.key_to_wait, self.happen)

    def onKey(self):
        print "derivato "
        return True

    def happen(self):
        self.gui.free_key(self.key_to_wait)



class Scheduler():
    """ The scheduler has the list of all the steps to do.
        It registers with the GUI to be called on GUI events.
        When it is called, it fires the next event in the list, registers again for callback etc. """
    def __init__(self, events, gui):
        self.events = events
        self.event_iterator = 0
        self.event_end = len(events)

        self.gui = gui
        self.gui.register_event(0, self.schedule_event)  # Schedule immediately the 1st event of the list.

    def schedule_event(self):
        print "--------sched"
        if self.event_iterator >= self.event_end:
            return  # Do nothing, we are at the end of the script.

        kevent = self._current_event().onKey()
        print kevent
        if kevent:  # Apply polimorphism here...
            self.gui.bind_key(self._current_event().key_to_wait, self.do_event)
            print "on key"
        else:
            self.gui.register_event(0, self.do_event)
            print "registered"

    def do_event(self, event_from_gui=None):
        print "--------do"
        self._current_event().happen()  # Perform the scheduled action.

        self.event_iterator += 1        # Advance to the next.

        self.schedule_event()  # Put another one in the pipe.


    def _current_event(self):
        return self.events[self.event_iterator]


