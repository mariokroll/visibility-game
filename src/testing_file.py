from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import (
    get_convex_hull,
    intersect_polygon,
    point_inside_polygon2,
    get_circular_sector_as_polygon,
    polygon_area,
)

import random
import matplotlib.pyplot as plt
import numpy as np
import json

random.seed(42)  # For reproducibility


def generate_polygon(n):
    """
    Generates a polygon from the points
    """
    uniform_distributed_points = [
        (random.randint(20, 780), random.randint(170, 550)) for _ in range(n)
    ]

    # Choose the first 3 points to create a triangle. It must not contain any other points inside.
    polygon, points = get_first_triangle(uniform_distributed_points)
    all_points = np.array(points.copy())
    problem = False
    tries = 0
    while len(points) > 0:
        tries += 1
        if tries > all_points.shape[0]:
            # Plot current polygon
            plt.plot(*zip(*polygon), marker="o")
            plt.plot(*zip(*all_points), marker="o", linestyle="None")
            plt.plot(*zip(*points), marker="1", linestyle="None")
            plt.show()
            print("Could not generate polygon")
            problem = True
        # Select the next point to add to the polygon
        i = 0
        while i < len(points):

            ch = get_convex_hull(polygon + [points[i]])
            point_inside = False
            element = points.pop(i)
            if problem:
                # Plot current polygon
                plt.plot(*zip(*polygon), marker="o")
                plt.plot(*zip(*all_points), marker="o", linestyle="None")
                plt.plot(*zip(*points), marker="1", linestyle="None")
                plt.plot(element[0], element[1], marker="x", color="red")
                plt.plot(*zip(*ch), marker="o", linestyle="None")
                plt.show()
            for point in points:
                if point_inside_polygon2(ch, point, closed=False):
                    point_inside = True
                    break
            if not point_inside:
                # Find suitable position to insert the point
                polygon = insert_point_in_polygon(polygon, element)
                break
            else:
                points.insert(i, element)
                i += 1
    polygon.append(polygon[0])
    return polygon


def get_first_triangle(points: list) -> tuple[list, list]:
    """
    Get the first triangle to create the polygon

    Parameters
    ----------
    points: list
        List of points to get the first triangle from

    Returns
    -------
    tuple[list, list]
        Tuple with the triangle and the rest of the points
    """
    triangle = points[:2]
    points = points[2:]
    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                continue
            if point_inside_polygon2(triangle + [points[i]], points[j], closed=False):
                break
        else:
            triangle.append(points[i])
            points.remove(points[i])
            return triangle, points


def insert_point_in_polygon(polygon: list, point: tuple) -> list:
    """
    Insert a point in the polygon in a suitable position. This means that at least
    one of the edges of the polygon must be completetly visible from the point.

    Parameters
    ----------
    polygon: list
        List of points of the polygon
    point: tuple
        Point to insert in the polygon

    Returns
    -------
    list
        List of points of the polygon with the new point inserted
    """
    for i in range(len(polygon)):
        line1 = [point, polygon[i]]
        line2 = [point, polygon[(i + 1) % len(polygon)]]
        if intersect_polygon(
            line1, polygon, closed=False, allow_vertex=False, line_is_infinite=False
        ) or intersect_polygon(
            line2, polygon, closed=False, allow_vertex=False, line_is_infinite=False
        ):
            continue
        else:
            # Insert the point in the polygon
            polygon.insert(i + 1, point)
            break
    return polygon


def poly_area(points: list) -> float:
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


if __name__ == "__main__":
    polygons = []
    for i in range(100):
        polygon = generate_polygon(25)
        polygons.append(polygon)
    with open("./data/polygons_25.json", "w") as f:
        json.dump(polygons, f)

    polygons = []
    for i in range(100):
        polygons.append(generate_polygon(50))
        print("Generated polygon", i + 1)

    with open("./data/polygons_50.json", "w") as f:
        json.dump(polygons, f)
