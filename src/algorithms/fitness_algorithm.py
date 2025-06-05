from typing import List, Optional, Tuple
import numpy as np
from math import isclose, sqrt

from src.algorithms.visibility_algorithm import (
    compute_visibility_polygon,
)
from src.utils import get_circular_sector_as_polygon, polygon_area, intersect_polygon
import matplotlib.pyplot as plt


Point = Tuple[float, float]


def segment_circle_intersections(
    center: Point, radius: float, p0: Point, p1: Point, atol: float = 1e-9
) -> List[Point]:
    """
    Compute the intersection point(s) between a circle and a line segment.

    Parameters
    ----------
    center : (float, float)
        The circle's centre coordinates (cx, cy).
    radius : float
        Circle radius (non-negative).
    p0     : (float, float)
        Segment start point.
    p1     : (float, float)
        Segment end point.
    atol   : float, optional
        Absolute tolerance used when comparing to zero (helps numerical robustness).

    Returns
    -------
    List[Point]
        A list containing zero, one, or two intersection points.
        The list is empty if the segment does not hit the circle.
    """
    # Direction vector of the segment:  p(t) = p0 + t·d ,  t∈[0,1]
    dx, dy = d = (p1[0] - p0[0], p1[1] - p0[1])

    # Vector from circle centre to p0
    fx, fy = f = (p0[0] - center[0], p0[1] - center[1])

    # Quadratic coefficients:  (d·d) t² + 2(f·d) t + (f·f − r²) = 0
    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - radius * radius

    disc = b * b - 4 * a * c  # discriminant

    if disc < -atol:
        return []  # no intersection (outside tolerance)

    # One intersection (tangent) if discriminant ≈ 0
    if isclose(disc, 0.0, abs_tol=atol):
        t = -b / (2 * a)
        if 0.0 - atol <= t <= 1.0 + atol:
            return [(p0[0] + t * dx, p0[1] + t * dy)]
        return []

    # Two potential intersections
    sqrt_disc = sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)

    points: List[Point] = []
    for t in (t1, t2):
        if 0.0 - atol <= t <= 1.0 + atol:  # within segment?
            points.append((p0[0] + t * dx, p0[1] + t * dy))

    return points[::-1]  # First point return is the closest to p0


def calculate_fitness_area(
    polygon: np.ndarray, point: np.ndarray, radius: float, return_polygon: bool = False
) -> float | Tuple[float, np.ndarray]:
    """
    Calculate the area of visibility of a point inside a polygon with
    a given radius.

    Parameters
    ----------
    polygon : np.ndarray
        Polygon vertices.
    point : np.ndarray
        Point coordinates.
    radius : float
        Radius of the circle.
    return_polygon : bool, optional
        If True, return the polygon of visibility (default is False).

    Returns
    -------
    float
        Area of visibility.
    """
    if return_polygon:
        sections = []
    visibility_polygon = np.array(
        compute_visibility_polygon(point, polygon, eps=1e-9)
    )  # type: ignore

    atol = 1e-9
    intersection_points, new_polygon = intersect_circunference_polygon(
        point, radius, visibility_polygon
    )
    if intersection_points.shape[0] == 0:
        if return_polygon:
            return np.pi * radius**2, []
        return np.pi * radius**2  # No intersection, full area

    # Iterate for every pair of intersection points
    area = 0.0
    # plot_polygon(new_polygon, color="blue", marker="x")
    for i in range(intersection_points.shape[0]):
        p0 = intersection_points[i]
        p1 = intersection_points[(i + 1) % intersection_points.shape[0]]
        middle_point = (p0 + p1) / 2.0

        # Get the angle between the two segments
        v0 = p0 - point
        v1 = p1 - point
        dot = np.dot(v0, v1)
        det = np.linalg.det([v0, v1])
        angle = np.arctan2(det, dot)
        if angle > 0:
            intersection_point = intersect_polygon(
                [point, middle_point], new_polygon, semiline=True
            )
        else:
            middle_point_opposite = 2 * point - middle_point
            intersection_point = intersect_polygon(
                [point, middle_point_opposite], new_polygon, semiline=True
            )
            angle += np.pi * 2.0
        if np.linalg.norm(intersection_point - point) < radius:
            # TODO
            # Calculate the area of the polygon formed by the polygon vertices between
            # the intersection points and the point
            target_polygon = calculate_polygon(new_polygon, point, p0, p1, atol=atol)
            # print(target_polygon)
            area += polygon_area(np.array(target_polygon))
            # plot_polygon(np.array(target_polygon), color="green", marker="o")
            if return_polygon:
                sections.append(target_polygon)
        else:
            # Add the area of the circular sector
            area += radius**2 * angle / 2.0
            if return_polygon:
                sections.append(np.array([p0, p1]))
    if return_polygon:
        return (area, sections)
    # plt.show()
    return area


def calculate_fitness_area2(
    polygon: np.ndarray, point: np.ndarray, radius: float, return_polygon: bool = False
) -> float:
    """
    Calculate the area of visibility of a point inside a polygon with
    a given radius.

    Parameters
    ----------
    polygon : np.ndarray
        Polygon vertices.
    point : np.ndarray
        Point coordinates.
    radius : float
        Radius of the circle.

    Returns
    -------
    float
        Area of visibility.
    """
    visibility_polygon = np.array(
        compute_visibility_polygon(point, polygon, eps=1e-9)
    )  # type: ignore

    atol = 1e-9
    intersection_points, new_polygon_prov = intersect_circunference_polygon(
        point, radius, visibility_polygon
    )

    # REVIEW: TODO
    if intersection_points.shape[0] == 0:
        return np.pi * radius**2  # No intersection, full area

    if return_polygon:
        sections = []
    new_polygon_update = new_polygon_prov.tolist()[:-1]
    # Roll the polygon to start from the first intersection point
    for k in range(len(new_polygon_update)):
        if (
            np.linalg.norm(np.array(new_polygon_update[k]) - intersection_points[0])
            < atol
        ):
            new_polygon = np.roll(new_polygon_update, -k, axis=0)
            new_polygon = np.concatenate((new_polygon, new_polygon[:1]), axis=0)
            break
    i = 0  # Index of the next vertex in the polygon
    j = 0  # Index of the next intersection point
    area = 0.0
    # plot_polygon(new_polygon, color="blue", marker="x")
    n_intersection_points = intersection_points.shape[0]
    while i < new_polygon.shape[0] - 1:
        p0 = new_polygon[i]
        p1 = new_polygon[i + 1]
        if (
            np.linalg.norm(p1 - intersection_points[(j + 1) % n_intersection_points])
            < atol
        ):
            target_polygon = [point, p0, p1, point]
            area += polygon_area(np.array(target_polygon))
            if return_polygon:
                sections.append(np.array(target_polygon))

            i += 1
            j = (j + 1) % intersection_points.shape[0]
        elif np.linalg.norm(p1 - point) < radius:
            target_polygon = [point, p0]
            i += 1
            j = (j + 1) % intersection_points.shape[0]
            while np.linalg.norm(new_polygon[i] - intersection_points[j]) > atol:
                target_polygon.append(new_polygon[i])
                i += 1
            target_polygon.append(new_polygon[i])
            area += polygon_area(np.array(target_polygon))
            if return_polygon:
                sections.append(np.array(target_polygon))
            # plot_polygon(np.array(target_polygon), color="green", marker="o")
        else:
            # Add the area of the circular sector
            j = (j + 1) % intersection_points.shape[0]
            while np.linalg.norm(new_polygon[i] - intersection_points[j]) > atol:
                i += 1
            v0 = p0 - point
            v1 = new_polygon[i] - point
            dot = np.dot(v0, v1)
            det = np.linalg.det([v0, v1])
            angle = np.arctan2(det, dot)
            if angle < 0:
                angle += 2 * np.pi
            area += radius**2 * angle / 2.0
            if return_polygon:
                sections.append(np.array([p0, new_polygon[i]]))
    if return_polygon:
        return (area, sections)
    # plt.show()
    return area


def calculate_polygon(
    new_polygon: np.ndarray,
    point: np.ndarray,
    p0: np.ndarray,
    p1: np.ndarray,
    atol: float = 1e-9,
) -> np.ndarray:
    """
    Calculate the polygon formed by the intersection points and the point.

    Parameters
    ----------
    new_polygon : np.ndarray
        Polygon vertices.
    point : np.ndarray
        Point coordinates.
    p0 : np.ndarray
        First intersection point.
    p1 : np.ndarray
        Second intersection point.
    atol : float, optional
        Absolute tolerance used when comparing to zero (default is 1e-9).

    Returns
    -------
    np.ndarray
        Polygon vertices.
    """
    target_polygon = []
    for k in range(new_polygon.shape[0] - 1):
        if np.linalg.norm(new_polygon[k] - p0) < atol:
            target_polygon.append(new_polygon[k])
            break
    k += 1
    n = len(new_polygon)
    while np.linalg.norm(new_polygon[k % n] - p1) > atol:
        target_polygon.append(new_polygon[k % n])
        k += 1
    target_polygon.append(new_polygon[k % n])
    target_polygon.append(point)
    target_polygon.append(p0)
    return np.array(target_polygon)


def intersect_circunference_polygon(
    center: np.ndarray, r: float, polygon: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the intersection points between a circle and a polygon.

    Parameters
    ----------
    center : np.ndarray
        Center of the circle.
    r : float
        Radius of the circle.
    polygon : np.ndarray
        Polygon vertices.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing two elements:
        - intersection points (np.ndarray): Points where the circle intersects the polygon.
        - new polygon (np.ndarray): The polygon with the intersection points added.
        The new polygon is formed by the original polygon vertices and the intersection points.
    """
    intersection_points = []
    new_polygon = []
    for i in range(polygon.shape[0] - 1):
        p0 = polygon[i]
        new_polygon.extend([p0])
        p1 = polygon[(i + 1) % polygon.shape[0]]
        points = segment_circle_intersections(center, r, p0, p1)
        if len(points) > 0:
            intersection_points.extend(points)
            new_polygon.extend(points)
    new_polygon.append(polygon[-1])
    # plt.plot(polygon[:, 0], polygon[:, 1], "k--", marker="o")
    # plt.plot(center[0], center[1], "ro")
    # plt.show()
    return np.array(intersection_points), np.array(new_polygon)


import matplotlib.pyplot as plt


def plot_polygon(polygon: np.ndarray, color: str = "blue", marker="x") -> None:
    """
    Plot a polygon using matplotlib.

    Parameters
    ----------
    polygon : np.ndarray
        Polygon vertices.
    color : str, optional
        Color of the polygon (default is "blue").
    """
    plt.plot(polygon[:, 0], polygon[:, 1], color=color, marker=marker, linestyle="-")
    plt.fill(polygon[:, 0], polygon[:, 1], color=color, alpha=0.3)


# polygon = np.array(
#     [
#         [467, 27],
#         [4, 290],
#         [163, 5],
#         [585, 1],
#         [493, 45],
#         [554, 135],
#         [618, 235],
#         [637, 378],
#         [626, 435],
#         [604, 356],
#         [596, 247],
#         [591, 388],
#         [565, 241],
#         [502, 190],
#         [505, 235],
#         [528, 372],
#         [248, 560],
#         [79, 559],
#         [55, 531],
#         [149, 368],
#         [217, 221],
#         [305, 129],
#         [207, 278],
#         [341, 128],
#         [487, 222],
#         [467, 27],
#     ]
# )
# point = np.array([531, 131])
# radius = 100
# area = calculate_fitness_area(polygon, point, radius)
# area2 = calculate_fitness_area2(polygon, point, radius)
# print("Area of visibility:", area)
# print("Area of visibility2:", area2)
# # for section in sections:
# #     # print(section)
# #     if len(section) > 2:
# #         plot_polygon(section, color="green", marker="v")
# # else:
# #     new_section = get_circular_sector_as_polygon(point, section[0], section[1])
# #     plot_polygon(new_section, color="green", marker="o")
# plot_polygon(polygon, color="blue")
# plt.plot(point[0], point[1], "ro")
# plt.grid()
# plt.show()
