"""
This example demonstrates how to subclass the SimViz class
in order to create your own custom visualizations. This is
if you want to do something besides just show icons moving
on the map.
"""

from __future__ import annotations

import pygame

from osmviz.animation import Simulation, SimViz, TrackingViz

# Our goal is to show a train lassoed to Denver, running around it.

red = pygame.Color("red")


class LassoViz(SimViz):
    """
    LassoViz draws a line between two (optionally moving) locations.
    """

    def __init__(
        self,
        get_loc_at_time1,
        get_loc_at_time2,
        line_color=red,
        line_width: int = 3,
        drawing_order: int = 0,
    ) -> None:
        """
        get_loc_at_time 1 and 2 represent the location of the 1st and 2nd
        endpoint of this lasso, respectively. They should take a single
        argument (time) and return the (lat,lon) of that endpoint.
        """
        SimViz.__init__(self, drawing_order)
        self.xy1 = None
        self.xy2 = None
        self.line_color = line_color
        self.line_width = line_width
        self.get_loc1 = get_loc_at_time1
        self.get_loc2 = get_loc_at_time2

    def set_state(self, sim_time, get_xy) -> None:
        self.xy1 = get_xy(*self.get_loc1(sim_time))
        self.xy2 = get_xy(*self.get_loc2(sim_time))

    def draw_to_surface(self, surf) -> None:
        pygame.draw.line(surf, self.line_color, self.xy1, self.xy2, self.line_width)

    # So long as we are passing LassoViz's in as part of the scene_viz
    # list to a Simulation, we don't need to implement the getLabel,
    # getBoundingBox, or mouseIntersect methods.


class TiedTrain(TrackingViz):
    """
    TiedTrain shows a train tied to a certain location, running around
    it at a specified distance and frequency.
    This is partly meant to demonstrate that it's ok to override
    the TrackingViz class, too (in fact it's usually easier).
    """

    def __init__(
        self,
        tie_post,
        lat_dist,
        lon_dist,
        frequency,
        time_window,
        label,
        drawing_order: int = 0,
        image: str = "images/train.png",
    ) -> None:
        self.clat, self.clon = tie_post
        self.lat_dist = lat_dist
        self.lon_dist = lon_dist
        self.frequency = int(frequency)

        TrackingViz.__init__(
            self,
            label,
            image,
            self.get_loc_at_time,
            time_window,
            (
                self.clat - self.lat_dist,
                self.clat + self.lat_dist,
                self.clon - self.lon_dist,
                self.clon + self.lon_dist,
            ),
            drawing_order,
        )

    def get_loc_at_time(self, time):
        phase = float(time % self.frequency) / self.frequency
        if phase < 0.25:
            blat = self.clat - self.lat_dist
            elat = self.clat + self.lat_dist
            blon = elon = self.clon - self.lon_dist
            frac = phase / 0.25
        elif phase < 0.5:
            blat = elat = self.clat + self.lat_dist
            blon = self.clon - self.lon_dist
            elon = self.clon + self.lon_dist
            frac = (phase - 0.25) / 0.25
        elif phase < 0.75:
            blat = self.clat + self.lat_dist
            elat = self.clat - self.lat_dist
            blon = elon = self.clon + self.lon_dist
            frac = (phase - 0.5) / 0.25
        else:
            blat = elat = self.clat - self.lat_dist
            blon = self.clon + self.lon_dist
            elon = self.clon - self.lon_dist
            frac = (phase - 0.75) / 0.25
        return blat + frac * (elat - blat), blon + frac * (elon - blon)


denver = 39.756111, -104.994167
train = TiedTrain(denver, 5.0, 5.0, 60, (0, 600), "Denver Bound")
lasso = LassoViz(train.get_loc_at_time, lambda t: denver)

sim = Simulation([train], [lasso], 0)
sim.run(refresh_rate=0.01, speed=1, osm_zoom=7)
