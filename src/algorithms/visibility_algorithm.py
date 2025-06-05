from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

import math


def compute_visibility_polygon(p, poly, eps=1e-9):
    """
    Compute the visibility polygon of point p = (px, py) inside a simple polygon poly.

    Args:
        poly: List of vertices [(x0,y0), (x1,y1), ..., (xn-1,yn-1)] in CCW or CW order.
        p: Tuple (px, py), a point strictly inside the polygon.
        eps: Tiny angle offset to handle rays that pass exactly through polygon vertices.

    Returns:
        List of points [(vx0,vy0), (vx1,vy1), ...] in CCW order forming the visibility polygon.
    """
    px, py = p

    # 1) Gather all ray angles: for each vertex, use angle, angle-eps, angle+eps
    angles = []
    for vx, vy in poly:
        base = math.atan2(vy - py, vx - px)
        angles += [base - eps, base, base + eps]

    # 2) For each angle cast a ray and find nearest intersection with any edge
    intersects = []
    for ang in angles:
        dx, dy = math.cos(ang), math.sin(ang)
        closest_t = float("inf")
        closest_pt = None

        # For each edge AB of the polygon
        for i in range(len(poly)):
            ax, ay = poly[i]
            bx, by = poly[(i + 1) % len(poly)]

            # Solve p + t·r = A + u·s
            # where r = (dx, dy), s = (bx-ax, by-ay)
            rx, ry = dx, dy
            sx, sy = bx - ax, by - ay
            rxs = rx * sy - ry * sx
            if abs(rxs) < 1e-12:
                # Ray and segment are parallel
                continue

            apx, apy = ax - px, ay - py
            t = (apx * sy - apy * sx) / rxs
            u = (apx * ry - apy * rx) / rxs

            # Intersection occurs if t>0 (in front of ray) and 0<=u<=1 (within segment)
            if t > 0 and 0.0 <= u <= 1.0:
                if t < closest_t:
                    closest_t = t
                    closest_pt = (px + t * rx, py + t * ry)

        if closest_pt is not None:
            intersects.append((ang, closest_pt))

    # 3) Sort intersections by angle
    intersects.sort(key=lambda x: x[0])

    # 4) Extract unique points (drop near-duplicates)
    vis_poly = []
    for _, pt in intersects:
        if (
            not vis_poly
            or math.hypot(pt[0] - vis_poly[-1][0], pt[1] - vis_poly[-1][1]) > 1e-6
        ):
            vis_poly.append(pt)
    vis_poly.append(vis_poly[0])  # Close the polygon

    # 5) Remove collinear points

    return vis_poly
