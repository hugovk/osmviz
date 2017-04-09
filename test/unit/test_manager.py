#!/usr/bin/env python
"""
Unit tests for manager.py
"""
from __future__ import print_function, unicode_literals

import unittest

from osmviz.manager import ImageManager, PILImageManager


class TestImageManager(unittest.TestCase):
    # Abstract interface to be overridden

    def test_unimplemented(self):
        # Arrange
        imgr = ImageManager()
        # Dummy parameters
        dp1 = None
        dp2 = None

        # Act / Assert
        self.assertRaises(Exception, lambda: imgr.paste_image(dp1, dp2))
        self.assertRaises(Exception, lambda: imgr.load_image_file(dp1))
        self.assertRaises(Exception, lambda: imgr.create_image(dp1, dp2))


class TestPILImageManager(unittest.TestCase):

    def setUp(self):
        mode = "RGB"
        self.imgr = PILImageManager(mode)

    def test_prepare_image(self):
        # Arrange
        width, height = 200, 100

        # Act
        self.imgr.prepare_image(width, height)

        # Assert
        self.assertEqual(self.imgr.image.size, (200, 100))

    def test_prepare_image__twice(self):
        # Arrange
        width, height = 200, 100

        # Act
        self.imgr.prepare_image(width, height)

        # Assert
        self.assertRaises(Exception,
                          lambda: self.imgr.prepare_image(width, height))

    def test_destroy_image__no_image(self):
        # Arrange
        # Act
        self.imgr.destroy_image()

        # Assert
        self.assertEqual(self.imgr.image, None)

    def test_destroy_image__with_image(self):
        # Arrange
        width, height = 200, 100
        self.imgr.prepare_image(width, height)
        self.assertEqual(self.imgr.image.size, (200, 100))

        # Act
        self.imgr.destroy_image()

        # Assert
        self.assertEqual(self.imgr.image, None)

    def test_paste_image_file__image_not_prepared(self):
        # Arrange
        imagef = "dummy.jpg"
        xy = (0, 0)

        # Act / Assert
#         self.imgr.paste_image_file(imagef, xy)
        self.assertRaises(Exception,
                          lambda: self.imgr.paste_image_file(imagef, xy))

    def test_paste_image_file__could_not_load_image(self):
        # Arrange
        width, height = 200, 100
        self.imgr.prepare_image(width, height)
        self.assertEqual(self.imgr.image.size, (200, 100))
        imagef = "dummy.jpg"
        xy = (0, 0)

        # Act / Assert
        self.assertRaises(Exception,
                          lambda: self.imgr.paste_image_file(imagef, xy))

    def test_paste_image_file(self):
        # Arrange
        width, height = 200, 100
        self.imgr.prepare_image(width, height)
        self.assertEqual(self.imgr.image.size, (200, 100))
        imagef = "test/images/bus.png"
        xy = (0, 0)

        # Act
        self.imgr.paste_image_file(imagef, xy)

        # Assert
        self.assertEqual(self.imgr.image.size, (200, 100))
        # TODO assert image for correctness

    def test_getImage(self):
        # Arrange
        width, height = 200, 100
        self.imgr.prepare_image(width, height)
        self.assertIsNotNone(self.imgr.image)

        # Act
        im = self.imgr.getImage()

        # Assert
        self.assertEqual(im.size, (200, 100))


if __name__ == '__main__':
    unittest.main()


# End of file
