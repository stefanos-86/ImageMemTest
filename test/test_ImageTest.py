import unittest

import sys
sys.path.append("./..")

from TrialImage import TrialImage


# Can not load images if tk is not initialized.
import Tkinter as tk
window = tk.Tk()

class TestImageTest(unittest.TestCase):
    def test_construction(self):
        img = TrialImage(1, 2, 3, 4, 5, "TestImage.jpg")
        self.assertEqual(1, img.width)
        self.assertEqual(2, img.height)
        self.assertEqual(3, img.centre_x)
        self.assertEqual(4, img.centre_y)
        self.assertEqual(5, img.duration)
        self.assertTrue("TestImage.jpg" in img.file_path)

        self.assertIsNotNone(img.tk_image)

    def test_construction__no_image_file(self):
        self.assertRaises(IOError, TrialImage, 1, 2, 3, 4, 5, "Does not exists.jpeg")