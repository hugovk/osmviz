"""
Unit tests for PILImageManager
"""
import pytest

from osmviz.manager import PILImageManager


@pytest.fixture()
def image_manager():
    mode = "RGB"
    image_manager = PILImageManager(mode)
    yield image_manager


def test_prepare_image(image_manager):
    # Arrange
    width, height = 200, 100

    # Act
    image_manager.prepare_image(width, height)

    # Assert
    assert image_manager.image.size == (200, 100)


def test_prepare_image__twice(image_manager):
    # Arrange
    width, height = 200, 100

    # Act
    image_manager.prepare_image(width, height)

    # Assert
    with pytest.raises(Exception):
        image_manager.prepare_image(width, height)


def test_destroy_image__no_image(image_manager):
    # Arrange
    # Act
    image_manager.destroy_image()

    # Assert
    assert image_manager.image is None


def test_destroy_image__with_image(image_manager):
    # Arrange
    width, height = 200, 100
    image_manager.prepare_image(width, height)
    assert image_manager.image.size == (200, 100)

    # Act
    image_manager.destroy_image()

    # Assert
    assert image_manager.image is None


def test_paste_image_file__image_not_prepared(image_manager):
    # Arrange
    filename = "dummy.jpg"
    xy = (0, 0)

    # Act / Assert
    with pytest.raises(Exception):
        image_manager.paste_image_file(filename, xy)


def test_paste_image_file__could_not_load_image(image_manager):
    # Arrange
    width, height = 200, 100
    image_manager.prepare_image(width, height)
    assert image_manager.image.size == (200, 100)
    filename = "dummy.jpg"
    xy = (0, 0)

    # Act / Assert
    with pytest.raises(Exception):
        image_manager.paste_image_file(filename, xy)


def test_paste_image_file(image_manager):
    # Arrange
    width, height = 200, 100
    image_manager.prepare_image(width, height)
    assert image_manager.image.size == (200, 100)
    filename = "test/images/bus.png"
    xy = (0, 0)

    # Act
    image_manager.paste_image_file(filename, xy)

    # Assert
    assert image_manager.image.size == (200, 100)


def test_get_image(image_manager):
    # Arrange
    width, height = 200, 100
    image_manager.prepare_image(width, height)
    assert image_manager.image is not None

    # Act
    im = image_manager.get_image()

    # Assert
    assert im.size == (200, 100)
