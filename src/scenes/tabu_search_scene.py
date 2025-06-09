from src.scenes.solver_scene import SolverScene
from src.algorithms.tabu_search import TabuSearch
from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import get_circular_sector_as_polygon, polygon_area
import pygame
import numpy as np


class TabuSearchScene(SolverScene):
    """
    Class for the Tabu Search scene
    """

    def __init__(
        self,
        manager,
        radius: float = 100,
        tabu_size: int = 15,
        max_iter: int = 200,
    ):
        """
        Constructor for the TabuSearchScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.algorithm = None
        self.radius = radius
        self.tabu_size = tabu_size
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
        self.algorithm = TabuSearch(
            np.array(polygon),
            radius=self.radius,
            tabu_size=self.tabu_size,
            max_iter=self.max_iter,
            initial_solution=self.initial_solution,
        )

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

        # Draw the best solution area
        if self.algorithm:
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

            # Draw the previous solution points
            for point in self.algorithm.previous_solutions:
                pygame.draw.circle(screen, (158, 156, 156), point, 1)

            # Draw the best solution point
            pygame.draw.circle(screen, (255, 0, 0), self.best_solution[0], 2)

        # Draw the polygon outline
        if self.polygon:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 1)
