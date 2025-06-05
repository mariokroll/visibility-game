import numpy as np
import random
from typing import List, Tuple
from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import point_inside_polygon


class TabuSearch:
    """
    Tabu Search for maximizing visibility area in a polygon.

    Methods:
    - step(): perform one iteration of the search
    - run(): execute until maximum iterations
    - get_best(): return current best solution (point, fitness)
    """

    def __init__(
        self,
        polygon: np.ndarray,
        radius: float,
        tabu_size: int = 50,
        max_iter: int = 200,
    ) -> None:
        """
        Constructor for TabuSearch.

        Parameters
        ----------
        polygon : np.ndarray
            Polygon vertices (N x 2 array).
        radius : float
            Radius of the visibility area.
        tabu_size : int, optional
            Size of the tabu list (default is 50).
        max_iter : int, optional
            Maximum number of iterations (default is 1000).
        """
        self.polygon = polygon
        self.radius = radius
        self.tabu_size = tabu_size
        self.max_iter = max_iter
        self.tabu_list = []  # list of recent points

        first_solution = self._random_point()
        first_fitness = self._evaluate(first_solution)
        self.best_solution = (first_solution, first_fitness)
        self.previous_solutions = []
        self.iteration = 0

    def _random_point(self):
        """
        Sample a random point inside the polygon using rejection sampling.

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
            candidate = np.array([x, y])
            if point_inside_polygon(self.polygon, candidate):
                return candidate

    def _evaluate(self, point: np.ndarray) -> float:
        """
        Evaluate the fitness of a point.
        The fitness is defined as the area of the visibility polygon
        from the point within a given radius.

        Returns
        -------
        float
            Fitness value (area of visibility polygon).
        """
        return calculate_fitness_area(self.polygon, point, self.radius)

    def _neighbors(self) -> List[np.ndarray]:
        """
        Generate a neighbor by small random move.

        Returns
        -------
        list[np.ndarray]
            Neighbor points.
        """
        p = self.best_solution[0]
        directions = np.array(
            [np.array([dx, dy]) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
        )
        random_advance = np.random.normal(0, 1, size=directions.shape)
        candidates = p + directions + random_advance
        # filter candidates to be inside the polygon
        neighbors = []
        for candidate in candidates:
            if point_inside_polygon(self.polygon, candidate):
                neighbors.append(candidate)
            else:
                # if candidate is outside, generate a new random point
                neighbors.append(self._random_point())
        return neighbors

    def step(self) -> bool:
        """
        Perform one iteration of Tabu Search.

        Returns
        -------
        bool
            True if a step was taken, False if max_iter reached."""
        if self.iteration >= self.max_iter:
            print("Max iterations reached.")
            return False  # no more steps
        neighbors = self._neighbors()
        best_fitness = -np.inf
        for candidate in neighbors:
            if any(np.allclose(candidate, t, atol=1e-6) for t in self.tabu_list):
                continue  # skip if candidate is in tabu list
            # evaluate candidate
            fitness = self._evaluate(candidate)
            if fitness >= np.pi * self.radius**2:
                self.iteration = self.max_iter
                self.best_solution = (candidate, fitness)
                print("Found optimal solution.")
                return False
            # update best
            if fitness > best_fitness:
                best_fitness = fitness
                self.best_solution = (candidate, fitness)
                updated = True
            # update tabu list
        if updated:
            self.previous_solutions.append(self.best_solution[0])
            self.tabu_list.append(self.best_solution[0])
            if len(self.tabu_list) > self.tabu_size:
                self.tabu_list.pop(0)
            if len(self.previous_solutions) > 100:
                self.previous_solutions.pop(0)
        self.iteration += 1
        return True

    def run(self) -> Tuple[np.ndarray, float]:
        """
        Execute Tabu Search until max_iter reached.

        Returns
        -------
        Tuple[np.ndarray, float]
            Best solution found (point, fitness).
        """
        while self.iteration < self.max_iter:
            self.step()
        print("Max iterations reached.")
        return self.get_best()

    def get_best(self) -> Tuple[np.ndarray, float]:
        """
        Return best found solution.

        Returns
        -------
        Tuple[np.ndarray, float]
            Best solution (point, fitness).
        """
        return self.best_solution
