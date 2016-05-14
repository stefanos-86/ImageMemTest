import unittest

import sys
sys.path.append("./..")

from ExperimentLoader import *


class MockGui():
    pass


class ExperimentLoaderTest(unittest.TestCase):
    def test_parse_input_line__nothing(self):
        loader = ExperimentLoader()

        events = loader.parse_input_file([], "filename", MockGui())

        self.assertEqual([], events)

    def test_parse_input_line__one_event(self):
        loader = ExperimentLoader()
        mock_file = ["ChangeBackgroundColor(0, 0, 255)"]

        events = loader.parse_input_file(mock_file, "filename", MockGui())

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], ChangeBackgroundColor)

    def test_parse_input_line__two_events(self):
        loader = ExperimentLoader()
        mock_file = ["ChangeBackgroundColor(0, 0, 255)", "PressKeyToContinue(\"a\")"]

        events = loader.parse_input_file(mock_file, "filename", MockGui())

        self.assertEqual(2, len(events))
        self.assertIsInstance(events[0], ChangeBackgroundColor)
        self.assertIsInstance(events[1], PressKeyToContinue)

    def test_parse_input_line__inline_comment(self):
        loader = ExperimentLoader()
        mock_file = ["ChangeBackgroundColor(0, 0, 255) # This is a comment."]

        events = loader.parse_input_file(mock_file, "filename", MockGui())

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], ChangeBackgroundColor)

    def test_parse_input_line__comment_line(self):
        loader = ExperimentLoader()
        mock_file = ["# This is a comment.", "ChangeBackgroundColor(0, 0, 255)"]

        events = loader.parse_input_file(mock_file, "filename", MockGui())

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], ChangeBackgroundColor)

    def test_parse_input_line__blank_line(self):
        loader = ExperimentLoader()
        mock_file = ["", "ChangeBackgroundColor(0, 0, 255)"]

        events = loader.parse_input_file(mock_file, "filename", MockGui())

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], ChangeBackgroundColor)

    def test_parse_input_line__blanks(self):
        loader = ExperimentLoader()
        mock_file = [" ", "ChangeBackgroundColor(0, 0, 255)"]

        events = loader.parse_input_file(mock_file, "filename", MockGui())

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], ChangeBackgroundColor)