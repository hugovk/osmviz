"""
Unit tests PILImageManager
"""
from __future__ import annotations

import pytest

from osmviz.manager import OSMManager, PILImageManager


@pytest.fixture()
def osm_manager():
    image_manager = PILImageManager("RGB")
    osm_manager = OSMManager(image_manager=image_manager)
    yield osm_manager


def test_get_tile_coord(osm_manager):
    # Arrange
    lon_deg = 24.945831
    lat_deg = 60.192059
    zoom = 15

    # Act
    coord = osm_manager.get_tile_coord(lon_deg, lat_deg, zoom)

    # Assert
    assert coord == (18654, 9480)


def test_get_tile_url(osm_manager):
    # Arrange
    tile_coord = (18654, 9480)
    zoom = 15

    # Act
    url = osm_manager.get_tile_url(tile_coord, zoom)

    # Assert
    assert url == "https://tile.openstreetmap.org/15/18654/9480.png"


def test_get_local_tile_filename(osm_manager):
    # Arrange
    tile_coord = (18654, 9480)
    zoom = 15

    # Act
    filename = osm_manager.get_local_tile_filename(tile_coord, zoom)

    # Assert
    assert filename.endswith("-15_18654_9480.png")


def test_retrieve_tile_image(osm_manager):
    # Arrange
    tile_coord = (18654, 9480)
    zoom = 15

    # Act
    filename = osm_manager.retrieve_tile_image(tile_coord, zoom)

    # Assert
    assert filename.endswith("-15_18654_9480.png")


def test_tile_nw_lat_lon(osm_manager):
    # Arrange
    tile_coord = (18654, 9480)
    zoom = 15

    # Act
    lat_deg, lon_deg = osm_manager.tile_nw_lat_lon(tile_coord, zoom)

    # Assert
    assert (lat_deg, lon_deg) == (60.19615576604439, 24.93896484375)


def test_create_osm_image(osm_manager):
    # Arrange
    minlat = 59.9225115912
    maxlat = 60.297839409
    minlon = 24.7828044415
    maxlon = 25.2544966708
    bounds = (minlat, maxlat, minlon, maxlon)
    zoom = 8

    # Act
    im, new_bounds = osm_manager.create_osm_image(bounds, zoom)

    # Assert
    assert new_bounds == (59.5343180010956, 60.930432202923335, 23.90625, 25.3125)
    assert im.size == (256, 512)
