import pygame
import numpy as np

from src.algorithms.random_search import RandomSearch
from src.scenes import Scene
from src.ui import Button


class ApplyRandomSearchScene(Scene):
    """
    Class for the Apply Random Search scene
    """

    def __init__(self, manager, max_iter=100):
        """
        Constructor for the ApplyRandomSearchScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        radius: float
            Radius of the circular sector to sample points from
        max_iter: int
            Maximum number of iterations
        """
        super().__init__(manager)
        self.algorithm = None
        self.rs = None
        self.radius = None
        self.max_iter = max_iter
        self.description_lines = [
            "¿Quieres aplicar el algoritmo de búsqueda aleatoria",
            "antes de correr el algoritmo?",
        ]
        self.buttons = [
            Button(
                150,
                300,
                200,
                120,
                "Aplicar",
                font_size=32,
                action=self.solve,
                text_color=(0, 0, 0),
                border_radius=20,
            ),
            Button(
                450,
                300,
                200,
                120,
                "No aplicar",
                font_size=32,
                action=self.solve_without_applying,
                border_radius=20,
                text_color=(0, 0, 0),
            ),
        ]

    def set_radius(self, radius):
        """
        Sets the radius for the algorithm

        Parameters
        ----------
        radius: float
            Radius of the circular sector to sample points from
        """
        self.radius = radius

    def set_polygon(self, polygon):
        """
        Sets the polygon for the algorithm

        Parameters
        ----------
        polygon: np.ndarray
            Polygon to set
        """
        self.polygon = polygon
        self.rs = RandomSearch(
            np.array(polygon), radius=self.radius, max_iter=self.max_iter
        )

    def set_algorithm(self, algorithm: str):
        """
        Sets the algorithm for the scene

        Parameters
        ----------
        algorithm: RandomSearch
            Algorithm to set
        """
        self.algorithm = algorithm

    def draw_description(self, screen):
        """
        Draws the description of the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 24)
        y_start = 50
        line_spacing = 35
        for i, line in enumerate(self.description_lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(400, y_start + i * line_spacing))
            screen.blit(text, text_rect)

    def update(self):
        """
        Updates the scene
        """
        hovering = any(button.is_hovered() for button in self.buttons)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
        )

    def solve(self):
        """
        Solves the Random Search algorithm and changes the scene
        """
        self.rs.run()
        best_solution, _ = self.rs.get_best()
        self.manager.set_scene(self.algorithm)
        self.manager.current_scene.set_radius(self.radius)
        self.manager.current_scene.set_initial_solution(best_solution)
        self.manager.current_scene.set_polygon(self.polygon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def solve_without_applying(self):
        """
        Returns to the solver scene without applying the Random Search algorithm
        """
        self.manager.set_scene(self.algorithm)
        self.manager.current_scene.set_radius(self.radius)
        self.manager.current_scene.set_polygon(self.polygon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
            Screen to draw on
        """
        screen.fill((255, 255, 255))
        self.draw_description(screen)

        for button in self.buttons:
            button.draw(screen)
