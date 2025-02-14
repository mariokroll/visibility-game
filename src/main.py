import pygame
import numpy as np

from src.polygon import Polygon
from src.ui import Button

from src.scenes.choose_algorithm import ChooseAlgorithmScene
from src.scenes.scene_manager import SceneManager
from src.scenes.solver_scene import SolverScene
from src.scenes.menu_scene import MenuScene
from src.scenes.draw_polygon_scene import DrawPolygonScene
from src.scenes.create_polygon_scene import CreatePolygonScene


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
    scene_manager.add_scene("menu", MenuScene(scene_manager))
    scene_manager.add_scene("choose_algorithm", ChooseAlgorithmScene(scene_manager))
    scene_manager.add_scene("solver", SolverScene(scene_manager))
    scene_manager.add_scene("draw_polygon", DrawPolygonScene(scene_manager))
    scene_manager.add_scene("create_polygon", CreatePolygonScene(scene_manager))

    scene_manager.set_scene("menu")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)

        scene_manager.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
