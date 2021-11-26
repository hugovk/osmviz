import PIL.Image as Image

from osmviz.manager import OSMManager, PILImageManager


def test_pil():
    image_manager = PILImageManager("RGB")
    osm = OSMManager(image_manager=image_manager)
    image, bounds = osm.create_osm_image((30, 31, -117, -116), 9)
    wh_ratio = float(image.size[0]) / image.size[1]
    image2 = image.resize((int(800 * wh_ratio), 800), Image.ANTIALIAS)
    del image
    image2.show()


if __name__ == "__main__":
    test_pil()

# End of file
