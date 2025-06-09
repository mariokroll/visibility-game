import pygame
import numpy as np

from src.polygon import Polygon
from src.ui import Button

from src.scenes.start_scene import StartScene
from src.scenes.choose_algorithm import ChooseAlgorithmScene
from src.scenes.scene_manager import SceneManager
from src.scenes.solver_scene import SolverScene
from src.scenes.menu_scene import MenuScene
from src.scenes.draw_polygon_scene import DrawPolygonScene
from src.scenes.create_polygon_scene import CreatePolygonScene
from src.scenes.load_polygon_scene import LoadPolygonScene
from src.scenes.apply_random_search_scene import ApplyRandomSearchScene
from src.scenes.genetic_algorithm_scene import GeneticAlgorithmScene
from src.scenes.tabu_search_scene import TabuSearchScene
from src.scenes.simulated_annealing_scene import SimulatedAnnealingScene

# from src.scenes.simulated_annealing_scene import SimulatedAnnealingScene


WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (193, 193, 193)


def button_clicked():
    print("Button clicked!")


def main():
    """
    Main function for the game
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aplicación interactiva")

    scene_manager = SceneManager()
    scene_manager.add_scene("start_scene", StartScene(scene_manager))
    scene_manager.add_scene("menu", MenuScene(scene_manager))
    scene_manager.add_scene("choose_algorithm", ChooseAlgorithmScene(scene_manager))
    scene_manager.add_scene("solver", SolverScene(scene_manager))
    scene_manager.add_scene("draw_polygon", DrawPolygonScene(scene_manager))
    scene_manager.add_scene("create_polygon", CreatePolygonScene(scene_manager))
    scene_manager.add_scene("load_polygon", LoadPolygonScene(scene_manager))
    scene_manager.add_scene("random_search", ApplyRandomSearchScene(scene_manager))
    scene_manager.add_scene("genetic_algorithm", GeneticAlgorithmScene(scene_manager))
    scene_manager.add_scene("tabu_search", TabuSearchScene(scene_manager))
    scene_manager.add_scene(
        "simulated_annealing", SimulatedAnnealingScene(scene_manager)
    )

    scene_manager.set_scene("start_scene")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)

        scene_manager.update()
        scene_manager.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
