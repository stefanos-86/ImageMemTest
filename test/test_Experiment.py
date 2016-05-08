import unittest
import os

import sys
sys.path.append("./..")

from Experiment import Experiment

class TestExperiment(unittest.TestCase):
    test_path = os.path.realpath("./test")

    def test_construction__wrong_image(self):
        description = "1 2 3 rubbish 4 5 TestImage.jpg"
        self.assertRaises(Exception, Experiment, description, TestExperiment.test_path)

    def test_construction__one_image(self):
        exp = Experiment("1 2 3 4 5 TestImage.jpg", TestExperiment.test_path)
        self.assertEqual(1, len(exp.images))

        img = exp.images[0]
        self.assertEqual(1, img.width)
        self.assertEqual(2, img.heigth)
        self.assertEqual(3, img.centre_x)
        self.assertEqual(4, img.centre_y)
        self.assertEqual(5, img.duration)
        self.assertTrue("TestImage.jpg" in img.file_path)

    def test_construction__many_images(self):
        exp = Experiment("1 2 3 4 5 TestImage.jpg\n1 2 3 4 5 TestImage.jpg", TestExperiment.test_path)
        self.assertEqual(2, len(exp.images))

    def test_construction__empty_lines(self):
        exp = Experiment("1 2 3 4 5 TestImage.jpg\n1 2 3 4 5 TestImage.jpg\n", TestExperiment.test_path)
        self.assertEqual(2, len(exp.images))

    def test_construction__comment_line(self):
        exp = Experiment("#Comment\n1 2 3 4 5 TestImage.jpg", TestExperiment.test_path)
        self.assertEqual(1, len(exp.images))

    def test_construction__inline_comment(self):
        exp = Experiment("1 2 3 4 5 TestImage.jpg #Comment", TestExperiment.test_path)
        self.assertEqual(1, len(exp.images))
