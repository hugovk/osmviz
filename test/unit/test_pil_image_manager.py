"""
Unit tests for PILImageManager
"""
import unittest

from osmviz.manager import PILImageManager


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


if __name__ == "__main__":
    unittest.main()


# End of file
