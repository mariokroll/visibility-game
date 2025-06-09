import numpy as np
import random
import math
from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import point_inside_polygon


class SimulatedAnnealing:
    """
    Simulated Annealing for maximizing visibility area.

    Methods:
    - step(): perform one annealing step
    - run(): execute until temperature threshold
    - get_best(): return best solution
    """

    def __init__(
        self,
        polygon: np.ndarray,
        radius: float,
        T0: float = 1.0,
        alpha: float = 0.999,
        min_temp: float = 1e-3,
        max_iter: int = 10000,
        initial_solution: np.ndarray = None,
    ) -> None:
        """
        Constructor for Simulated Annealing.

        Parameters
        ----------
        polygon : np.ndarray
            Polygon vertices (N x 2 array).
        radius : float
            Radius of the visibility area.
        T0 : float, optional
            Initial temperature (default is 1.0).
        alpha : float, optional
            Cooling rate (default is 0.99).
        min_temp : float, optional
            Minimum temperature (default is 1e-3).
        max_iter : int, optional
            Maximum number of iterations (default is 10000).
        """
        self.polygon = polygon
        self.radius = radius
        self.T = T0
        self.alpha = alpha
        self.min_temp = min_temp
        self.max_iter = max_iter
        self.iteration = 0
        if initial_solution is not None:
            first_point = initial_solution
        else:
            first_point = self._random_point()
        self.best_solution = (first_point, self._evaluate(first_point))
        self.previous_solutions = []

    def _random_point(self) -> np.ndarray:
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
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            if point_inside_polygon(self.polygon, (x, y)):
                return np.array([x, y])

    def _evaluate(self, point: np.ndarray) -> float:
        """
        Evaluate the fitness of a point.

        Parameters
        ----------
        point : np.ndarray
            Point to evaluate.

        Returns
        -------
        float
            Fitness value (area of visibility polygon).
        """
        return calculate_fitness_area(self.polygon, point, self.radius)

    def _neighbor(self) -> np.ndarray:
        """
        Generate a neighboring solution by perturbing the current solution.
        The perturbation is done by adding a small random delta to the current solution.

        Returns
        -------
        np.ndarray
            Neighboring solution (point).
        """
        delta = np.random.normal(scale=1.5, size=2)
        cand = self.best_solution[0] + delta
        if point_inside_polygon(self.polygon, cand):
            return cand
        return self._random_point()

    def step(self):
        """
        Perform one iteration of SA.

        Returns
        -------
        bool
            True if the algorithm should continue, False otherwise.
        """
        if self.T < self.min_temp or self.iteration >= self.max_iter:
            print("Done")
            return False
        cand = self._neighbor()
        f_new = self._evaluate(cand)
        if f_new >= np.pi * self.radius**2:
            self.best_solution = (cand, f_new)
            self.iteration = self.max_iter
            print("Done")
            return False
        delta = f_new - self.best_solution[1]
        if delta > 0 or random.random() < math.exp(delta / self.T):
            self.previous_solutions.append(self.best_solution)
            if len(self.previous_solutions) > 100:
                self.previous_solutions.pop(0)
            self.best_solution = (cand, f_new)
        self.T *= self.alpha
        self.iteration += 1
        return True

    def run(self):
        """
        Execute SA until stop criteria.

        Returns
        -------
        tuple
            Best solution found (point, fitness).
        """
        while self.step():
            pass
        print("Done")
        return self.get_best()

    def get_best(self):
        """
        Return best found solution (point, fitness).

        Returns
        -------
        tuple
            Best solution found (point, fitness).
        """
        return self.best_solution
