from osmviz.manager import PILImageManager, OSMManager
import PIL.Image as Image


def test_pil():
    image_manager = PILImageManager("RGB")
    osm = OSMManager(image_manager=image_manager)
    image, bounds = osm.createOSMImage((30, 31, -117, -116), 9)
    wh_ratio = float(image.size[0]) / image.size[1]
    image2 = image.resize((int(800 * wh_ratio), 800), Image.ANTIALIAS)
    del image
    image2.show()


if __name__ == "__main__":
    test_pil()

# End of file
