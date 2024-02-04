"""
OpenStreetMap Animation Tool:
  - Provides easy setup to show things moving around on a map.
  - Requires pygame.

Basic idea:
  1. Create TrackingViz objects or your own custom SimViz's
  2. Create a Simulation object with those Viz's
  3. Call the Simulation's run() method
  4. Run the simulation:
     - Mouse over icons to display labels
     - up/down keys increase/decrease speed of simulation
     - left/right keys move simulation to begin/end of time window
     - space bar sets speed to zero
     - escape key exits

The TrackingViz class can be used without any knowledge of Pygame. All you
need is an image you want to put on the map and a function defining where it
should be on the map as a function of time.

For any other visualization on the map, you will want to override the
SimViz class. This will require knowledge of how to use Pygame. Basically
a Pygame Surface will be passed in when it is time to draw.

The Simulation class just does the following:
  1. Downloads OSM tiles, patches them together, and resizes
  2. Displays a window with the map on it
  3. Runs a timer and has all Viz objects draw to the map at each frame.

Keyboard input is accepted to control the speed of the simulation.
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
from __future__ import annotations

import time
from functools import reduce

import pygame

from .manager import OSMManager, PygameImageManager

Inf = float("inf")


class SimViz:
    """
    Abstract interface representing an object which knows how and when
    to display itself on a surface inside of a Simulation.

    This class is meant to serve as an interface definition to be
    subclassed (or at least replicated).
    """

    def __init__(self, drawing_order=0):
        """
        Base constructor for a SimViz.
        'drawingOrder' is used to specify the order in which this viz
        is drawn to the surface relative to others. See 'get_drawing_order()'.
        """
        self.drawing_order = drawing_order

    def get_bounding_box(self):
        """
        To be overridden.
        Returns (lat_min, lat_max, lon_min, lon_max) the lat/lon bounds
        of this visualization object.
        Note that for Simulation purposes, this does not need to
        be implemented if this SimViz is passed in as one of the
        scene_viz's (as opposed to an actor_viz).
        """
        raise NotImplementedError

    def get_time_interval(self):
        """
        To be overridden.
        Returns (begin, end) time values for the existence of this
        visualization object.
        May return (-Inf, Inf) to indicate that it is always present.
        """
        raise NotImplementedError

    def set_state(self, sim_time, get_xy):
        """
        To be overridden.
        Sets the internal state of this viz to the specified time.
        This should be stored internally, for subsequent calls to
        methods such as drawToSurface or mouseIntersect.
        """
        raise NotImplementedError

    def draw_to_surface(self, surf):
        """
        To be overridden.
        Draws this viz on the supplied surface, according to its
        internal state.
        """
        raise NotImplementedError

    def get_drawing_order(self):
        """
        Returns an integer representing the order in which this viz
        should be drawn relative to other vizs. Vizs with a higher
        drawing order are drawn after those with a lower drawing
        order, meaning they will be drawn on top.
        """
        return self.drawing_order

    def get_label(self):
        """
        To be overridden (optionally).
        Returns string to be displayed as descriptive label for this
        viz object. Default behavior is to return None, meaning no
        label should ever be displayed.
        """
        return None

    def mouse_intersect(self, mouse_x, mouse_y):
        """
        To be overridden.
        Returns True if the given mouse location is inside some
        designated region of this visualization.
        Note that for Simulation purposes, if get_label() returns
        None then this method does not need to be implemented.
        """
        raise NotImplementedError


class TrackingViz(SimViz):
    """
    A generic SimViz which displays a moving image on the map.
    """

    def __init__(
        self,
        label,
        image,
        get_lat_lon_at_time_func,
        time_window,
        bounding_box,
        drawing_order=0,
    ):
        """
        Constructs a TrackingViz.
        Arguments:
            label - text to display when moused over, or None for no text
            image - filename of image to display on map
            get_lat_lon_at_time_func - a function that takes one argument (time)
                 and returns (lat, lon)
            time_window - a tuple (begin_time, end_time) representing the times
                 this object exists
            bounding_box - a tuple (min_lat, max_lat, min_lon, max_lon)
                 representing the farthest bounds that this object will reach
            drawing_order - see SimViz.get_drawing_order()
        """
        SimViz.__init__(self, drawing_order)
        self.label = label
        self.image = pygame.image.load(image)
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.time_window = time_window
        self.bounding_box = bounding_box
        self.get_location_at_time = get_lat_lon_at_time_func

    def get_time_interval(self):
        return self.time_window

    def get_bounding_box(self):
        return self.bounding_box

    def get_label(self):
        return self.label

    def set_state(self, sim_time, get_xy):
        self.xy = None
        ll = self.get_location_at_time(sim_time)
        if ll is None:
            return
        x, y = get_xy(*ll)
        self.xy = x, y

    def draw_to_surface(self, surf):
        if self.xy:
            x, y = self.xy
            w, h = self.width, self.height
            x, y = x - w / 2, y - h / 2
            surf.blit(self.image, (x, y))

    def mouse_intersect(self, mouse_x, mouse_y):
        if not self.xy:
            return False
        x, y = self.xy
        w, h = self.width, self.height
        return abs(x - mouse_x) < w / 2 and abs(y - mouse_y) < h / 2


class Simulation:
    """
    A collection of generic SimViz's and a timer, of sorts. This lets the
    visualizer say "Give me coordinates of each object at time T". A run()
    method is provided which displays the simulation in a pygame window.
    """

    def __init__(self, actor_vizs, scene_vizs, init_time=0):
        """
        Given two collections of generic SimViz objects, and optionally an
        initial time, creates a Simulation object.
        Both actor_vizs and scene_vizs should be a collection of SimViz
        objects. The difference is that the actor_vizs will determine the
        bounds of the animation in space and time, while the location and
        time windows of the scene_vizs will be largely ignored.
        """
        self.actor_vizs = actor_vizs
        self.scene_vizs = scene_vizs
        self.all_vizs = actor_vizs + scene_vizs
        self.__find_bounding_box()
        self.__find_time_window()
        self.__sort_vizs()

        self.time = 10000
        self.set_time(init_time)

    def __find_bounding_box(self):
        """Finds the lat_lon box bounding all objects"""
        init_box = (Inf, -Inf, Inf, -Inf)

        def helper(left, right):
            right = right.get_bounding_box()
            return (
                min(left[0], right[0]),
                max(left[1], right[1]),
                min(left[2], right[2]),
                max(left[3], right[3]),
            )

        self.bounding_box = reduce(helper, self.actor_vizs, init_box)

    def __find_time_window(self):
        """Finds the min and max times over all routes"""
        init_window = (Inf, -Inf)

        def helper(left, right):
            right = right.get_time_interval()
            return min(left[0], right[0]), max(left[1], right[1])

        self.time_window = reduce(helper, self.actor_vizs, init_window)

    def __sort_vizs(self):
        """Sorts tracked objects in order of Drawing Order"""

        def key_function(item):
            return item.get_drawing_order()

        self.all_vizs.sort(key=key_function)

    def set_time(self, time):
        """
        Moves all bus tracks to the given time.
        """
        self.time = min(max(time, self.time_window[0]), self.time_window[1])

    def print_time(self):
        hours = int(self.time / 3600)
        minutes = int((self.time % 3600) / 60)
        seconds = int(self.time % 60)
        print(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def get_xy(self, lat, lon, bounds, screen_size):
        """
        Given coordinates in lon, lat, and a screen size,
        returns the corresponding (x, y) pixel coordinates.
        """
        x_ratio = (lon - bounds[2]) / (bounds[3] - bounds[2])
        y_ratio = 1.0 - ((lat - bounds[0]) / (bounds[1] - bounds[0]))
        x, y = int(x_ratio * screen_size[0]), int(y_ratio * screen_size[1])
        return x, y

    def run(
        self,
        speed=0.0,
        window_size=(1280, 800),
        refresh_rate=1.0,
        font="/Library/Frameworks/Python.framework/Versions/2.5/"
        "lib/python2.5/site-packages/pygame/freesansbold.ttf",
        font_size=10,
        osm_zoom=14,
    ):
        """
        Pops up a window and displays the simulation on it.
        speed is advancement of sim in seconds/second.
        refresh_rate is pause in seconds between frames.
        window_size is the desired (width, height) of the display window.
        Font is either the full path to a pygame-compatible font file
            (e.g. a .ttf file), or an actual pygame Font object, or None.
            If None, then labels will not be rendered, instead they will be
            printed to stdout.
        font_size is the size of the font, if it exists.
        """
        pygame.init()
        black = pygame.Color(0, 0, 0)
        notec = pygame.Color(200, 200, 80)

        fnt = None
        if isinstance(font, str):
            try:
                fnt = pygame.font.Font(font, font_size)
            except Exception:
                fnt = None
        elif isinstance(font, pygame.font.Font):
            fnt = font

        osm = OSMManager(cache="maptiles/", image_manager=PygameImageManager())
        bg_big, new_bounds = osm.create_osm_image(self.bounding_box, zoom=osm_zoom)
        w_h_ratio = float(bg_big.get_width()) / bg_big.get_height()
        # Make the window smaller to keep proportions and stay within
        # specified window_size
        new_width = int(window_size[1] * w_h_ratio)
        new_height = int(window_size[0] / w_h_ratio)
        if new_width > window_size[0]:
            window_size = window_size[0], new_height
        elif new_height > window_size[1]:
            window_size = new_width, window_size[1]

        screen = pygame.display.set_mode(window_size)

        bg_small = pygame.transform.smoothscale(bg_big, window_size)
        del bg_big

        last_time = self.time

        def get_xy(lat, lon):
            return self.get_xy(lat, lon, new_bounds, window_size)

        # Main simulation loop #

        ready_to_exit = False
        while not ready_to_exit:
            # Check keyboard events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    ready_to_exit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    speed = max((speed + 1) * 1.4, (speed / 1.4) + 1)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    speed = min((speed / 1.4) - 1, (speed - 1) * 1.4)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    speed = 0.0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.time = self.time_window[0]
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.time = self.time_window[1]

            # Grab mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected = None

            # Print the time if changed
            if self.time != last_time:
                self.print_time()
            last_time = self.time

            # Draw the background
            screen.blit(bg_small, (0, 0))

            # Draw the tracked objects
            for sviz in self.all_vizs:
                sviz.set_state(self.time, get_xy)
                sviz.draw_to_surface(screen)
                label = sviz.get_label()
                if label and sviz.mouse_intersect(mouse_x, mouse_y):
                    selected = sviz

            # Display selected label
            if selected:
                if fnt:
                    text = fnt.render(selected.get_label(), True, black, notec)
                    screen.blit(text, (mouse_x, mouse_y - 10))
                    del text
                else:
                    print(selected.getLabel())

            pygame.display.flip()

            time.sleep(refresh_rate)
            self.set_time(self.time + speed * refresh_rate)

        # Clean up and exit
        del bg_small
        pygame.display.quit()
