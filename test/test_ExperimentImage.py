import unittest

import sys
sys.path.append("./..")

from ExperimentImage import ExperimentImage

from GuiFacade import GuiFacade
g = GuiFacade()  # Must initialize TK to load the real images.


class ExperimentImageTest(unittest.TestCase):
    def test_construction__load_real_jpeg(self):
        img = ExperimentImage(0, 0, "TestImage.jpg")

        self.assertIsNotNone(img.tk_image)

    def test_construction__remember_saved_data(self):
        img = ExperimentImage(1, 2, "TestImage.jpg")
        self.assertEqual("TestImage.jpg", img.id)
        self.assertEqual(1, img.centre_x)
        self.assertEqual(2, img.centre_y)

    def test_construction__compute_left_top(self):
        test_image_side = 192
        img = ExperimentImage(10, 200, "TestImage.jpg")

        self.assertEqual(-86, img.left)
        self.assertEqual(104, img.top)


    def test_validate__fits(self):
        test_image_side = 192  # Known from measurement. Notice that can be divided by 2.
        img = ExperimentImage(test_image_side/2, test_image_side/2, "TestImage.jpg")
        img.validate(test_image_side, test_image_side)  # The screen is exactly as big as the image.
        # No assertion needed. If the image is not good, there would be an exception.

    def test_validate__exits_left(self):
        test_image_side = 192
        img = ExperimentImage(test_image_side/2 - 1, test_image_side/2, "TestImage.jpg")  # 1 pixel too to the left.

        self.assertRaises(Exception, img.validate, 1000, 1000)

    def test_validate__exits_right(self):
        test_image_side = 192
        img = ExperimentImage(1000, test_image_side / 2, "TestImage.jpg")  # Centered on the border.

        self.assertRaises(Exception, img.validate, 1000, 1000)

    def test_validate__exits_top(self):
        test_image_side = 192
        img = ExperimentImage(500, test_image_side / 2 - 1 , "TestImage.jpg")  # 1 pixel too high

        self.assertRaises(Exception, img.validate, 1000, 1000)

    def test_validate__exits_bottom(self):
        test_image_side = 192
        img = ExperimentImage(test_image_side / 2, test_image_side / 2, "TestImage.jpg")

        self.assertRaises(Exception, img.validate, test_image_side, test_image_side - 1)  # Screen is 1 pixel too short.

