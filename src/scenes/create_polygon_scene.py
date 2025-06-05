import pygame
import numpy as np
import random

from src.scenes import Scene
from src.ui import Button, Slider
from src.utils import (
    save_polygon,
    point_inside_polygon,
    get_convex_hull,
    intersect_polygon,
)


class CreatePolygonScene(Scene):
    """
    Class for the create polygon scene
    """

    def __init__(self, manager):
        """
        Constructor for the CreatePolygonScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.polygon = []
        self.buttons = [
            Button(
                280,
                35,
                150,
                60,
                "Crear polígono",
                (255, 230, 196),
                (0, 0, 0),
                font_size=18,
                action=self.generate_polygon,
            ),
            Button(
                465,
                35,
                150,
                60,
                "Hecho",
                (255, 230, 196),
                (0, 0, 0),
                font_size=18,
                action=self.done_action,
            ),
        ]
        self.slider = Slider(
            20,
            60,
            200,
            10,
            10,
            50,
            25,
            title="Número de vértices",
            knob_color=(0, 200, 0),
            font_size=18,
            font_path="./fonts/nunito/Nunito-Regular.ttf",
        )
        self.drawed = False

    def handle_event(self, event):
        """
        Handles events of the scene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        for button in self.buttons:
            button.handle_event(event)
        self.slider.handle_event(event)
        self.save_button.handle_event(event, self.polygon)

    def generate_polygon(self):
        """
        Generates a polygon from the points
        """
        n = self.slider.get_value()
        uniform_distributed_points = [
            (random.randint(20, 780), random.randint(170, 550)) for _ in range(n)
        ]

        # Choose the first 3 points to create a triangle. It must not contain any other points inside.
        self.polygon, points = self.get_first_triangle(uniform_distributed_points)

        while len(points) > 0:
            # Select the next point to add to the polygon
            i = 0
            while i < len(points):
                ch = get_convex_hull(self.polygon + [points[i]])
                point_inside = False
                element = points.pop(i)
                for point in points:
                    if point_inside_polygon(ch, point, closed=False):
                        point_inside = True
                        break
                if not point_inside:
                    # Find suitable position to insert the point
                    self.polygon = self.insert_point_in_polygon(self.polygon, element)
                    break
                else:
                    points.insert(i, element)
                    i += 1
        self.polygon.append(self.polygon[0])

    def get_first_triangle(self, points: list) -> tuple[list, list]:
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
                if point_inside_polygon(
                    triangle + [points[i]], points[j], closed=False
                ):
                    break
            else:
                triangle.append(points[i])
                points.remove(points[i])
                return triangle, points

    def insert_point_in_polygon(self, polygon: list, point: tuple) -> list:
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

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the scene on
        """
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (230, 230, 232), (5, 120, 790, 495), 0)
        pygame.draw.rect(screen, (0, 0, 0), (5, 120, 790, 495), 1)

        for button in self.buttons:
            button.draw(screen)
        self.slider.draw(screen)
        if len(self.polygon) > 0:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 1)
        for point in self.polygon:
            pygame.draw.circle(screen, (255, 161, 161), point, 3)

    def update(self):
        """
        Updates the scene
        """
        hovering = any(button.is_hovered() for button in self.buttons)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
        )

    def get_polygon(self):
        """
        Returns the polygon drawn

        Returns
        -------
        list
            List of points of the polygon
        """
        return self.polygon

    def done_action(self):
        """
        Action to perform when the done button is clicked
        """
        self.manager.set_scene("choose_algorithm")
        self.manager.current_scene.set_polygon(self.polygon)
