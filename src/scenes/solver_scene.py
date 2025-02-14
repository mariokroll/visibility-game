import pygame
import numpy as np
from src.polygon import Polygon
from src.ui import Button
from src.scenes import Scene


class SolverScene(Scene):
    """
    Class for the solver scene
    """

    def __init__(self, manager):
        """
        Constructor for the SolverScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.polygon = None
        self.buttons = []

    def set_polygon(self, polygon):
        """
        Sets the polygon to solve

        Parameters
        ----------
        polygon: list
            Polygon to solve
        """
        self.polygon = Polygon(polygon)

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

    def update(self):
        """
        Updates the scene
        """
        pass

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the scene on
        """
        screen.fill((255, 255, 255))
        if self.polygon:
            self.polygon.draw(screen)
        for button in self.buttons:
            button.draw(screen)
