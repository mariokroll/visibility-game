import pygame
import random

from src.scenes import Scene
from src.ui import Button
from src.utils import load_polygons


class LoadPolygonScene(Scene):
    """
    Class for the Load Polygon scene
    """

    def __init__(self, manager):
        """
        Constructor for the LoadPolygonScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.description = [
            "Escoja el número de vértices del polígono a cargar y después pulse 'Continuar'"
        ]
        self.load_25 = Button(
            20,
            50,
            150,
            60,
            "25 vértices",
            (255, 230, 196),
            text_color=(0, 0, 0),
            action=self.load_polygon_action,
            font_size=18,
        )
        self.load_50 = Button(
            200,
            50,
            150,
            60,
            "50 vértices",
            (255, 230, 196),
            text_color=(0, 0, 0),
            action=self.load_polygon_action,
            font_size=18,
        )
        self.continue_button = Button(
            380,
            50,
            150,
            60,
            "Continuar",
            (255, 230, 196),
            text_color=(0, 0, 0),
            action=self.done_action,
            font_size=18,
        )
        self.polygon = []

    def handle_event(self, event):
        """
        Handles events for the LoadPolygonScene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        self.load_25.handle_event(event, 25)
        self.load_50.handle_event(event, 50)
        self.continue_button.handle_event(event)

    def update(self):
        """
        Updates the scene
        """
        if self.continue_button.is_hovered():
            if len(self.polygon) == 0:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.load_25.is_hovered() or self.load_50.is_hovered():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def load_polygon_action(self, num_vertices: int):
        """
        Action to load a polygon with a given number of vertices

        Parameters
        ----------
        num_vertices: int
            Number of vertices of the polygon to load

        Returns
        -------
        list
            List of points of the loaded polygon
        """
        num_vertices_str = str(num_vertices)
        file_path = f"./data/polygons_{num_vertices_str}.json"
        polygons = load_polygons(file_path)
        self.polygon = random.choice(polygons)

    def done_action(self):
        """
        Action to advance to the next scene
        """
        self.manager.set_scene("choose_algorithm")
        self.manager.current_scene.set_polygon(self.polygon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_description(self, screen):
        """
        Draws the description of the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 20)
        y_start = 20
        line_separation = 30
        for i, line in enumerate(self.description):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (20, y_start + i * line_separation))

    def draw(self, screen):
        """
        Draws the scene on the screen

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw on
        """
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (230, 230, 232), (5, 120, 790, 495), 0)
        pygame.draw.rect(screen, (0, 0, 0), (5, 120, 790, 495), 1)
        self.draw_description(screen)
        self.load_25.draw(screen)
        self.load_50.draw(screen)
        self.continue_button.draw(screen)
        if len(self.polygon) > 0:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 1)
            for point in self.polygon:
                pygame.draw.circle(screen, (255, 161, 161), point, 3)
