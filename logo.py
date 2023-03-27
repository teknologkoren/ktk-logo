from math import cos, sin, radians
from dataclasses import dataclass

import svgwrite

# https://cdn.thskth.se/wp-content/uploads/2016/07/Brandbook_digital.pdf
# page 19, 3.2 Emblem
circle_radius = 62.5      # THS: Circle diameter 125px

n_rings = 7
ring_inner_radius = 32.5  # THS: Inner diameter 65px
ring_width = 7.5          # THS: Outer diameter 40px
rings_x_offset = 0
rings_y_offset = 20

ring_radius = ring_inner_radius + ring_width / 2


def circle_coords(r, theta):
    theta_rads = radians(theta)
    return (r * sin(theta_rads), r * cos(theta_rads))


def ring_coords(n_rings, circle_radius):
    rings = []
    for i in range(n_rings):
        theta = (360 / n_rings * i) % 360
        x, y = circle_coords(circle_radius, theta)
        rings.append((x, y))
    return rings


def ring_min_coords(rings):
    ring_it = iter(rings)
    x_min, y_min = next(ring_it)
    for x, y in ring_it:
        x_min = min(x, x_min)
        y_min = min(y, y_min)
    return (x_min, y_min)


def ring_shapes(rings, x_offset, y_offset, x_min, y_min):
    ring_shapes = []
    for ring_coords in rings:
        x = ring_coords[0] + ring_radius + ring_width/2 + x_offset - x_min
        y = ring_coords[1] + ring_radius + ring_width/2 + y_offset - y_min
        ring = svgwrite.shapes.Circle(
            (x, y),
            r=ring_radius,
            fill="none",
            stroke="black",
            stroke_width=ring_width
        )
        ring_shapes.append(ring)
    return ring_shapes


@dataclass
class ForkDimensions:
    fork_width: float = None
    fork_offset: float = None
    prong_height: float = None
    prong_width: float = None
    stem_height: float = None


def fork_dimensions(fork_height, logo_width):
    d = ForkDimensions()
    d.fork_width = fork_height / 6.4
    d.fork_offset = logo_width / 2 - d.fork_width / 2
    d.prong_height = fork_height / 3 * 2.05
    d.prong_width = d.prong_height / 17
    d.stem_height = d.prong_height / 2
    return d


# attempt #1
def fork_path1(d: ForkDimensions):
    fork = svgwrite.path.Path(
        (
            f"M {d.fork_offset} 0 "
            f"v {d.prong_height} "
            f"c 0 {d.prong_height/7}, "
            f"  {d.fork_width} {d.prong_height/7}, "
            f"  {d.fork_width} 0 "
            f"v {-d.prong_height} "
            f"h {-d.prong_width} "
            f"v {d.prong_height} "
            f"c 0 {d.prong_height/7 - d.prong_width}, "
            f"  {-d.fork_width + d.prong_width*2} {d.prong_height/7 - d.prong_width}, "
            f"  {-d.fork_width + d.prong_width*2} 0 "
            f"v {-d.prong_height} "
        )
    )
    return fork


# attempt #2, refactor
def fork_path2(d: ForkDimensions):
    fork = svgwrite.path.Path(
        (
            f"M {d.fork_offset} 0 "
            f"v {d.prong_height} "
            f"q 0 {d.prong_height/7} "
            f"  {d.fork_width/2} {d.prong_height/7} "
            f"m {-d.prong_width/2} 0 "
            f"v 0 {d.stem_height} "
            f"h {d.prong_width} 0 "
            f"v 0 {-d.stem_height} "
        )
    )
    return fork


ring_cs = ring_coords(n_rings, circle_radius)
x_min, y_min = ring_min_coords(ring_cs)

width = (ring_radius + ring_width/2 - x_min) * 2 + rings_x_offset
height = circle_radius + ring_width + ring_radius * 2 + rings_y_offset - y_min
dwg = svgwrite.Drawing(
    'logo.svg',
    size=(width, height)
)
rings = ring_shapes(ring_cs, rings_x_offset, rings_y_offset, x_min, y_min)
for ring in rings:
    dwg.add(ring)

fd = fork_dimensions(height, width)
fork = fork_path2(fd)
dwg.add(fork)

dwg.save()
