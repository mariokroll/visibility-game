# import pygame
import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from typing import Tuple, List, Optional


def sign(
    p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]
) -> float:
    """
    Determines the sign of the area of the triangle formed by three points.
    If used to calculate an angle, the vertex of the angle is p1.

    Parameters
    ----------
    p1: tuple
        First point
    p2: tuple
        Second point
    p3: tuple
        Third point

    Returns
    -------
    float
        Sign of the area of the triangle
    """
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


def intersect_line(
    line1: list[tuple[float, float]],
    line2: list[tuple[float, float]],
    allow_vertex=True,
    line1_is_infinite=False,
    line2_is_infinite=False,
) -> tuple[float, float] | None:
    """
    Determines if two lines intersect

    Parameters
    ----------
    line1: list
        List of two points representing the first line
    line2: list
        List of two points representing the second line
    allow_vertex: bool
        If the intersection is allowed at the vertices of the lines
    line1_is_infinite: bool
        If the first line is infinite
    line2_is_infinite: bool
        If the second line is infinite
    """
    p1, p2 = line1
    p3, p4 = line2

    vector1 = np.array(p2) - np.array(p1)
    vector2 = np.array(p4) - np.array(p3)

    denominator = np.cross(vector1, vector2)

    if denominator == 0:
        return None

    t1 = np.cross(np.array(p3) - np.array(p1), vector2) / denominator
    t2 = np.cross(np.array(p3) - np.array(p1), vector1) / denominator

    if line1_is_infinite and line2_is_infinite:
        if not allow_vertex:
            if t1 == 0 or t1 == 1 or t2 == 1 or t2 == 0:
                return None
        return (t1, t2)
    elif line1_is_infinite:
        if allow_vertex:
            return (t1, t2) if 0 <= t2 <= 1 else None
        return (t1, t2) if 0 < t2 < 1 else None
    elif line2_is_infinite:
        if allow_vertex:
            return (t1, t2) if 0 <= t1 <= 1 else None
        return (t1, t2) if 0 < t1 < 1 else None
    else:
        if allow_vertex:
            return (t1, t2) if 0 <= t1 <= 1 and 0 <= t2 <= 1 else None
        return (t1, t2) if 0 < t1 < 1 and 0 < t2 < 1 else None


def intersect_semiline_line(
    semiline: list[tuple[float, float], tuple[float, float]] | np.ndarray,
    line: list[tuple[float, float], tuple[float, float]] | np.ndarray,
    allow_vertex=True,
) -> tuple[float, float] | None:
    """
    Determines the intersection point between a semiline and a line

    Parameters
    ----------
    semiline: list
        List of two points representing the semiline. First one is consider the origin
    line: list
        List of two points representing the line
    allow_vertex: bool
        If the intersection is allowed at the vertices of the semiline
        and the line

    Returns
    -------
    t1: float
        Parameter of the intersection point on the semiline
    t2: float
        Parameter of the intersection point on the line
    """

    semiline_origin = semiline[0]
    semiline_direction = -(np.array(semiline[1]) - np.array(semiline[0]))
    line_origin = line[0]
    line_end = line[1]
    line_direction = np.array(line_end) - np.array(line_origin)

    # Check if the lines are parallel
    denominator = np.cross(line_direction, semiline_direction)
    if denominator == 0:
        return None

    t1 = (
        np.cross(line_direction, np.array(semiline_origin) - np.array(line_origin))
    ) / denominator
    t2 = (
        np.cross(semiline_direction, np.array(line_origin) - np.array(semiline_origin))
    ) / denominator
    if allow_vertex:
        return (t1, t2) if t1 >= 0 and 0 <= t2 <= 1 else None
    return (t1, t2) if t1 > 0 and 0 < t2 < 1 else None


def intersect_polygon(
    line: list[tuple[float, float], tuple[float, float]],
    polygon: list[tuple[float, float]],
    closed=True,
    allow_vertex=True,
    semiline=False,
    line_is_infinite=True,
) -> list[tuple[float, float]] | bool:
    """
    Determines if a line intersects a polygon

    Parameters
    ----------
    line: list
        List of two points representing the line. Can be a semiline, determined by another parameter
    polygon: list
        List of vertices of the polygon
    closed: bool
        If the polygon provided is closed (last point is connected to the first)
    allow_vertex: bool
        If the intersection is allowed at the vertices of the polygon
    semiline: bool
        If the line is a semiline
    line_is_infinite: bool
        If the line is infinite

    Returns
    -------
    tuple
        Intersection points, if any
    """
    n = len(polygon)
    intersection_points = []
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        if closed:
            if i == n - 1:
                break
        if semiline:
            intersection = intersect_semiline_line(line, [p1, p2], allow_vertex)
        else:
            intersection = intersect_line(
                line, [p1, p2], allow_vertex, line1_is_infinite=line_is_infinite
            )

        if intersection:
            _, t2 = intersection
            intersection_point = np.array(p1) + t2 * (np.array(p2) - np.array(p1))
            intersection_points.append(tuple(intersection_point))
    if intersection_points:
        intersection_points_without_duplicates = [intersection_points.pop(0)]
        for point in intersection_points:
            for i in range(len(intersection_points_without_duplicates)):
                if np.allclose(point, intersection_points_without_duplicates[i]):
                    break
            else:
                intersection_points_without_duplicates.append(point)
        return intersection_points_without_duplicates
    return False


def order_points_polygon(
    points: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """
    Orders the points of a polygon in clockwise order

    Parameters
    ----------
    points: list
        List of points of the polygon

    Returns
    -------
    list
        List of points ordered in clockwise order
    """
    right, left, up, down = [], [], [], []
    # Pick a point and remove it from the list
    point = points.pop(0)
    for p in points:
        if p[0] > point[0]:
            right.append(p)
        elif p[0] < point[0]:
            left.append(p)
        elif p[0] == point[0] and p[1] > point[1]:
            up.append(p)
        else:
            down.append(p)

    right = sorted(
        right,
        key=lambda x: [
            (x[1] - point[1]) / (x[0] - point[0]),
            np.linalg.norm(np.array(x) - np.array(point)),
        ],
    )
    left = sorted(
        left,
        key=lambda x: [
            (x[1] - point[1]) / (x[0] - point[0]),
            np.linalg.norm(np.array(x) - np.array(point)),
        ],
    )
    up = sorted(
        up,
        key=lambda x: [
            (x[0] - point[0]) / (x[1] - point[1]),
            np.linalg.norm(np.array(x) - np.array(point)),
        ],
    )
    down = sorted(
        down,
        key=lambda x: [
            (x[0] - point[0]) / (x[1] - point[1]),
            np.linalg.norm(np.array(x) - np.array(point)),
        ],
    )
    return [point] + right + up + left + down


def order_points(
    reference_point: tuple[float, float], points: list[tuple[float, float]]
) -> list[tuple[float, float]]:
    """
    Orders the points of a polygon in clockwise order

    Parameters
    ----------
    reference_point: tuple
        Reference point to order the points
    points: list
        List of points to order

    Returns
    -------
    list
        List of points ordered in clockwise order
    """
    right, left, up, down = [], [], [], []
    for p in points:
        if p[0] > reference_point[0]:
            right.append(p)
        elif p[0] < reference_point[0]:
            left.append(p)
        elif p[0] == reference_point[0] and p[1] > reference_point[1]:
            up.append(p)
        else:
            down.append(p)

    right = sorted(
        right,
        key=lambda x: [
            (x[1] - reference_point[1]) / (x[0] - reference_point[0]),
            np.linalg.norm(np.array(x) - np.array(reference_point)),
        ],
    )
    left = sorted(
        left,
        key=lambda x: [
            (x[1] - reference_point[1]) / (x[0] - reference_point[0]),
            np.linalg.norm(np.array(x) - np.array(reference_point)),
        ],
    )
    up = sorted(
        up,
        key=lambda x: [
            (x[0] - reference_point[0]) / (x[1] - reference_point[1]),
            np.linalg.norm(np.array(x) - np.array(reference_point)),
        ],
    )
    down = sorted(
        down,
        key=lambda x: [
            (x[0] - reference_point[0]) / (x[1] - reference_point[1]),
            np.linalg.norm(np.array(x) - np.array(reference_point)),
        ],
    )
    print(right, up, left, down)
    return right + up + left + down


def save_polygon(
    polygon: list[tuple[float, float]], filename: str = "data/polygons.json"
):
    """
    Saves a polygon to a file

    Parameters
    ----------
    polygon: list
        List of vertices of the polygon
    filename: str
        Name of the file to save the polygon
    """
    with open(filename, "w") as file:
        json.dump(polygon, file)


def load_polygons(filename: str) -> list[list[tuple[float, float]]]:
    """
    Loads a polygon from a file

    Parameters
    ----------
    filename: str
        Name of the file to load the polygon

    Returns
    -------
    list
        List of vertices of the polygon
    """
    with open(filename, "r") as file:
        return json.load(file)


def visibility_polygon(
    polygon: list[tuple[float, float]], point: tuple[float, float]
) -> list[tuple[float, float]]:
    """
    Returns the visibility polygon of a point inside a polygon

    Parameters
    ----------
    polygon: list
        List of vertices of the polygon
    point: tuple
        Point from which the visibility polygon is calculated

    Returns
    -------
    list
        List of vertices of the visibility polygon
    """
    vertices = []

    for vertex in polygon:
        semiline = [point, vertex]
        intersection = intersect_polygon(semiline, polygon, semiline=True)
        # plot_what_it_is_happening(semiline, intersection, vertex, point)
        # print(intersection, vertex)
        if intersection:
            closest_point = sorted(
                intersection,
                key=lambda x: np.linalg.norm(np.array(x) - np.array(point)),
            )
            if np.allclose(closest_point[0], vertex):
                vertices.append(np.array(vertex))
                if len(intersection) > 1:
                    vertices.append(np.array(closest_point[1], dtype=float))

    print(point, vertices)
    return order_points(point, vertices)


def plot_what_it_is_happening(
    semiline: list[tuple[float, float]],
    intersection: list[tuple[float, float]],
    vertex: tuple[float, float],
    point: tuple[float, float],
):
    """
    Plots the semiline and the intersection points

    Parameters
    ----------
    semiline: list
        List of two points representing the semiline. First one is consider the origin
    intersection: list
        List of intersection points
    vertex: tuple
        Vertex of the polygon
    point: tuple
        Point from which the visibility polygon is calculated
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 3)
    ax.set_aspect("equal")
    ax.plot(*zip(*semiline), marker="o", color="b", label="Semiline")
    if intersection:
        ax.plot(*zip(*intersection), marker="o", color="r", label="Intersection")
        ax.plot(vertex[0], vertex[1], marker="x", color="g", label="Vertex")
        ax.plot(point[0], point[1], marker="o", color="y", label="Point")
        plt.legend()
        plt.show()


def polygon_area(polygon: list[tuple[float, float]] | np.ndarray, closed=True) -> float:
    """
    Calculates the area of a polygon

    Parameters
    ----------
    polygon: list
        List of vertices of the polygon

    Returns
    -------
    float
        Area of the polygon
    """
    if isinstance(polygon, list):
        polygon = np.array(polygon)
    if closed:
        if np.allclose(polygon[0], polygon[-1]):
            polygon = polygon[:-1]
    x = polygon[:, 0]
    y = polygon[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def point_inside_polygon(
    polygon: list[tuple[float, float]] | np.ndarray,
    point: tuple[float, float] | np.ndarray,
    closed: bool = True,
) -> bool:
    """
    Determines if a point is inside a polygon using the ray-casting algorithm.

    Parameters
    ----------
    polygon: list
        List of vertices of the polygon, can be a numpy array or a list of tuples
    point: tuple
        Point to check, can be a numpy array or a tuple
    closed: bool
        If True, the polygon is considered closed (last point connects to the first)

    Returns
    -------
    bool
        True if the point is inside the polygon, False otherwise
    """
    x, y = point
    count = 0
    n = len(polygon)
    for i in range(n):
        if closed:
            if i == n - 1:
                break
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]

        if p1[1] > p2[1]:
            p1, p2 = p2, p1

        if y == p1[1] or y == p2[1]:
            y += 1e-10

        if p1[1] < y < p2[1]:
            x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
            if x_intersect > x:
                count += 1

    return count % 2 == 1


def get_convex_hull(
    points: list[tuple[float, float]], plot: bool = False
) -> list[tuple[float, float]] | np.ndarray:
    """
    Returns the convex hull of a set of points

    Parameters
    ----------
    points: list
        List of points to calculate the convex hull
    plot: bool
        If True, plot the convex hull

    Returns
    -------
    list
        List of points of the convex hull
    """
    points = np.array(points)
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    if plot:
        plt.plot(points[:, 0], points[:, 1], "o")
        for simplex in hull.simplices:
            plt.plot(
                points[simplex, 0], points[simplex, 1], "k-", lw=2, label="Convex Hull"
            )
        plt.show()
    return hull_points


def get_circular_sector_as_polygon(
    center: np.ndarray | Tuple[float, float],
    p0: np.ndarray | Tuple[float, float],
    p1: np.ndarray | Tuple[float, float],
    step: float = 0.01,
) -> np.ndarray:
    """
    Returns the circular sector as a polygon

    Parameters
    ----------
    center: np.ndarray | Tuple[float, float]
        Center of the circular sector
    p0: np.ndarray | Tuple[float, float]
        First point of the circular sector
    p1: np.ndarray | Tuple[float, float]
        Second point of the circular sector

    Returns
    -------
    np.ndarray
        Circular sector as a polygon
    """
    radius = np.linalg.norm(p0 - center)
    if isinstance(center, tuple):
        center = np.array(center)
    angle_p0 = np.arctan2(p0[1] - center[1], p0[0] - center[0])
    angle_p1 = np.arctan2(p1[1] - center[1], p1[0] - center[0])
    if angle_p0 < 0:
        angle_p0 += 2 * np.pi
    if angle_p1 < 0:
        angle_p1 += 2 * np.pi
    curr_angle = angle_p0
    points = [center]
    if angle_p0 > angle_p1:
        angle_p1 += 2 * np.pi
    while curr_angle < angle_p1:
        x = center[0] + radius * np.cos(curr_angle)
        y = center[1] + radius * np.sin(curr_angle)
        points.append((x, y))
        curr_angle += step
    points.append(p1)
    points.append(center)
    return np.array(points)
