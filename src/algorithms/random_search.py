import numpy as np

from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import point_inside_polygon


class RandomSearch:
    """
    Class for the Random Search algorithm
    """

    def __init__(self, polygon, radius=100, max_iter=100):
        """
        Constructor for the RandomSearch class

        Parameters
        ----------
        polygon: np.ndarray
            Polygon to optimize
        radius: float
            Radius of the circular sector to sample points from
        max_iter: int
            Maximum number of iterations
        """
        self.polygon = polygon
        self.radius = radius
        self.best_solution = None
        self.best_fitness = -np.inf
        self.max_iter = max_iter
        self.closed_polygon = np.allclose(np.array(polygon[0]), np.array(polygon[-1]))

    def _random_point(self):
        """
        Generate a random point inside the polygon using rejection sampling.

        Returns
        -------
        np.ndarray
            Random point inside the polygon.
        """
        min_x, min_y = np.min(self.polygon, axis=0)
        max_x, max_y = np.max(self.polygon, axis=0)
        while True:
            x = np.random.uniform(min_x, max_x)
            y = np.random.uniform(min_y, max_y)
            if point_inside_polygon(self.polygon, (x, y), closed=self.closed_polygon):
                return np.array([x, y])

    def run(self):
        """
        Runs the Random Search algorithm

        Returns
        -------
        tuple
            Best solution and its fitness
        """
        for _ in range(self.max_iter):
            point = self._random_point()
            fitness = calculate_fitness_area(self.polygon, point, self.radius)
            if fitness >= 2.0 * np.pi * self.radius**2:
                # If the fitness is greater than the full area, we can stop early
                self.best_solution = point
                self.best_fitness = fitness
                break
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_solution = point

    def get_best(self):
        """
        Returns the best solution found

        Returns
        -------
        tuple
            Best solution and its fitness
        """
        return self.best_solution, self.best_fitness
