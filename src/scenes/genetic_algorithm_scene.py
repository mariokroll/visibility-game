from src.scenes.solver_scene import SolverScene
from src.algorithms.genetic_algorithm import GeneticAlgorithm
from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import get_circular_sector_as_polygon, polygon_area

import pygame
import numpy as np


class GeneticAlgorithmScene(SolverScene):
    """
    Class for the Genetic Algorithm scene
    """

    def __init__(
        self,
        manager,
        population_size: int = 100,
        pc: float = 0.8,
        pm: float = 0.05,
        max_generations: int = 100,
        stagnation: int = 20,
    ):
        """
        Constructor for the GeneticAlgorithmScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.algorithm = None
        self.population_size = population_size
        self.pc = pc
        self.pm = pm
        self.max_generations = max_generations
        self.stagnation = stagnation

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
        self.algorithm = GeneticAlgorithm(
            np.array(polygon),
            radius=self.radius,
            population_size=self.population_size,
            pc=self.pc,
            pm=self.pm,
            max_generations=self.max_generations,
            stagnation=self.stagnation,
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
        for button in self.buttons:
            button.draw(screen)
        if self.algorithm:
            for point in self.algorithm.population:
                pygame.draw.circle(screen, (255, 0, 0), point, 2)
        if self.algorithm and self.algorithm.best_solution:
            self.best_solution = self.algorithm.best_solution
            if self.finished:
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
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                self.best_solution[0],
                3,
            )
        if self.polygon:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 1)
