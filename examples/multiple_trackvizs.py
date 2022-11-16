"""
This example demonstrates the animation of multiple icons
on a map using TrackingViz objects.
"""

from __future__ import annotations

from osmviz.animation import Simulation, TrackingViz

# The goal is to show 10 trains racing eastward across the US.

right_lon = -(68 + 39.0 / 60)
left_lon = -(118 + 15.0 / 60)
top_lat = 45 + 46.0 / 60
bottom_lat = 30 + 3.0 / 60

begin_time = 0
end_time = 60

image_f = "images/train.png"
zoom = 6
num_trains = 10

track_vizs = []


def make_interpolator(begin_ll, end_ll, begin_t, end_t):
    def ret(t):
        if t < begin_t:
            return begin_ll
        elif t > end_t:
            return end_ll
        else:
            blat, blon = begin_ll
            elat, elon = end_ll
            frac = float(t) / (end_t - begin_t)
            return blat + frac * (elat - blat), blon + frac * (elon - blon)

    return ret


for i in range(num_trains):
    lat = bottom_lat + i * (top_lat - bottom_lat) / (num_trains - 1)

    loc_at_time = make_interpolator(
        (lat, left_lon), (lat, right_lon), begin_time, end_time
    )

    tviz = TrackingViz(
        f"Train {i+1}",
        image_f,
        loc_at_time,
        (begin_time, end_time),
        (30, 46, -119, -68.5),
        1,
    )  # drawing order doesn't really matter here

    track_vizs.append(tviz)


sim = Simulation(track_vizs, [], 0)
sim.run(speed=1, refresh_rate=0.1, osm_zoom=zoom)
