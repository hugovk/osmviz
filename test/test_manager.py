from osmviz.manager import PILImageManager, OSMManager
import PIL.Image as Image


def test_pil():
    imgr = PILImageManager('RGB')
    osm = OSMManager(image_manager=imgr)
    image, bnds = osm.createOSMImage((30, 35, -117, -112), 9)
    wh_ratio = float(image.size[0]) / image.size[1]
    image2 = image.resize((int(800*wh_ratio), 800), Image.ANTIALIAS)
    del image
    image2.show()


if __name__ == '__main__':
    test_pil()

# End of file
