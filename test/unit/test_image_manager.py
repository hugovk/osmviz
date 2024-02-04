"""
Unit tests for ImageManager
"""

from __future__ import annotations

import pytest

from osmviz.manager import ImageManager


def test_unimplemented():
    # Arrange
    image_manager = ImageManager()
    # Dummy parameters
    dp1 = None
    dp2 = None

    # Act / Assert
    with pytest.raises(NotImplementedError):
        image_manager.paste_image(dp1, dp2)
        image_manager.load_image_file(dp1)
        image_manager.create_image(dp1, dp2)
