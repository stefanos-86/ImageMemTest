import unittest

import sys
sys.path.append("./..")

from ExperimentImage import ExperimentImage
from ExperimentImage import ImageCollection


from GuiFacade import GuiFacade
gui = GuiFacade()  # Must initialize TK to load the real images.

class MockGui(GuiFacade):  # Subclass so we get the real loading methods, but we can mock what we need.
    def screen_size(self):
        return (1000, 1000)


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

    def test_size(self):
        img = ExperimentImage(0, 0, "TestMarker.jpg")
        self.assertEquals((64, 64), img.size())

    def test_centre_position(self):
        img = ExperimentImage(10, 230, "TestMarker.jpg")
        self.assertEquals((10, 230), img.centre_position())


class TestImageCollection(unittest.TestCase):
    def test_load_image(self):
        images = ImageCollection(MockGui(), ".")

        image = images.load_image("TestImage.jpg", 100, 100)

        self.assertIsNotNone(image)
        self.assertEquals(1, len(images.images))
        self.assertEquals(image, images.images[0])

    def test_load_image__invalid_image(self):
        images = ImageCollection(MockGui(), ".")

        self.assertRaises(Exception, images.load_image, "TestImage.jpg", 1000, 100)

    def test_create_markers(self):
        images = ImageCollection(MockGui(), ".")
        images.load_image("TestImage.jpg", 100, 100)
        images.load_image("TestImage.jpg", 100, 100)

        markers = images.create_markers("TestMarker.jpg")

        self.assertIsNotNone(markers)
        self.assertEquals(2, len(markers))
        self.assertEquals(2, len(images.marker_images))

    def test_find_distances__no_markers(self):
        images = ImageCollection(MockGui(), ".")
        self.assertRaises(Exception, images.find_distances)

