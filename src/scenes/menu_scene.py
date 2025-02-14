import pygame
from src.scenes import Scene
from src.ui import Button


class MenuScene(Scene):
    """
    Class for the menu scene
    """

    def __init__(self, manager):
        """
        Constructor for the MenuScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.buttons = [
            Button(
                325,
                100,
                150,
                90,
                "Dibujar polígono",
                (0, 0, 255),
                (255, 255, 255),
                font_size=20,
                action=self.draw_polygon,
            ),
            Button(
                325,
                300,
                150,
                90,
                "Cargar polígono",
                (0, 0, 255),
                (255, 255, 255),
                font_size=20,
                action=self.load_polygon,
            ),
            Button(
                325,
                450,
                150,
                90,
                "Crear polígono",
                (0, 0, 255),
                (255, 255, 255),
                font_size=20,
                action=self.create_polygon,
            ),
        ]

    def load_polygon(self):
        """
        Loads a polygon from a file
        """
        self.manager.set_scene("load_polygon")

    def draw_polygon(self):
        """
        Draws a polygon
        """
        self.manager.set_scene("draw_polygon")

    def create_polygon(self):
        """
        Creates a polygon
        """
        self.manager.set_scene("create_polygon")

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

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the scene
        """
        screen.fill((193, 193, 193))
        for button in self.buttons:
            button.draw(screen)
