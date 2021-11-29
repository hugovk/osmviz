"""
Unit tests PILImageManager
"""
import unittest

from osmviz.manager import OSMManager, PILImageManager


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
