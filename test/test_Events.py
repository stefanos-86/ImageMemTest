import unittest

import sys
sys.path.append("./..")

from Events import *


def mock_callback():
    pass


class MockGui():
    def __init__(self):
        self.delay = None
        self.callback = None

    def register_event(self, delay, callback):
        self.delay = delay
        self.callback = callback


class EventTest(unittest.TestCase):
    def test_attach_gui(self):
        mock_gui = MockGui
        event = Event()
        event.attach_gui(mock_gui)
        self.assertEquals(mock_gui, event.gui)


class DelayedEventTest(unittest.TestCase):
    def test_construction(self):
        delay = 123;
        event = DelayedEvent(delay)
        self.assertEquals(delay, event.delay)

    def test_construnction__nonsensical_delay(self):
        delay = "Not a number."
        self.assertRaises(Exception, DelayedEvent, delay)

    def test_construnction__negative_delay(self):
        self.assertRaises(Exception, DelayedEvent,  0)
        self.assertRaises(Exception, DelayedEvent, -1)

    def test_construction__float_delay(self):
        self.assertRaises(Exception, DelayedEvent, 1.5)

    def test_register(self):
        delay = 123
        gui = MockGui()

        event = DelayedEvent(delay)
        event.attach_gui(gui)

        event.register(mock_callback)

        self.assertEquals(delay, gui.delay)
        self.assertEquals(mock_callback, gui.callback)





