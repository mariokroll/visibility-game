import pygame
import numpy as np
import random

from src.scenes import Scene
from src.ui import Button, Slider
from src.utils import order_points, save_polygon


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
                300,
                35,
                150,
                60,
                "Dibujar polígono",
                (0, 0, 255),
                (255, 255, 255),
                font_size=20,
                action=self.generate_polygon,
            ),
        ]
        self.save_button = Button(
            500,
            35,
            150,
            60,
            "Guardar polígono",
            (0, 0, 255),
            (255, 255, 255),
            font_size=20,
            action=save_polygon,
        )
        self.slider = Slider(50, 50, 200, 15, 10, 50, 25, title="Número de vértices")
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
        vertex = [
            (random.randint(100, 600), random.randint(100, 600)) for _ in range(n)
        ]
        self.polygon = order_points(vertex)

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the scene on
        """
        screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(screen)
        self.slider.draw(screen)
        self.save_button.draw(screen)
        if len(self.polygon) > 0:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 3)
        for point in self.polygon:
            pygame.draw.circle(screen, (255, 0, 0), point, 3)
