"""
OpenStreetMap Management Tool:
  - Provides simple interface to retrieve and tile OSM images
  - Can use pygame or PIL (to generate pygame Surfaces or PIL images)

Basic idea:
  1. Choose an ImageManager class and construct an instance.
     - Pygame and PIL implementations available
     - To make your own custom ImageManager, override the ImageManager
       class.
  2. Construct an OSMManager object.
     - Can provide custom OSM server URL, etc.
  3. Use the OSMManager to retrieve individual tiles and do as you please
     or patch tiles together into a larger image for you.
"""

# Copyright (c) 2010 Colin Bick, Robert Damphousse

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function, unicode_literals
import hashlib
import math
import os.path as path
import os
try:
    # Python 2
    from urllib import urlretrieve, FancyURLopener
    import urllib
except ImportError:
    # Python 3
    from urllib.request import urlretrieve, FancyURLopener
    import urllib.request._urlopener


class ImageManager(object):
    """
    Simple abstract interface for creating and manipulating images, to be used
    by an OSMManager object.
    """

    def __init__(self):
        self.image = None

    # TO BE OVERRIDDEN #

    def paste_image(self, img, xy):
        """
        To be overridden.
        Given an already-loaded file, paste it into the internal image
        at the specified top-left coordinate.
        """
        raise Exception("UNIMPLEMENTED")

    def load_image_file(self, imagef):
        """
        To be overridden.
        Loads specified image file into image object and returns it.
        """
        raise Exception("UNIMPLEMENTED")

    def create_image(self, width, height):
        """
        To be overridden.
        Create and return image with specified dimensions
        """
        raise Exception("UNIMPLEMENTED")

    # END OF TO BE OVERRIDDEN #

    def prepare_image(self, width, height):
        """
        Create and internally store an image whose dimensions
        are those specified by width and height.
        """
        if self.image:
            raise Exception("Image already prepared.")
        self.image = self.create_image(width, height)

    def destroy_image(self):
        """
        Destroys internal representation of the image, if it was
        ever created.
        """
        if self.image:
            del self.image
        self.image = None

    def paste_image_file(self, imagef, xy):
        """
        Given the filename of an image, and the x, y coordinates of the
        location at which to place the top left corner of the contents
        of that image, pastes the image into this object's internal image.
        """
        if not self.image:
            raise Exception("Image not prepared")

        try:
            img = self.load_image_file(imagef)
        except Exception as e:
            raise Exception("Could not load image "+str(imagef)+"\n"+str(e))

        self.paste_image(img, xy)
        del img

    def getImage(self):
        """
        Returns some representation of the internal image. The returned value
        is not for use by the OSMManager.
        """
        return self.image


class PygameImageManager(ImageManager):
    """
    An ImageManager which works with Pygame images.
    """

    def __init__(self):
        ImageManager.__init__(self)
        try:
            import pygame
        except:
            raise Exception("Pygame could not be imported!")
        self.pygame = pygame

    def create_image(self, width, height):
        return self.pygame.Surface((width, height))

    def load_image_file(self, imagef):
        return self.pygame.image.load(imagef)

    def paste_image(self, img, xy):
        self.getImage().blit(img, xy)


class PILImageManager(ImageManager):
    """
    An ImageManager which works with PIL images.
    """

    def __init__(self, mode):
        """
        Constructs a PIL Image Manager.
        Arguments:
            mode - the PIL mode in which to create the image.
        """
        ImageManager.__init__(self)
        self.mode = mode
        try:
            import PIL.Image
        except:
            raise Exception("PIL could not be imported!")
        self.PILImage = PIL.Image

    def create_image(self, width, height):
        return self.PILImage.new(self.mode, (width, height))

    def load_image_file(self, imagef):
        return self.PILImage.open(imagef)

    def paste_image(self, img, xy):
        self.getImage().paste(img, xy)


class OSMManager(object):
    """
    An OSMManager manages the retrieval and storage of Open Street Map
    images. The basic utility is the createOSMImage() method which
    automatically gets all the images needed, and tiles them together
    into one big image.
    """
    def __init__(self, **kwargs):
        """
        Creates an OSMManager.
        Arguments:

        cache - path (relative or absolute) to directory where tiles downloaded
                    from OSM server should be saved. Default "/tmp".

        server - URL of OSM server from which to retrieve OSM tiles. This
                    should be fully qualified, including the protocol.
                    Default "http://tile.openstreetmap.org"

        url - Full URL template from which to retrieve OSM tiles. This should
                    be fully qualified, including the protocol, and should
                    contain placeholders for zoom ('{z}'), coordinate x and y
                    ('{x}' and '{y}'), and optionally scale ('{s}') for high-
                    resolution tile retrieval.
                    Note: when specified, the server parameter is ignored.
                    Default: server with "/{z}/{x}/{y}.png" appended

        scale - Scale to use for high-resolution tiles. Note that both URL and
                    scale must be set correctly for correct high-resolution
                    support. Standard tile size is 256 pixels, high-resolution
                    tiles are scale times 256 pixels (e.g., 512 pixels when
                    scale is 2).
                    Default 1 (standard resolution)

        image_manager - ImageManager instance which will be used to do all
                            image manipulation. You must provide this.
        """
        cache = kwargs.get('cache')
        server = kwargs.get('server')
        url = kwargs.get('url')
        scale = kwargs.get('scale')
        mgr = kwargs.get('image_manager')

        self.cache = None

        if cache:
            if not os.path.isdir(cache):
                try:
                    os.makedirs(cache, 0o766)
                    self.cache = cache
                    print("WARNING: Created cache dir", cache)
                except:
                    print("Could not make cache dir", cache)
            elif not os.access(cache, os.R_OK | os.W_OK):
                print("Insufficient privileges on cache dir", cache)
            else:
                self.cache = cache

        if not self.cache:
            self.cache = (os.getenv("TMPDIR") or
                          os.getenv("TMP") or
                          os.getenv("TEMP") or
                          "/tmp")
            print("WARNING: Using %s to cache maptiles." % self.cache)
            if not os.access(self.cache, os.R_OK | os.W_OK):
                print(" ERROR: Insufficient access to %s." % self.cache)
                raise Exception("Unable to find/create/use maptile cache "
                                "directory.")

        # Get URL template, which supports the following fields:
        #  * {z}: tile zoom level
        #  * {x}, {y}: coordinate x and y
        #  * {s}: high-resolution scale factor.
        # Note: high-resolution is not currently supported by the default OSM
        # tile servers, but this can look like this, for example:
        #  * http://server/layer@{s}x/{z}/{x}/{y}.png
        #  * http://server/layer/{z}/{x}/{y}@{s}x.png (e.g. Mapbox)
        #  * http://server/layer/{z}/{x}/{y}.png?scale={s} (e.g. Google Maps)
        if url:
            self.url = url
        elif server:
            self.url = "%s/{z}/{x}/{y}.png" % server
        else:
            self.url = "http://tile.openstreetmap.org/{z}/{x}/{y}.png"

        # Default scale is 1. High-resolution tiles use 1.5, 2 (most common),
        # 3, 4 or even more.
        if scale:
            self.scale = scale
        else:
            self.scale = 1

        # Tile size is 256 pixels multiplied by scale
        self.tile_size = 256 * self.scale

        # Make a hash of the server URL to use in cached tile filenames.
        md5 = hashlib.md5()
        md5.update(self.url.replace("{s}", str(self.scale)).encode("utf-8"))
        self.cache_prefix = 'osmviz-%s-' % md5.hexdigest()[:5]

        if mgr:  # Assume it's a valid manager
            self.manager = mgr
        else:
            raise Exception("OSMManager.__init__ requires argument "
                            "image_manager")

    def getTileCoord(self, lon_deg, lat_deg, zoom):
        """
        Given lon, lat coords in DEGREES, and a zoom level,
        returns the (x, y) coordinate of the corresponding tile #.
        (http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python)
        """
        lat_rad = lat_deg * math.pi / 180.0
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) +
                    (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return(xtile, ytile)

    def getTileURL(self, tile_coord, zoom):
        """
        Given x, y coord of the tile to download, and the zoom level,
        returns the URL from which to download the image.
        """
        return self.url.format(x=tile_coord[0], y=tile_coord[1], z=zoom,
                               s=self.scale)

    def getLocalTileFilename(self, tile_coord, zoom):
        """
        Given x, y coord of the tile, and the zoom level,
        returns the filename to which the file would be saved
        if it was downloaded. That way we don't have to kill
        the osm server every time the thing runs.
        """
        params = (self.cache_prefix, zoom, tile_coord[0], tile_coord[1])
        return path.join(self.cache, "%s%d_%d_%d.png" % params)

    def retrieveTileImage(self, tile_coord, zoom):
        """
        Given x, y coord of the tile, and the zoom level,
        retrieves the file to disk if necessary and
        returns the local filename.
        """
        filename = self.getLocalTileFilename(tile_coord, zoom)
        if not path.isfile(filename):
            url = self.getTileURL(tile_coord, zoom)
            try:
                urlretrieve(url, filename=filename)
            except Exception as e:
                raise Exception("Unable to retrieve URL: "+url+"\n"+str(e))
        return filename

    def tileNWLatlon(self, tile_coord, zoom):
        """
        Given x, y coord of the tile, and the zoom level,
        returns the (lat, lon) coordinates of the upper
        left corner of the tile.
        """
        xtile, ytile = tile_coord
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return(lat_deg, lon_deg)

    def createOSMImage(self, bounds, zoom):
        """
        Given bounding latlons (in degrees), and an OSM zoom level,
        creates an image constructed from OSM tiles.
        Returns (img, bounds) where img is the constructed image (as returned
        by the image manager's "getImage()" method),
        and bounds is the (latmin, latmax, lonmin, lonmax) bounding box
        which the tiles cover.
        """
        (minlat, maxlat, minlon, maxlon) = bounds
        if not self.manager:
            raise Exception("No ImageManager was specified, cannot create "
                            "image.")

        topleft = minX, minY = self.getTileCoord(minlon, maxlat, zoom)
        maxX, maxY = self.getTileCoord(maxlon, minlat, zoom)
        new_maxlat, new_minlon = self.tileNWLatlon(topleft, zoom)
        new_minlat, new_maxlon = self.tileNWLatlon((maxX+1, maxY+1), zoom)
        pix_width = (maxX-minX+1)*self.tile_size
        pix_height = (maxY-minY+1)*self.tile_size
        self.manager.prepare_image(pix_width, pix_height)
        print("Retrieving %d tiles..." % ((1+maxX-minX)*(1+maxY-minY), ))

        for x in range(minX, maxX+1):
            for y in range(minY, maxY+1):
                fname = self.retrieveTileImage((x, y), zoom)
                x_off = self.tile_size*(x-minX)
                y_off = self.tile_size*(y-minY)
                self.manager.paste_image_file(fname, (x_off, y_off))
        print("... done.")
        return (self.manager.getImage(),
                (new_minlat, new_maxlat, new_minlon, new_maxlon))


class _useragenthack(FancyURLopener):
    def __init__(self, *args):
        FancyURLopener.__init__(self, *args)
        for i, (header, val) in enumerate(self.addheaders):
            if header == "User-Agent":
                del self.addheaders[i]
                break
        self.addheader('User-Agent',
                       'OSMViz/1.0 +http://cbick.github.com/osmviz')


# import httplib
# httplib.HTTPConnection.debuglevel = 1
try:
    # Python 2
    urllib._urlopener = _useragenthack()
except AttributeError:
    # Python 3
    urllib.request._urlopener = _useragenthack()
