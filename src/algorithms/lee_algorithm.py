import numpy as np
from typing import Any, Tuple, Union, List, Dict
from src.utils import sign, intersect_line, intersect_semiline_line


def is_right_turn(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> bool:
    """
    Check if p3 is on the right of the line formed by p1 and p2.
    This is used to determine the orientation of the turn.

    Parameters
    ----------
    p1 : np.ndarray
        The first point.
    p2 : np.ndarray
        The second point.
    p3 : np.ndarray
        The third point.

    Returns
    -------
    bool
        True if the turn is a right turn, False otherwise.
    """
    # Calculate the cross product of the vectors p1p2 and p1p3
    cross_product = np.cross(p2 - p1, p3 - p1)
    return cross_product < 0  # Right turn if cross product is negative


def is_left_turn(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> bool:
    """
    Check if p3 is on the left of the line formed by p1 and p2.
    This is used to determine the orientation of the turn.

    Parameters
    ----------
    p1 : np.ndarray
        The first point.
    p2 : np.ndarray
        The second point.
    p3 : np.ndarray
        The third point.

    Returns
    -------
    bool
        True if the turn is a left turn, False otherwise.
    """
    # Calculate the cross product of the vectors p1p2 and p1p3
    cross_product = np.cross(p2 - p1, p3 - p1)
    return cross_product > 0  # Left turn if cross product is positive


def shift_to_origin(reference: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    Shift the points to the origin based on the reference point.

    Parameters
    ----------
    reference : np.ndarray
        The reference point to shift around.
    points : np.ndarray
        The points to be shifted.

    Returns
    -------
    np.ndarray
        The shifted points.
    """
    return points - reference  # Shift points to origin


def rotate_points_to_closer(
    reference: np.ndarray, points: np.ndarray, sort: True
) -> np.ndarray:
    """
    Find the point closest to the reference point and rotate the points accordingly, so that the closest point is
    aligned witht the x-axis

    Parameters
    ----------
    reference : np.ndarray
        The reference point to rotate around.
    points : np.ndarray
        The points to be rotated. They are already shifted to the origin.
    sort : bool
        If True, the points' order will be preserved, but with the closest point to the reference point being the first point.

    Returns
    -------
    np.ndarray
        The rotated points.
    """
    # Find the point closest to the reference point
    distances = np.linalg.norm(points - reference, axis=1)
    closest_index = np.argmin(distances)

    # Get the closest point
    closest_point = points[closest_index]

    # Calculate the angle to rotate
    angle = np.arctan2(closest_point[1], closest_point[0])

    # Create the rotation matrix
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )

    # Rotate the points
    rotated_points = points @ rotation_matrix.T

    rotated_points = np.concatenate([rotated_points, rotated_points[0:1]])

    if sort:
        # Sort the points to preserve the order, but with the closest point to the reference point being the first point
        rotated_points = np.roll(rotated_points[1:], -closest_index, axis=0)
        rotated_points = np.concatenate([rotated_points, rotated_points[0:1]])
    return rotated_points


def get_order_of_points(points: np.ndarray) -> bool:
    """
    Given a set of points, determine whether they are in clockwise or counter-clockwise order.

    Parameters
    ----------
    points : np.ndarray
        The points to be ordered.


    Returns
    -------
    bool
        True if the points are in counter-clockwise order, False otherwise.
    """
    # Determine a point in the convex hull of the points. The point with the lowest y-coordinate is used.
    # If there are multiple points with the same y-coordinate, the one with the lowest x-coordinate is used.
    index = np.argmin(points[:, 1])
    print("index", index)

    sign_value = sign(
        points[index - 1], points[index], points[(index + 1) % len(points)]
    )

    return sign_value < 0


def get_counter_clockwise_order(points: np.ndarray) -> np.ndarray:
    """
    Given a set of points, return the points in counter-clockwise order.

    Parameters
    ----------
    points : np.ndarray
        The points to be ordered.


    Returns
    -------
    np.ndarray
        The points in counter-clockwise order.
    """
    # Check if the points are in counter-clockwise order
    if get_order_of_points(points):
        return points

    # If not, reverse the order of the points
    return np.flip(points, axis=0)


def get_angles(
    points: np.ndarray, reference: np.ndarray = np.array([0, 0])
) -> tuple[np.ndarray, List[bool]]:
    """
    Calculates the angles of the points with respect to the x-axis, following
    Lee's algorithm. Following Lee's algorithm, points should be shifted to the origin
    and rotated to the closest point to the reference point.
    The angles are calculated in radians. Points must be in counter-clockwise order.

    Parameters
    ----------
    points : np.ndarray
        The points to calculate the angles for.
    reference : np.ndarray, optional
        The reference point to calculate the angles from, by default np.array([0, 0]).

    Returns
    -------
    np.ndarray
        The angles of the points with respect to the x-axis.
    turns : List[bool]
        A list of booleans indicating whether the points are turning left or right. True for left turn, False for right turn.
    """
    print(points.shape)
    return_points = np.zeros(points.shape[0])
    print(return_points.shape)
    for i in range(1, points.shape[0]):
        # Determine whether it is a left turn or a right turn.
        prev_vector = points[i - 1] - reference
        curr_vector = points[i] - reference
        turn_sign = np.cross(prev_vector, curr_vector)
        return_points[i] = return_points[i - 1]
        if turn_sign == 0:
            continue

        angle = np.arccos(
            np.dot(prev_vector, curr_vector)
            / (np.linalg.norm(prev_vector) * np.linalg.norm(curr_vector))
        )
        if turn_sign > 0:
            return_points[i] += angle
        else:
            return_points[i] -= angle
    return return_points


def _point_at_infinity(theta: float, r: float = 1e9) -> tuple[float, float]:
    return (r * np.cos(theta), r * np.sin(theta))


def get_visibility_polygon(
    points_list: List[tuple[float, float]], candidate_point: tuple[float, float]
) -> np.ndarray:
    """
    Given a set of points of a polygon, return the visibility polygon of the points.

    Parameters
    ----------
    points : np.ndarray | List[tuple[float, float]]
        The points of the polygon.


    Returns
    -------
    np.ndarray
        The visibility polygon of the points.
    """
    # Convert the points to a numpy array
    points = np.array(points_list)
    candidate = np.array(candidate_point)

    # Shift the points to the origin
    shifted_points = shift_to_origin(candidate, points[1:])

    # Rotate the points to the closest point
    rotated_points = rotate_points_to_closer(candidate, shifted_points, sort=True)

    # Get points in counter-clockwise order
    ordered_points = get_counter_clockwise_order(rotated_points)
    print(ordered_points.shape)

    # Get the angles of the points
    angles = get_angles(ordered_points)

    # Get the visibility polygon
    i, t = 0, 0
    inf_point = _point_at_infinity(angles[0])
    w = np.array([inf_point[0], inf_point[1], angles[0]])
    stack = [[ordered_points[0], angles[0]]]
    if angles[1] >= angles[0]:
        upcase = "advance"
    else:
        upcase = "scan"
        ccw = True
    while upcase != "done":
        if upcase == "advance":
            # Advance the visibility polygon algorithm
            stack, i, t, upcase, ccw, w = _advance(
                candidate, ordered_points, stack, angles, i, t, upcase, ccw, w
            )
        elif upcase == "scan":
            # Scan the visibility polygon algorithm
            stack, i, t, upcase, ccw, w = _scan(
                candidate, ordered_points, stack, angles, i, t, upcase, ccw, w
            )
        elif upcase == "retard":
            stack, i, t, upcase, ccw, w = _retard(
                candidate, points, stack, angles, i, t, upcase, ccw, w
            )
    return stack


def _advance(
    candidate: np.ndarray,
    points: np.ndarray,
    stack: np.ndarray,
    angles: np.ndarray,
    i: int,
    t: int,
    upcase: str,
    ccw: bool,
    w: np.ndarray,
) -> Tuple[np.ndarray, int, int, str, bool, np.ndarray]:
    """
    Advance the visibility polygon algorithm.

    Parameters
    ----------
    candidate : np.ndarray
        The candidate point.
    points : np.ndarray
        The points of the polygon.
    stack : np.ndarray
        The stack of points.
    angles : np.ndarray
        The angles of the points.
    i : int
        The current i for the points.
    t : int
        The current t for the stack.
    upcase : str
        The current upcase.
    ccw : bool
        Whether the points are in counter-clockwise order.
    w : np.ndarray
        Arbitrary point

    Returns
    -------
    Tuple[np.ndarray, int, int, str, bool, np.ndarray]
        Updated stack, i, t, upcase, ccw and w values.
    """
    # Advance the visibility polygon algorithm.
    while upcase == "advance":
        if angles[i + 1] <= np.pi * 2:
            i += 1
            t += 1
            stack = np.concatenate([stack, [points[i], angles[i]]])
            if i == len(points) - 1:
                upcase = "done"
            elif angles[i + 1] < angles[i] and is_right_turn(
                points[i - 1], points[i], points[i + 1]
            ):
                upcase = "scan"
                ccw = True
                inf_point = _point_at_infinity(angles[i])
                w = np.array([inf_point[0], inf_point[1], angles[i]])
            elif angles[i + 1] > angles[i] and is_left_turn(
                points[i - 1], points[i], points[i + 1]
            ):
                upcase = "retard"
        else:
            if stack[t][1] < 2 * np.pi:
                intersection = intersect_line(
                    [points[i], points[i + 1]], [candidate, points[0]]
                )
                if intersection is not None:
                    intersection_angle = np.arctan2(
                        intersection[1] - candidate[1],
                        intersection[0] - candidate[0],
                    )
                    stack = np.concatenate(
                        [stack, [intersection, intersection_angle]], axis=0
                    )
                    t += 1
            upcase = "scan"
            ccw = False
            w = np.array([points[0][0], points[0][1], angles[0]])

    return stack, i, t, upcase, ccw, w


def _scan(
    candidate: np.ndarray,
    points: np.ndarray,
    stack: np.ndarray,
    angles: np.ndarray,
    i: int,
    t: int,
    upcase: str,
    ccw: bool,
    w: np.ndarray,
) -> Tuple[np.ndarray, int, int, str]:
    """
    Scan the visibility polygon algorithm.

    Parameters
    ----------
    candidate : np.ndarray
        The candidate point.
    points : np.ndarray
        The points of the polygon.
    stack : np.ndarray
        The stack of points.
    angles : np.ndarray
        The angles of the points.
    i : int
        The current i for the points.
    t : int
        The current t for the stack.
    upcase : str
        The current upcase.
    ccw : bool
        Whether the points are in counter-clockwise order.
    w : np.ndarray
        Arbitrary point

    Returns
    -------
    Tuple[np.ndarray, int, int, str]
        Updated stack, i, t and upcase values.
    """
    # Scan the visibility polygon algorithm.
    while upcase == "scan":
        i += 1
        if ccw and angles[i + 1] > stack[t][1] and stack[t][1] >= angles[i]:
            # Check if the next angle is greater than the last angle in the stack
            intersection = intersect_line(
                [points[i], points[i + 1]], [candidate, [w[0], w[1]]]
            )
            if intersection is not None:
                intersection_angle = np.arctan2(
                    intersection[1] - candidate[1],
                    intersection[0] - candidate[0],
                )
                stack = np.concatenate([stack, [intersection, intersection_angle]])
                t += 1
                upcase = "advance"
        elif not ccw and angles[i + 1] <= stack[t][1] and stack[t][1] < angles[i]:
            # Check if the next angle is less than the last angle in the stack
            intersection = intersect_line([points[i], points[i + 1]], [candidate, w[0]])
            if intersection is not None:
                upcase = "retard"

    return stack, i, t, upcase


def _retard(
    candidate: np.ndarray,
    points: np.ndarray,
    stack: np.ndarray,
    angles: np.ndarray,
    i: int,
    t: int,
    upcase: str,
    ccw: bool,
    w: np.ndarray,
) -> Tuple[np.ndarray, int, int, str, bool, np.ndarray]:
    """
    Retard procedure

    Parameters
    ----------
    candidate : np.ndarray
        The candidate point.
    points : np.ndarray
        The points of the polygon.
    stack : np.ndarray
        The stack of points.
    angles : np.ndarray
        The angles of the points.
    i : int
        The current i for the points.
    t : int
        The current t for the stack.
    upcase : str
        The current upcase.
    ccw : bool
        Whether the points are in counter-clockwise order.
    w : np.ndarray
        Arbitrary point

    Returns
    -------
    Tuple[np.ndarray, int, int, str, bool, np.ndarray]
        Updated stack, i, t, upcase, ccw and w values.
    """
    while upcase == "retard":
        j = t - 1
        while j > 0:
            intersection = intersect_line(
                [points[i], points[i + 1]], [stack[j], stack[j + 1]]
            )
            if (stack[j][1] < angles[i + 1] <= stack[j + 1][1]) or (
                angles[i + 1] <= stack[j][1]
                and stack[j][1] == stack[j + 1][1]
                and intersection is not None
            ):
                break
            j -= 1
        if stack[j][1] < angles[i + 1]:
            i += 1
            t += 1
            intersection = intersect_semiline_line(
                [candidate, points[i]], [stack[j][0], stack[j + 1][0]]
            )
            if intersection is not None:
                stack = np.concatenate([stack, [intersection, angles[i + 1]]])
                t += 1
                stack = np.concatenate([stack, [points[i], angles[i]]], axis=0)
            if i == len(points) - 1:
                upcase = "done"
            elif angles[i + 1] > angles[i] and is_right_turn(
                points[i - 1], points[i], points[i + 1]
            ):
                upcase = "advance"
            elif angles[i + 1] > angles[i] and is_left_turn(
                points[i - 1], points[i], points[i + 1]
            ):
                upcase = "scan"
                ccw = False
                w = np.array([points[i][0], points[i][0], angles[i]])
                t -= 1
            else:
                t -= 1
        else:
            if (
                angles[i + 1] == stack[j][1]
                and angles[i + 2] > angles[i + 1]
                and is_left_turn(points[i], points[i + 1], points[i + 2])
            ):
                upcase = "advance"
                i += 1
                t = j + 1
                stack = np.concatenate([stack, [points[i], angles[i]]])
            else:
                upcase = "scan"
                t = j
                ccw = True
                intersection = intersect_line(
                    [points[i], points[i + 1]], [stack[j], stack[j + 1]]
                )
    return stack, i, t, upcase, ccw, w


points = np.array([[0, 0], [2, 0], [2, 2], [1, 1], [0, 1], [0, 0]])
candidate = np.array([0.4, 0.6])
solution = get_visibility_polygon(points, candidate)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.plot(points[:, 0], points[:, 1], "ro-")
plt.plot(candidate[0], candidate[1], "bo")
plt.plot(solution[:, 0], solution[:, 1], "go-")

plt.gca().add_patch(patches.Polygon(solution, closed=True, fill=True, alpha=0.5))
plt.xlim(-1, 3)
plt.ylim(-1, 3)
plt.gca().set_aspect("equal", adjustable="box")
plt.grid()
plt.show()
