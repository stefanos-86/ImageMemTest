# Here we have the classes to deal with the scheduling of events.


class Event(object):
    """ Base of all the events, and also the no-op events."""
    def __init__(self, gui):
        self.gui = gui  # All the events have to register with and manipulate the GUI.

    def happen(self):
        """ Does nothing. """
        pass


class DelayedEvent(Event):
    """ This event has to be scheduled after a certain time. """
    def __init__(self, gui, delay):
        super(DelayedEvent, self).__init__(gui)
        self.delay = delay

    def register(self, back_to_scheduler):
        self.gui.register_event(self.delay, back_to_scheduler)


class OnKeyEvent(Event):
    """ This event waits for a key press. """
    def __init__(self, gui, key):
        super(OnKeyEvent, self).__init__(gui)
        self.key = key

    def register(self, back_to_scheduler):
        self.gui.bind_key(self.key, back_to_scheduler)

    def _remove_key_binding(self):
        """ To be called at the end of happen() """  # TODO: consider a generic "unregister", but it makes no sense for DelayEvents.
        self.gui.free_key(self.key)


class ChangeBackgroundColor(DelayedEvent):
    """ Orders the gui to change the background color. """
    def __init__(self, gui, rgb_triplet):
        super(ChangeBackgroundColor, self).__init__(gui, 0)  # 0 Deleay: this is immediate.
        self.rgb_triplet = rgb_triplet

    def happen(self):
        r, g, b = self.rgb_triplet
        self.gui.background_color(r, g, b)


class PressKeyToContinue(OnKeyEvent):
    """ Does nothing until the user press the specified key. """
    def __init__(self, gui, key_to_wait):
        super(PressKeyToContinue, self).__init__(gui, key_to_wait)

    def happen(self):
        self._remove_key_binding()


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
        if self.event_iterator >= self.event_end:
            return  # Do nothing, we are at the end of the script.

        self._current_event().register(self.do_event)  # The event should not be called directly.
                                                       # Its trigger must re-call the scheduler.

    def do_event(self, event_from_gui=None):  # Event_from_gui is received in case of key presses.
        self._current_event().happen()  # Perform the scheduled action.

        self.event_iterator += 1        # Advance to the next.

        self.schedule_event()           # Put another one in the pipe.


    def _current_event(self):
        return self.events[self.event_iterator]


