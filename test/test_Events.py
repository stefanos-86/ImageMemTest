import unittest

import sys
sys.path.append("./..")

from Events import *
from ExperimentImage import ImageCollection


def mock_callback():
    pass


class MockGui():
    def __init__(self):
        self.delay = None
        self.callback = None
        self.key = None
        self.bg_color = None
        self.freed_key = None
        self.added_image = None
        self.removed_image = None
        self.draggable_image = None

    def register_event(self, delay, callback):
        self.delay = delay
        self.callback = callback

    def bind_key(self, key, callback):
        self.key = key
        self.callback = callback

    def background_color(self, r, g, b):
        self.bg_color = (r, g, b)

    def free_key(self, key):
        self.freed_key = key

    def screen_size(self):
        return (1000, 1000)

    def show_image(self, top, left, tk_image):
        self.added_image = tk_image
        return tk_image

    def remove_image(self, image_handle):
        self.removed_image = image_handle

    def show_draggable_image(self, top, left, tk_image):
        self.draggable_image = tk_image
        return tk_image


class MockMarker:
    def centre_position(self):
        return (0, 0)


class EventTest(unittest.TestCase):
    def test_attach_gui(self):
        mock_gui = MockGui
        event = ExperimentStep()
        event.attach_gui(mock_gui)
        self.assertEquals(mock_gui, event.gui)


class DelayedEventTest(unittest.TestCase):
    def test_construction(self):
        delay = 123
        event = DelayedExperimentStep(delay)
        self.assertEquals(delay, event.delay)

    def test_construnction__nonsensical_delay(self):
        delay = "Not a number."
        self.assertRaises(Exception, DelayedExperimentStep, delay)

    def test_construnction__negative_delay(self):
        self.assertRaises(Exception, DelayedExperimentStep, -1)

    def test_construction__float_delay(self):
        self.assertRaises(Exception, DelayedExperimentStep, 1.5)

    def test_register(self):
        delay = 123
        gui = MockGui()

        event = DelayedExperimentStep(delay)
        event.attach_gui(gui)

        event.register(mock_callback)

        self.assertEquals(delay, gui.delay)
        self.assertEquals(mock_callback, gui.callback)


class OnKeyEventTest(unittest.TestCase):
    def test_construction(self):
        key = "x"
        event = OnKeyExperimentStep(key)
        self.assertEquals(key, event.key)

    def test_construction__special_binding(self):
        key = "<Return>"
        event = OnKeyExperimentStep(key)
        self.assertEquals(key, event.key)

    def test_construction__nonsensical_key(self):
        key = 3874.83
        self.assertRaises(Exception, OnKeyExperimentStep, key)

    def test_construction__too_many_keys(self):
        key = "ab"
        self.assertRaises(Exception, OnKeyExperimentStep, key)

    def test_construction__incorrect_space(self):
        key = " "
        self.assertRaises(Exception, OnKeyExperimentStep, key)

    def test_construction__unsupported_special_bind(self):
        key = "<rubbish>"
        self.assertRaises(Exception, OnKeyExperimentStep, key)

    def test_register(self):
        key = "4"
        gui = MockGui()
        event = OnKeyExperimentStep(key)
        event.attach_gui(gui)

        event.register(mock_callback)

        self.assertEquals(key, gui.key)
        self.assertEquals(mock_callback, gui.callback)


class ChangeBackgroundColorTest(unittest.TestCase):
    def test_construction(self):
        event = ChangeBackgroundColor(1,2,3)
        self.assertEquals((1, 2, 3), event.rgb_triplet)

    def test_construction__invalid_rgb(self):
        self.assertRaises(Exception, ChangeBackgroundColor, -1, 2, 3)
        self.assertRaises(Exception, ChangeBackgroundColor, 256, 2, 3)
        self.assertRaises(Exception, ChangeBackgroundColor, "NaN", 2, 3)

    def test_happen(self):
        gui = MockGui()
        event = ChangeBackgroundColor(1,2,3)
        event.attach_gui(gui)

        event.happen()

        self.assertEqual((1, 2, 3), gui.bg_color)


class PressKeyToContinueTest(unittest.TestCase):
    def test_happen(self):
        key = "r"
        event = PressKeyToContinue(key)
        gui = MockGui()
        event.attach_gui(gui)

        event.happen()

        self.assertEquals(key, gui.freed_key)


class WaitTest(unittest.TestCase):
    def test_construction(self):
        wait_duration = 123

        event = Wait(wait_duration)

        self.assertEqual(wait_duration, event.delay)

    def test_happen(self):
        wait_duration = 123
        event = Wait(wait_duration)
        gui = MockGui()
        event.attach_gui(gui)

        event.happen()
        # No assertion possible. happen() is a no-op.


class ShowImageTest(unittest.TestCase):

    def test_attach_gui__invalid_image(self):
        event = ShowImage(1, 2, 3, "TestImage.jpg")
        gui = MockGui()
        self.assertRaises(Exception, event.attach_images, ImageCollection(gui, "."))

    # No other validation cases: it is delegated to the image.

    def test_register__shows_the_image(self):
        event = ShowImage(1, 200, 300, "TestImage.jpg")
        gui = MockGui()
        event.attach_images(ImageCollection(gui, "."))
        event.attach_gui(gui)

        event.register(mock_callback)

        self.assertEqual(event.image.tk_image, gui.added_image)

    def test_register__normal_delay(self):
        event = ShowImage(1, 200, 300, "TestImage.jpg")
        gui = MockGui()
        event.attach_images(ImageCollection(gui, "."))
        event.attach_gui(gui)

        event.register(mock_callback)

        self.assertEqual(1, gui.delay)

    def test_happen(self):
        event = ShowImage(1, 200, 300, "TestImage.jpg")
        gui = MockGui()
        event.attach_images(ImageCollection(gui, "."))
        event.attach_gui(gui)
        event.register(mock_callback)  # Emplace the gui handle to the image.

        event.happen()

        self.assertEqual(event.image.tk_image, gui.removed_image)


class ShowAllImagesTest(unittest.TestCase):
    def test_register(self):
        gui = MockGui()
        collection = ImageCollection(gui, ".")
        image = collection.load_image("TestImage.jpg", 100, 100)
        event = ShowAllImages(152)
        event.attach_images(collection)
        event.attach_gui(gui)

        event.register(mock_callback)

        self.assertEquals(image.tk_image, gui.added_image)

    def test_happen(self):
        gui = MockGui()
        collection = ImageCollection(gui, ".")
        image = collection.load_image("TestImage.jpg", 100, 100)
        event = ShowAllImages(152)
        event.attach_images(collection)
        event.attach_gui(gui)
        event.register(mock_callback)

        event.happen()

        self.assertEquals(image.tk_image, gui.removed_image)


class PrepareMarkersTest(unittest.TestCase):
    def test_happen(self):
        gui = MockGui()
        collection = ImageCollection(gui, ".")
        collection.load_image("TestImage.jpg", 100, 100)
        event = PrepareMarkers("TestMarker.jpg")
        event.attach_images(collection)
        event.attach_gui(gui)

        event.happen()

        self.assertIsNotNone(gui.draggable_image)


class ComputeResultTest(unittest.TestCase):
    def test_happen(self):
        gui = MockGui()
        collection = ImageCollection(gui, ".")
        collection.load_image("TestImage.jpg", 100, 100)
        collection.create_markers("TestMarker.jpg")
        collection.gui_markers.append(MockMarker())
        expected_file = "./TestOutput.txt"

        event = ComputeResult(expected_file)
        event.attach_images(collection)
        event.attach_gui(gui)
        event.happen()

        self.assertIsNotNone(open(expected_file, "r"))  # This event writes on a file, but is not master of the file format.
                                             # Assuring that the file exists is good enough.

class SchedulerTest(unittest.TestCase):
    def test_construction__enqueue_schedule_first_event(self):
        gui = MockGui()
        events = [ExperimentStep()]

        scheduler = Scheduler(events, gui)

        self.assertEquals(0, gui.delay)
        self.assertEquals(scheduler.schedule_event, gui.callback)

    def test_schedule_event(self):
        gui = MockGui()
        key = "r"
        event = PressKeyToContinue(key)
        event.attach_gui(gui)
        events = [event]
        scheduler = Scheduler(events, gui)

        scheduler.schedule_event()

        self.assertEqual(gui.callback, scheduler.do_event)  # When the event fires, the scheduler must be invoked to do
                                                            # some bookkeeping.
        self.assertEqual(key, gui.key)  # The event did its registration.

    def test_schedule_event__end_of_events(self):
        gui = MockGui()
        event = PressKeyToContinue("<Key>")
        event.attach_gui(gui)
        events = [event]

        scheduler = Scheduler(events, gui)
        scheduler.schedule_event()  # Use the only available event.

        scheduler.do_event()

        gui.callback = None  # Reset gui
        scheduler.schedule_event()

        self.assertIsNone(gui.callback) # No changes from the previous scheduling.

    def test_do_event(self):
        gui = MockGui()
        event1 = PressKeyToContinue("a")
        event2 = PressKeyToContinue("b")
        event1.attach_gui(gui)
        event2.attach_gui(gui)
        events = [event1, event2]

        scheduler = Scheduler(events, gui)
        scheduler.schedule_event()

        scheduler.do_event()
        self.assertEquals("a", gui.freed_key)  # Side effect of the event 1: it did run.
        self.assertEquals("b", gui.key)  # The next event has been registered.
