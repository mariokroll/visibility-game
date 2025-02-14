import pygame
from src.scenes.scene_manager import SceneManager


class Scene:
    """
    Class to represent a scene
    """

    def __init__(self, manager: SceneManager):
        """
        Constructor for the Scene class

        Parameters
        ----------
        name: str
            Name of the scene
        """
        self.manager = manager

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events of the scene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        pass

    def update(self):
        """
        Updates the scene
        """
        pass

    def draw(self, screen: pygame.Surface):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the scene
        """
        pass
