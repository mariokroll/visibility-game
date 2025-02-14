import pygame
from src.scenes import Scene
from src.scenes.scene_manager import SceneManager
from src.ui import Button


class ChooseAlgorithmScene(Scene):
    """
    Class for the choose algorithm scene
    """

    def __init__(self, manager: SceneManager):
        """
        Constructor for the ChooseAlgorithmScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.buttons = [
            Button(
                325,
                200,
                150,
                90,
                "Simulated Annealing",
                (0, 0, 255),
                (255, 255, 255),
                action=self.simulated_annealing,
            ),
            Button(
                325,
                400,
                150,
                90,
                "Genetic algorithms",
                (0, 0, 255),
                (255, 255, 255),
                action=self.genetic_algorithms,
            ),
            Button(
                325,
                600,
                150,
                90,
                "Tabu Search",
                (0, 0, 255),
                (255, 255, 255),
                action=self.tabu_search,
            ),
        ]

    def simulated_annealing(self):
        """
        Starts the simulated annealing algorithm
        """
        self.manager.set_scene("simulated_annealing")

    def genetic_algorithms(self):
        """
        Starts the genetic algorithms algorithm
        """
        self.manager.set_scene("genetic_algorithms")

    def tabu_search(self):
        """
        Starts the tabu search algorithm
        """
        self.manager.set_scene("tabu_search")

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
            Screen to draw the scene
        """
        for button in self.buttons:
            button.draw(screen)
