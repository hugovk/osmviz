#!/usr/bin/env python
"""
Unit tests for manager.py
"""
from __future__ import print_function, unicode_literals

import unittest

from osmviz.manager import ImageManager, OSMManager, PILImageManager


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

    def test_getImage(self):
        # Arrange
        width, height = 200, 100
        self.imgr.prepare_image(width, height)
        self.assertIsNotNone(self.imgr.image)

        # Act
        im = self.imgr.getImage()

        # Assert
        self.assertEqual(im.size, (200, 100))


class TestOSMManager(unittest.TestCase):

    def setUp(self):
        imgr = PILImageManager('RGB')
        self.osm = OSMManager(image_manager=imgr)

    def test_getTileCoord(self):
        # Arrange
        lon_deg = 24.945831
        lat_deg = 60.192059
        zoom = 15

        # Act
        coord = self.osm.getTileCoord(lon_deg, lat_deg, zoom)

        # Assert
        self.assertEqual(coord, (18654, 9480))

    def test_getTileURL(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        url = self.osm.getTileURL(tile_coord, zoom)

        # Assert
        self.assertEqual(url,
                         "https://tile.openstreetmap.org/15/18654/9480.png")

    def test_getLocalTileFilename(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        filename = self.osm.getLocalTileFilename(tile_coord, zoom)

        # Assert
        self.assertTrue(filename.endswith("-15_18654_9480.png"))

    def test_retrieveTileImage(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        filename = self.osm.retrieveTileImage(tile_coord, zoom)

        # Assert
        self.assertTrue(filename.endswith("-15_18654_9480.png"))

    def test_tileNWLatlon(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        lat_deg, lon_deg = self.osm.tileNWLatlon(tile_coord, zoom)

        # Assert
        self.assertEqual((lat_deg, lon_deg),
                         (60.19615576604439, 24.93896484375))

    def test_createOSMImage(self):
        # Arrange
        minlat = 59.9225115912
        maxlat = 60.297839409
        minlon = 24.7828044415
        maxlon = 25.2544966708
        bounds = (minlat, maxlat, minlon, maxlon)
        zoom = 8

        # Act
        im, new_bounds = self.osm.createOSMImage(bounds, zoom)

        # Assert
        self.assertEqual(new_bounds,
                         (59.5343180010956, 60.930432202923335,
                          23.90625, 25.3125))
        self.assertEqual(im.size, (256, 512))


if __name__ == '__main__':
    unittest.main()


# End of file
