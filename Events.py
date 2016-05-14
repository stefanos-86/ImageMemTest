# Here we have the classes to deal with the scheduling of events.
# Constructors can be invoked by the end users (to program the experiments),
# therefore the parameter validation must be merciless.


class Event(object):
    """ Base of all the events, and also the no-op events."""
    def __init__(self):
        self.gui = None  # All the events have to register with and manipulate the GUI.
                         # But it can't be in the constructor signature because I don't want the client
                         # to bother with such details.

    def attach_gui(self, gui):
        self.gui = gui


class DelayedEvent(Event):
    """ This event has to be scheduled after a certain time. """
    def __init__(self, delay_milliseconds):
        super(DelayedEvent, self).__init__()

        assert isinstance(delay_milliseconds, (int, long)), "Delay must be integer -> " + str(delay_milliseconds)
        assert delay_milliseconds >= 0, "Delay must be 0 or positive -> " + str(delay_milliseconds)

        self.delay = delay_milliseconds

    def register(self, back_to_scheduler):
        self.gui.register_event(self.delay, back_to_scheduler)


class OnKeyEvent(Event):
    """ This event waits for a key press. """
    def __init__(self, key):
        super(OnKeyEvent, self).__init__()
        self._validate_key(key)
        self.key = key

    def _validate_key(self, key):
        supported_special_bindings = "<space> <Return> <Key>"

        assert isinstance(key, basestring), "Key must be a string (like \"a\", with the quotes) -> " + str(key)

        key_length = len(key)
        if key_length > 1 and "<" in key:
            assert key in supported_special_bindings, "Invalid special key -> [" + key + "]" \
                                                       " - available: " + supported_special_bindings
        else:
            assert len(key) == 1, "Normal key must be one symbol (like \"a\") -> [" + key + "]"
        assert key != " ", "Use \"<space>\", not a literal blank char."

    def register(self, back_to_scheduler):
        self.gui.bind_key(self.key, back_to_scheduler)

    def _remove_key_binding(self):
        """ Some events may need to remove the key binding at the end of happen(). """
        self.gui.free_key(self.key)


class ChangeBackgroundColor(DelayedEvent):
    """ Orders the gui to change the background color. """
    def __init__(self,r, g, b):
        super(ChangeBackgroundColor, self).__init__(0)  # 0 delay: this is immediate.
        self.rgb_triplet = (r, g, b)

    def happen(self):
        r, g, b = self.rgb_triplet
        self.gui.background_color(r, g, b)


class PressKeyToContinue(OnKeyEvent):
    """ Does nothing until the user press the specified key. """
    def __init__(self, key_to_wait):
        super(PressKeyToContinue, self).__init__(key_to_wait)

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


