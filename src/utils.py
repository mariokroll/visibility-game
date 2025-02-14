import pygame
import numpy as np
import json


def sign(
    p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]
) -> float:
    """
    Determines the sign of the area of the triangle formed by three points

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
    line1: list[tuple[float, float]], line2: list[tuple[float, float]]
) -> bool:
    """
    Determines if two lines intersect

    Parameters
    ----------
    line1: list
        List of two points representing the first line
    line2: list
        List of two points representing the second line
    """
    p1, p2 = line1
    p3, p4 = line2

    d1 = sign(p3, p4, p1)
    d2 = sign(p3, p4, p2)
    d3 = sign(p1, p2, p3)
    d4 = sign(p1, p2, p4)

    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    if d1 == 0 and np.dot(p3, p4) <= np.dot(p1, p2):
        return True
    if d2 == 0 and np.dot(p3, p4) <= np.dot(p1, p2):
        return True
    if d3 == 0 and np.dot(p1, p2) <= np.dot(p3, p4):
        return True
    if d4 == 0 and np.dot(p1, p2) <= np.dot(p3, p4):
        return True

    return False


def intersect_polygon(
    line: list[tuple[float, float], tuple[float, float]],
    polygon: list[tuple[float, float]],
    closed=True,
) -> bool:
    """
    Determines if a line intersects a polygon

    Parameters
    ----------
    line: list
        List of two points representing the line
    polygon: list
        List of vertices of the polygon
    closed: bool
        If the polygon provided is closed (last point is connected to the first)
    """
    n = len(polygon)
    for i in range(n):
        if closed:
            p1 = polygon[i]
            p2 = polygon[(i + 1) % n]
        else:
            p1 = polygon[i]
            p2 = polygon[(i + 1) % n]
            if i == n - 1:
                break

        if intersect_line(line, [p1, p2]):
            return True

    return False


def order_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
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
    print("hey")
    with open(filename, "w") as file:
        json.dump(polygon, file)
