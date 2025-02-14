import pygame
import numpy as np


class Polygon:
    """
    Class to represent a polygon

    Attributes
    ----------
    vertices: list
        List of vertices of the polygon (x, y)
    color: tuple
        Color of the polygon (r, g, b)
    """

    def __init__(self, vertices, color=(0, 0, 0)):
        """
        Constructor for the Polygon class

        Parameters
        ----------
        vertices: list
            List of vertices of the polygon (x, y)
        color: tuple
            Color of the polygon (r, g, b)
        """
        self.vertices = vertices
        self.color = color

    def draw(self, screen):
        """
        Method to draw the polygon on the screen

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the polygon on
        """
        pygame.draw.polygon(screen, self.color, self.vertices, 2)
        