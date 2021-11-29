#!/usr/bin/env python
"""
Unit tests for manager.py
"""
import unittest

from osmviz.manager import ImageManager, OSMManager, PILImageManager


class TestImageManager(unittest.TestCase):
    # Abstract interface to be overridden

    def test_unimplemented(self):
        # Arrange
        image_manager = ImageManager()
        # Dummy parameters
        dp1 = None
        dp2 = None

        # Act / Assert
        self.assertRaises(Exception, lambda: image_manager.paste_image(dp1, dp2))
        self.assertRaises(Exception, lambda: image_manager.load_image_file(dp1))
        self.assertRaises(Exception, lambda: image_manager.create_image(dp1, dp2))


class TestPILImageManager(unittest.TestCase):
    def setUp(self):
        mode = "RGB"
        self.image_manager = PILImageManager(mode)

    def test_prepare_image(self):
        # Arrange
        width, height = 200, 100

        # Act
        self.image_manager.prepare_image(width, height)

        # Assert
        self.assertEqual(self.image_manager.image.size, (200, 100))

    def test_prepare_image__twice(self):
        # Arrange
        width, height = 200, 100

        # Act
        self.image_manager.prepare_image(width, height)

        # Assert
        self.assertRaises(
            Exception, lambda: self.image_manager.prepare_image(width, height)
        )

    def test_destroy_image__no_image(self):
        # Arrange
        # Act
        self.image_manager.destroy_image()

        # Assert
        self.assertIsNone(self.image_manager.image)

    def test_destroy_image__with_image(self):
        # Arrange
        width, height = 200, 100
        self.image_manager.prepare_image(width, height)
        self.assertEqual(self.image_manager.image.size, (200, 100))

        # Act
        self.image_manager.destroy_image()

        # Assert
        self.assertIsNone(self.image_manager.image)

    def test_paste_image_file__image_not_prepared(self):
        # Arrange
        imagef = "dummy.jpg"
        xy = (0, 0)

        # Act / Assert
        self.assertRaises(
            Exception, lambda: self.image_manager.paste_image_file(imagef, xy)
        )

    def test_paste_image_file__could_not_load_image(self):
        # Arrange
        width, height = 200, 100
        self.image_manager.prepare_image(width, height)
        self.assertEqual(self.image_manager.image.size, (200, 100))
        imagef = "dummy.jpg"
        xy = (0, 0)

        # Act / Assert
        self.assertRaises(
            Exception, lambda: self.image_manager.paste_image_file(imagef, xy)
        )

    def test_paste_image_file(self):
        # Arrange
        width, height = 200, 100
        self.image_manager.prepare_image(width, height)
        self.assertEqual(self.image_manager.image.size, (200, 100))
        imagef = "test/images/bus.png"
        xy = (0, 0)

        # Act
        self.image_manager.paste_image_file(imagef, xy)

        # Assert
        self.assertEqual(self.image_manager.image.size, (200, 100))

    def test_get_image(self):
        # Arrange
        width, height = 200, 100
        self.image_manager.prepare_image(width, height)
        self.assertIsNotNone(self.image_manager.image)

        # Act
        im = self.image_manager.get_image()

        # Assert
        self.assertEqual(im.size, (200, 100))


class TestOSMManager(unittest.TestCase):
    def setUp(self):
        image_manager = PILImageManager("RGB")
        self.osm = OSMManager(image_manager=image_manager)

    def test_get_tile_coord(self):
        # Arrange
        lon_deg = 24.945831
        lat_deg = 60.192059
        zoom = 15

        # Act
        coord = self.osm.get_tile_coord(lon_deg, lat_deg, zoom)

        # Assert
        self.assertEqual(coord, (18654, 9480))

    def test_get_tile_url(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        url = self.osm.get_tile_url(tile_coord, zoom)

        # Assert
        self.assertEqual(url, "https://tile.openstreetmap.org/15/18654/9480.png")

    def test_get_local_tile_filename(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        filename = self.osm.get_local_tile_filename(tile_coord, zoom)

        # Assert
        self.assertTrue(filename.endswith("-15_18654_9480.png"))

    def test_retrieve_tile_image(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        filename = self.osm.retrieve_tile_image(tile_coord, zoom)

        # Assert
        self.assertTrue(filename.endswith("-15_18654_9480.png"))

    def test_tile_nw_latlon(self):
        # Arrange
        tile_coord = (18654, 9480)
        zoom = 15

        # Act
        lat_deg, lon_deg = self.osm.tile_nw_lat_lon(tile_coord, zoom)

        # Assert
        self.assertEqual((lat_deg, lon_deg), (60.19615576604439, 24.93896484375))

    def test_create_osm_image(self):
        # Arrange
        minlat = 59.9225115912
        maxlat = 60.297839409
        minlon = 24.7828044415
        maxlon = 25.2544966708
        bounds = (minlat, maxlat, minlon, maxlon)
        zoom = 8

        # Act
        im, new_bounds = self.osm.create_osm_image(bounds, zoom)

        # Assert
        self.assertEqual(
            new_bounds, (59.5343180010956, 60.930432202923335, 23.90625, 25.3125)
        )
        self.assertEqual(im.size, (256, 512))


if __name__ == "__main__":
    unittest.main()


# End of file
