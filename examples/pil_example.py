"""
This example demonstrates how to create and show a PIL image
of OSM tiles patched together.
"""

from PIL import Image

from osmviz.manager import OSMManager, PILImageManager

image_manager = PILImageManager("RGB")
osm = OSMManager(image_manager=image_manager)
image, bounds = osm.create_osm_image((30, 35, -117, -112), 9)
wh_ratio = float(image.size[0]) / image.size[1]
image2 = image.resize((int(800 * wh_ratio), 800), Image.ANTIALIAS)
del image
image2.show()
