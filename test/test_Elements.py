import unittest

import sys
import time
import re

sys.path.append("./..")

from Elements import ExperimentImage
from Elements import ImageCollection
from Elements import DecoratedDistance
from Elements import RecallTimer


from GuiFacade import GuiFacade
gui = GuiFacade()  # Must initialize TK to load the real images.

class MockGui(GuiFacade):  # Subclass so we get the real loading methods, but we can mock what we need.
    def screen_size(self):
        return (1000, 1000)

class MockMarker:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def centre_position(self):
        return self.x, self.y


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

        image = images.add_image("TestImage.jpg", 100, 100)

        self.assertIsNotNone(image)
        self.assertEquals(1, len(images.images))
        self.assertEquals(image, images.images[0])

    def test_load_image__invalid_image(self):
        images = ImageCollection(MockGui(), ".")

        self.assertRaises(Exception, images.add_image, "TestImage.jpg", 1000, 100)

    def test_create_markers(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 100, 100)
        images.add_image("TestImage.jpg", 100, 100)

        markers = images.create_markers("TestMarker.jpg")

        self.assertIsNotNone(markers)
        self.assertEquals(2, len(markers))
        self.assertEquals(2, len(images.marker_images))

    def test_find_distances__no_markers(self):
        images = ImageCollection(MockGui(), ".")
        self.assertRaises(Exception, images.find_distances)

    def test_find_distances__fills_results_correctly(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 100, 200)
        images.create_markers("TestMarker.jpg")
        images.gui_markers.append(MockMarker(3, 4))

        distances = images.find_distances()
        self.assertEquals(1, len(distances))

        distance = distances[0]
        self.assertEquals((100, 200), distance.image_centre)
        self.assertEquals((3, 4), distance.marker_centre)
        self.assertEquals("./TestImage.jpg", distance.image_id)

    def test_find_distances__coincidents(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 100, 100)
        images.create_markers("TestMarker.jpg")
        images.gui_markers.append(MockMarker(100, 100))

        distances = images.find_distances()
        self.assertEquals(0, distances[0].distance)

    def test_find_distances__single_image(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 100, 100)
        images.create_markers("TestMarker.jpg")
        images.gui_markers.append(MockMarker(200, 100))

        distances = images.find_distances()
        self.assertEquals(100, distances[0].distance)

    def test_find_distances__both_axis(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 100, 100)
        images.create_markers("TestMarker.jpg")
        images.gui_markers.append(MockMarker(101, 101))

        distances = images.find_distances()
        self.assertAlmostEquals(1.414, distances[0].distance, 3)

    def test_find_distances__equidistant_images(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 100, 100)
        images.add_image("TestImage.jpg", 200, 100)
        images.create_markers("TestMarker.jpg")
        images.gui_markers.append(MockMarker(101, 100))
        images.gui_markers.append(MockMarker(201, 100))

        distances = images.find_distances()
        self.assertEquals(2, len(distances))
        self.assertEquals(1, distances[0].distance)
        self.assertEquals(1, distances[1].distance)

    def test_find_distances__almost_whole_screen(self):
        images = ImageCollection(MockGui(), ".")
        images.add_image("TestImage.jpg", 96, 96)
        images.create_markers("TestMarker.jpg")
        images.gui_markers.append(MockMarker(996, 996))

        distances = images.find_distances()
        self.assertAlmostEquals(1.414213562 * 900, distances[0].distance, 3) # The screen is square.


class MockFile:
    def __init__(self):
        self.text = None

    def write(self, text):
        self.text = text


class TestDecoratedDistance(unittest.TestCase):
    def test_dump_on_file(self):
        output_file = MockFile()
        distance = DecoratedDistance(1, (2, 3), (4, 5), "id")

        distance.dump(output_file)

        self.assertEqual("     1           (2, 3)           (4, 5) id\n", output_file.text)

    def test_dump_on_file__lots_of_decimals_in_float_distance(self):
        output_file = MockFile()
        distance = DecoratedDistance(1.123456789, (2, 3), (4, 5), "id")

        distance.dump(output_file)

        self.assertEqual("     1           (2, 3)           (4, 5) id\n", output_file.text)


    def test_header(self):
        output_file = MockFile()
        distance = DecoratedDistance(1, (2, 3), (4, 5), "id")

        distance.header(output_file)

        self.assertEqual("  dist     image_centre    marker_centre image_id\n", output_file.text)


class TestRecallTimer(unittest.TestCase):
    def test_duration_measure(self):
        rt = RecallTimer()
        rt.markers_placed()
        time.sleep(1)
        rt.experiment_complete()

        self.assertEqual(1, rt.experiment_duration_seconds)

        # See also the long duration test Demo - can't have a minute-long test case...

    def test_dump(self):
        output_file = MockFile()
        rt = RecallTimer()
        rt.markers_placed()
        rt.experiment_complete()

        rt.dump(output_file)

        expected = re.compile("Start: .*\nEnd: .*\nDuration: 0 seconds")
        match = re.match(expected, output_file.text)

        self.assertTrue(match)