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
        self.radius = None
        self.buttons = [
            Button(
                10,
                80,
                120,
                30,
                "Resolver",
                font_size=17,
                action=self.solve,
                text_color=(0, 0, 0),
            ),
            Button(
                145,
                80,
                120,
                30,
                "1 iteración",
                font_size=17,
                text_color=(0, 0, 0),
                action=self.one_interation,
            ),
            Button(
                280,
                80,
                120,
                30,
                "10 iteraciones",
                font_size=17,
                text_color=(0, 0, 0),
                action=self.ten_iterations,
            ),
        ]
        self.algorithm = None
        self.finished = False
        self.description_lines = [
            "Pulse el botón 'Resolver' para obtener la solución del problema.",
            "Pulse el botón '1 iteración' para realizar una iteración del algoritmo.",
            "Pulse el botón '10 iteraciones' para realizar diez iteraciones del algoritmo.",
        ]
        self.best_solution = None
        self.area_text = "Área: "
        self.area = 0.0
        self.polygon_area = 0.0

    def set_polygon(self, polygon):
        """
        Sets the polygon to solve

        Parameters
        ----------
        polygon: list
            Polygon to solve
        """
        self.polygon = Polygon(polygon)

    def set_radius(self, radius):
        """
        Sets the radius of the polygon

        Parameters
        ----------
        radius: float
            Radius of the polygon
        """
        self.radius = radius

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
        hovering = any(button.is_hovered() for button in self.buttons)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
        )

    def one_interation(self):
        """
        Performs one iteration of the algorithm
        """
        if not self.algorithm.step():
            self.finished = True

    def ten_iterations(self):
        """
        Performs ten iterations of the algorithm
        """
        for _ in range(10):
            if not self.algorithm.step():
                self.finished = True
                break

    def solve(self):
        """
        Solves the problem completely
        """
        self.algorithm.run()
        self.finished = True

    def draw_description(self, screen):
        """
        Draws the description of the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the description on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Light.ttf", 15)
        y_start = 15
        line_separation = 20
        for i, line in enumerate(self.description_lines):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (20, y_start + i * line_separation))

    def draw_area(self, screen):
        """
        Draws the text showing the area of the polygon

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the area text on
        """
        if self.best_solution:
            # Plot total area of the polygon
            self.area = self.best_solution[1]
            area_text = f"{self.area_text}{self.area:.2f}"
            font = pygame.font.Font("./fonts/nunito/Nunito-Light.ttf", 15)
            text = font.render(area_text, True, (0, 0, 0))
            screen.blit(text, (550, 15))

            # Plot the percentage of the area covered by the solution
            if self.polygon_area > 0:
                percentage = (self.area / self.polygon_area) * 100
                percentage_text = f"Área cubierta: {percentage:.2f}%"
                text = font.render(percentage_text, True, (0, 0, 0))
                screen.blit(text, (550, 35))

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
