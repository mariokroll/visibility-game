import numpy as np
import random
from src.algorithms.fitness_algorithm import calculate_fitness_area
from src.utils import point_inside_polygon
from matplotlib.path import Path
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    """
    Simple Genetic Algorithm for maximizing visibility area.

    Methods:
    - step(): perform one generation
    - run(): execute until stop condition
    - get_best(): return best solution
    """

    def __init__(
        self,
        polygon: np.ndarray,
        radius: float = 0.0,
        population_size: int = None,
        pc: float = 0.85,
        pm: float = 0.1,
        max_generations: int = 200,
        stagnation: int = 20,
    ) -> None:
        """
        Constructor for GeneticAlgorithm.

        Parameters
        ----------
        polygon : np.ndarray
            Polygon vertices (N x 2 array).
        radius : float
            Radius of the visibility area.
        population_size : int, optional
            Size of the population (default is number of vertices).
        pc : float, optional
            Crossover probability (default is 0.85).
        pm : float, optional
            Mutation probability (default is 0.1).
        max_generations : int, optional
            Maximum number of generations (default is 100).
        stagnation : int, optional
            Stagnation criteria (default is 20).
        """
        self.polygon = polygon
        self.radius = radius
        self.pc = pc
        self.pm = pm
        self.max_generations = max_generations
        self.stagnation = stagnation
        n = polygon.shape[0]
        self.population_size = population_size or n
        self.population = [self._random_point() for _ in range(self.population_size)]
        self.fitness = [self._evaluate(p) for p in self.population]
        self.best_solution = max(zip(self.population, self.fitness), key=lambda x: x[1])
        self.prev_best_fitness = 0
        self.generation = 0
        self.no_improve = 0

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
            if point_inside_polygon(self.polygon, (x, y), closed=False):
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

    def _select(self):
        """
        Roulette-wheel selection.

        Returns
        -------
        np.ndarray
            Selected parent point.
        """
        total = sum(self.fitness)
        pick = random.uniform(0, total)
        current = 0
        for p, f in zip(self.population, self.fitness):
            current += f
            if current >= pick:
                return p
        return self.population[-1]

    def _crossover(self, parent1, parent2):
        """
        Single-point crossover for 2D point: mix x and y with prob pc.

        Parameters
        ----------
        parent1 : np.ndarray
            First parent point.
        parent2 : np.ndarray
            Second parent point.

        Returns
        -------
        np.ndarray
            Child point after crossover.
        """
        if random.random() < self.pc:
            alpha = random.random()
            child = alpha * parent1 + (1 - alpha) * parent2
            if point_inside_polygon(self.polygon, child, closed=False):
                return child
        return parent1.copy()

    def _mutate(self, point):
        """
        Gaussian mutation.

        Parameters
        ----------
        point : np.ndarray
            Point to mutate.

        Returns
        -------
        np.ndarray
            Mutated point.
        """
        if random.random() < self.pm:
            point2 = point + np.random.normal(scale=1, size=2)
            if point_inside_polygon(self.polygon, point2, closed=False):
                return point2
        return point

    def step(self):
        """
        Perform one generation of GA.

        Returns
        -------
        bool
            True if the algorithm should continue, False otherwise.
        """
        if self.generation > self.max_generations or self.no_improve >= self.stagnation:
            return False
        new_pop = []
        new_fitness = []
        for _ in range(self.population_size):
            p1 = self._select()
            p2 = self._select()
            child = self._crossover(p1, p2)
            child = self._mutate(child)
            new_pop.append(child)
            new_child_fitness = self._evaluate(child)
            if new_child_fitness >= 2.0 * np.pi * self.radius**2:
                return False
            new_fitness.append(new_child_fitness)
        prev_best_fitness = self.best_solution[1]
        self.population = new_pop
        self.fitness = new_fitness
        self.best_solution = max(zip(self.population, self.fitness), key=lambda x: x[1])
        if self.best_solution[1] - prev_best_fitness > 5:
            self.no_improve = 0
        else:
            self.no_improve += 1
        self.generation += 1
        return True

    def run(self):
        """
        Execute GA until stopping criteria.

        Returns
        -------
        tuple
            Best solution found (point, fitness).
        """
        while (
            self.generation < self.max_generations and self.no_improve < self.stagnation
        ):
            self.step()
        print("Terminado")
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
