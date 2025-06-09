from src.scenes.solver_scene import SolverScene
from src.algorithms.simulated_annealing import SimulatedAnnealing
from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import get_circular_sector_as_polygon, polygon_area
from src.ui import Button

import pygame
import numpy as np


class SimulatedAnnealingScene(SolverScene):
    """
    Class for the Simulated Annealing scene
    """

    def __init__(
        self,
        manager,
        radius: float = 100,
        T0: float = 1000,
        alpha: float = 0.99,
        min_temp: float = 1e-3,
        max_iter: int = 1000,
    ):
        """
        Constructor for the SimulatedAnnealingScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.algorithm = None
        self.radius = radius
        self.T0 = T0
        self.alpha = alpha
        self.min_temp = min_temp
        self.max_iter = max_iter
        self.initial_solution = None

    def set_initial_solution(self, initial_solution):
        """
        Sets the initial solution for the algorithm

        Parameters
        ----------
        initial_solution: np.ndarray
            Initial solution to set
        """
        self.initial_solution = initial_solution

    def set_polygon(self, polygon):
        """
        Sets the polygon for the algorithm

        Parameters
        ----------
        polygon: Polygon
            Polygon to set
        """
        self.polygon = polygon
        self.polygon_area = polygon_area(polygon)
        self.algorithm = SimulatedAnnealing(
            np.array(polygon),
            radius=self.radius,
            T0=self.T0,
            alpha=self.alpha,
            min_temp=self.min_temp,
            max_iter=self.max_iter,
            initial_solution=self.initial_solution,
        )
        self.best_solution = self.algorithm.get_best()

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw on
        """
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (230, 230, 232), (5, 120, 790, 495), 0)
        pygame.draw.rect(screen, (0, 0, 0), (5, 120, 790, 495), 1)
        self.draw_description(screen)
        self.draw_area(screen)
        self.draw_status_text(screen)

        for button in self.buttons:
            button.draw(screen)
        if self.algorithm:
            # Plot the current solution area
            self.best_solution = self.algorithm.get_best()
            _, sections = calculate_fitness_area(
                self.polygon,
                self.best_solution[0],
                self.radius,
                return_polygon=True,
            )
            if len(sections) == 0:
                pygame.draw.circle(
                    screen,
                    (243, 250, 246),
                    self.best_solution[0],
                    self.radius,
                    0,
                )
            else:
                for section in sections:
                    if len(section) > 2:
                        # Plot the polygon and fill it
                        pygame.draw.polygon(screen, (243, 250, 246), section, 0)
                    else:
                        polygon = get_circular_sector_as_polygon(
                            self.best_solution[0], section[0], section[1]
                        )
                        pygame.draw.polygon(screen, (243, 250, 246), polygon, 0)

            # Plot the previous solutions
            for solution in self.algorithm.previous_solutions:
                pygame.draw.circle(
                    screen,
                    (158, 156, 156),
                    solution[0],
                    1,
                )

            # Plot the best solution point
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                self.best_solution[0],
                2,
            )

        # Plot the polygon
        if self.polygon:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 1)
