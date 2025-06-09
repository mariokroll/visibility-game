import pygame
from src.scenes import Scene
from src.scenes.scene_manager import SceneManager
from src.ui import Button, Slider


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
        self.polygon = None
        self.radius = None
        self.description_lines = [
            "Ahora, escoja el alcance y uno de los siguientes algoritmos metaheurísticos que se",
            "aplicará sobre el polígono determinado previamente para resolver el problema.",
        ]
        self.button_title = "Algoritmos metaheurísticos:"
        self.buttons = [
            Button(
                100,
                170,
                200,
                90,
                "Simulated Annealing",
                action=self.simulated_annealing,
                font_size=20,
                text_color=(0, 0, 0),
                border_radius=20,
            ),
            Button(
                500,
                170,
                200,
                90,
                "Algoritmo Genético",
                action=self.genetic_algorithms,
                font_size=20,
                text_color=(0, 0, 0),
                border_radius=20,
            ),
            Button(
                100,
                300,
                200,
                90,
                "Búsqueda Tabú",
                action=self.tabu_search,
                font_size=20,
                text_color=(0, 0, 0),
                border_radius=20,
            ),
            Button(
                500,
                300,
                200,
                90,
                "Experimentar",
                action=self.toying_with_concept,
                font_size=20,
                text_color=(0, 0, 0),
                border_radius=20,
            ),
        ]
        self.radius_slider = Slider(
            70,
            500,
            600,
            7,
            min_value=10,
            max_value=600,
            start_value=80,
            background_color=(245, 245, 245),
            color=(158, 156, 156),
            font_size=25,
            title="Alcance:",
        )

    def simulated_annealing(self):
        """
        Starts the simulated annealing algorithm
        """
        self.manager.set_scene("random_search")
        self.manager.current_scene.set_algorithm("simulated_annealing")
        self.manager.current_scene.set_radius(self.radius)
        self.manager.current_scene.set_polygon(self.polygon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def genetic_algorithms(self):
        """
        Starts the genetic algorithms algorithm
        """
        self.manager.set_scene("genetic_algorithm")
        self.manager.current_scene.set_radius(self.radius)
        self.manager.current_scene.set_polygon(self.polygon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def tabu_search(self):
        """
        Starts the tabu search algorithm
        """
        self.manager.set_scene("random_search")
        self.manager.current_scene.set_algorithm("tabu_search")
        self.manager.current_scene.set_radius(self.radius)
        self.manager.current_scene.set_polygon(self.polygon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def toying_with_concept(self):
        """
        Starts the toying with concept scene
        """
        self.manager.set_scene("toying_with_concept")
        self.manager.current_scene.set_polygon(self.polygon)
        self.manager.current_scene.set_radius(self.radius)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
        self.radius_slider.handle_event(event)

    def set_polygon(self, polygon):
        """
        Sets the polygon for the algorithm

        Parameters
        ----------
        polygon: Polygon
            Polygon to set
        """
        self.polygon = polygon

    def set_radius(self, radius):
        """
        Sets the radius for the algorithm

        Parameters
        ----------
        radius: float
            Radius to set
        """
        self.radius = radius

    def draw_description(self, screen):
        """
        Draws the description of the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the description on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 20)
        y_start = 20
        line_separation = 30
        for i, line in enumerate(self.description_lines):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (20, y_start + i * line_separation))

    def update(self):
        """
        Updates the scene
        """
        hovering = any(button.is_hovered() for button in self.buttons)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
        )
        self.set_radius(self.radius_slider.get_value())

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the scene
        """
        screen.fill((255, 255, 255))
        self.draw_description(screen)
        pygame.draw.rect(screen, (219, 229, 245), (20, 100, 760, 480), 0, 20)
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 25)
        title = font.render(self.button_title, True, (0, 0, 0))
        title_rect = title.get_rect(centery=140)
        title_rect.x = 50
        screen.blit(title, title_rect)
        self.radius_slider.draw(screen)
        for button in self.buttons:
            button.draw(screen)
