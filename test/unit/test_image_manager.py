"""
Unit tests for ImageManager
"""
import unittest

from osmviz.manager import ImageManager


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


if __name__ == "__main__":
    unittest.main()


# End of file
