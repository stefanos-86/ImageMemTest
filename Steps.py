# Here we have the classes to deal with the scheduling of commands in the program.
# Constructors can be invoked by the end users (to program the experiments),
# therefore the parameter validation must be merciless.

import os

from Elements import ExperimentImage


class ExperimentStep(object):
    """ Base of all the steps (GUI events), and also the no-op action."""
    def __init__(self):
        self.gui = None  # All the commands have to register with and manipulate the GUI.
                         # But it can't be in the constructor signature because I don't want the client
                         # to bother with such details.
        self.images = None  # Similar to the gui, some actions need to interact with the whole image collection.
        self.recall_timer = None  # Same principle, with the object to time the duration of the experiment
                                  # (the time the user needs to recall the position of the images).

    def attach_gui(self, gui):
        self.gui = gui

    def attach_images(self, image_collection):
        self.images = image_collection

    def attach_recall_timer(self, recall_timer):
        self.recall_timer = recall_timer


class DelayedExperimentStep(ExperimentStep):
    """ This event has to be scheduled after a certain time. """
    def __init__(self, delay_milliseconds):
        super(DelayedExperimentStep, self).__init__()

        assert isinstance(delay_milliseconds, (int, long)), "Delay must be integer -> " + str(delay_milliseconds)
        assert delay_milliseconds >= 0, "Delay must be 0 or positive -> " + str(delay_milliseconds)

        self.delay = delay_milliseconds

    def register(self, back_to_scheduler):
        self.gui.register_event(self.delay, back_to_scheduler)


class OnKeyExperimentStep(ExperimentStep):
    """ This event waits for a key press. """
    def __init__(self, key):
        super(OnKeyExperimentStep, self).__init__()
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


class ChangeBackgroundColor(DelayedExperimentStep):
    """ Orders the gui to change the background color. """
    def __init__(self,r, g, b):
        super(ChangeBackgroundColor, self).__init__(0)  # 0 delay: this is immediate.

        assert isinstance(r, (int, long))and isinstance(g, (int, long)) and isinstance(b, (int, long)), \
                                                                       "R, g or b must be integers."
        assert r >= 0 and g >= 0 and b >= 0, "r, g and b must be 0 or positive."
        assert r <= 255 and g <= 255 and b <= 255, "r, g or b can't be bigger than 255."

        self.rgb_triplet = (r, g, b)

    def happen(self):
        r, g, b = self.rgb_triplet
        self.gui.background_color(r, g, b)


class PressKeyToContinue(OnKeyExperimentStep):
    """ Does nothing until the user press the specified key. """
    def __init__(self, key_to_wait):
        super(PressKeyToContinue, self).__init__(key_to_wait)
        # Key validated by the superclass.

    def happen(self):
        self._remove_key_binding()


class Wait(DelayedExperimentStep):
    """ Blocks the evnt processing until the time has passed. """
    def __init__(self, wait_milliseconds):
        super(Wait, self).__init__(wait_milliseconds)

    def happen(self):
        pass  # Do nothing. We just had to wait.


class ShowImage(DelayedExperimentStep):
    def __init__(self, how_long_milliseconds, centre_x_pixels, centre_y_pixels, filename):
        super(ShowImage, self).__init__(how_long_milliseconds)
        self.image_gui_handle = None
        self.image = None
        self.centre_x = centre_x_pixels
        self.centre_y = centre_y_pixels
        self.image_name = filename

    def attach_images(self, image_collection):
        super(ShowImage, self).attach_images(image_collection)
        self.image = image_collection.add_image(self.image_name, self.centre_x, self.centre_y)

    def register(self, back_to_scheduler):
        super(ShowImage, self).register(back_to_scheduler)  # Normal registration to call happen() at the right time.
        # The event starts now: show the image immediately.
        self.image_gui_handle = self.gui.show_image(self.image.top, self.image.left, self.image.tk_image)

    def happen(self):
        self.gui.remove_image(self.image_gui_handle)


class ShowAllImages(DelayedExperimentStep):
    def __init__(self, for_how_long):
        super(ShowAllImages, self).__init__(for_how_long)
        self.handles = []

    def register(self, back_to_scheduler):
        super(ShowAllImages, self).register(back_to_scheduler)
        # The event starts now: loop to show all images.
        for image in self.images.images:
            new_handle = self.gui.show_image(image.top, image.left, image.tk_image)
            self.handles.append(new_handle)

    def happen(self):
        for image in self.handles:
            self.gui.remove_image(image)


class ShowAllMarkers(DelayedExperimentStep):
    def __init__(self, for_how_long, marker_image):
        super(ShowAllMarkers, self).__init__(for_how_long)
        self.placeholder_handles = []
        self.placeholder_image_name = marker_image
        self.placeholder_images = []  # Must keep a reference to the images somewhere.
                                      # Tk does not keep it, and the images disappear otherwise.

    def register(self, back_to_scheduler):
        super(ShowAllMarkers, self).register(back_to_scheduler)
        for image in self.images.images:
            same_centre_x, same_centre_y = image.centre_position()
            placeholder = self.images.create_image(self.placeholder_image_name, same_centre_x, same_centre_y)
            placeholder_handle = self.gui.show_image(placeholder.top, placeholder.left, placeholder.tk_image)
            self.placeholder_handles.append(placeholder_handle)
            self.placeholder_images.append(placeholder)

    # Nothing in happen(): the coniguration must stay on for the duration of the experiment.


class ShowInstructions(OnKeyExperimentStep):
    def __init__(self, key_to_continue, instruction_image_file):
        super(ShowInstructions, self).__init__(key_to_continue)
        self.instruction_image = None  # To keep the image in memory, or it won't be displayed.
        self.instruction_image_gui_handle = None
        self.instruction_image_file = instruction_image_file

    def register(self, back_to_scheduler):
        super(ShowInstructions, self).register(back_to_scheduler)  # To have the key binding.
        centre_x, centre_y =self._screen_centre()
        self.instruction_image = self.images.create_image(self.instruction_image_file, centre_x, centre_y)
        self.instruction_image_gui_handle = self.gui.show_image(self.instruction_image.top, self.instruction_image.left,
                                                                self.instruction_image.tk_image)

    def happen(self):
        self._remove_key_binding()
        self.gui.remove_image(self.instruction_image_gui_handle)

    def _screen_centre(self):
        centre_x, centre_y = self.gui.screen_size()
        centre_x /= 2
        centre_y /= 2
        return centre_x, centre_y


class PrepareMarkers(DelayedExperimentStep):
    def __init__(self, marker_image, timing_option):
        super(PrepareMarkers, self).__init__(0)  # Immediate event.
        self.marker_image = marker_image
        self.start_timer_immediately = None  # To be set by the below call.
        self.decode_timing_option(timing_option)

    def happen(self):
        marker_handles = self.images.create_markers(self.marker_image)
        for handle in marker_handles:
            gui_handle = self.gui.show_draggable_image(handle.top, handle.left, handle.tk_image,
                                                       self.recall_timer.start_once)
            self.images.gui_markers.append(gui_handle)  # Store them for other events usage.

        # The markers are ready: if the user wants to count from this moment, start the clock.
        # The callback on the images may try to start it again, but the timer will only react on the 1st call.
        if self.start_timer_immediately:
            self._start_timer()

    def _start_timer(self):
        self.recall_timer.start_once()

    def decode_timing_option(self, timing_option):
        immediate = "immediate timing"
        on_drag = "time on marker movement"

        if timing_option != immediate and timing_option != on_drag:
            raise Exception("Bad timing option " + timing_option +
                            " (should be \"" + immediate + "\" or \"" + on_drag + "\").")

        self.start_timer_immediately = timing_option == immediate



class ComputeResult(DelayedExperimentStep):
    def __init__(self, result_file):
        super(ComputeResult, self).__init__(0)  # Immediate.
        self.output_file = result_file

    def happen(self):
        self.recall_timer.experiment_complete()

        distances = self.images.find_distances()
        with open(self.output_file, "w") as result_file:
            distances[0].header(result_file)  # There must be at least one result, no array overflow.
            for result in distances:
                result.dump(result_file)
            self.recall_timer.dump(result_file)


class Scheduler:
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


