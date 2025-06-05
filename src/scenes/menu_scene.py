import pygame
from src.scenes import Scene
from src.ui import Button


class MenuScene(Scene):
    """
    Class for the menu scene
    """

    def __init__(self, manager):
        """
        Constructor for the MenuScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.description_lines = [
            "Elija una de las siguientes opciones para determinar el polígono simple",
            "sobre el cual trabajarán las técnicas metaheurísticas:",
        ]
        self.buttons_description = [
            "Permite dibujar un polígono simple en la pantalla.",
            "Permite cargar un polígono simple desde un archivo.",
            "Permite generar un polígono simple de manera aleatoria.",
        ]
        self.buttons = [
            Button(
                50,
                130,
                200,
                90,
                "Dibujar polígono",
                text_color=(0, 0, 0),
                font_size=20,
                action=self.draw_polygon,
                font_path="./fonts/nunito/Nunito-Regular.ttf",
                border_radius=20,
            ),
            Button(
                50,
                280,
                200,
                90,
                "Cargar polígono",
                text_color=(0, 0, 0),
                font_size=20,
                action=self.load_polygon,
                font_path="./fonts/nunito/Nunito-Regular.ttf",
                border_radius=20,
            ),
            Button(
                50,
                430,
                200,
                90,
                "Crear polígono",
                text_color=(0, 0, 0),
                font_size=20,
                action=self.create_polygon,
                font_path="./fonts/nunito/Nunito-Regular.ttf",
                border_radius=20,
            ),
        ]

    def load_polygon(self):
        """
        Loads a polygon from a file
        """
        self.manager.set_scene("load_polygon")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_polygon(self):
        """
        Draws a polygon
        """
        self.manager.set_scene("draw_polygon")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def create_polygon(self):
        """
        Creates a polygon
        """
        self.manager.set_scene("create_polygon")
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

    def update(self):
        """
        Updates the scene
        """
        hovering = any(button.is_hovered() for button in self.buttons)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
        )

    def draw_description(self, screen):
        """
        Draws the description of the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the description
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 20)
        y_start = 30
        line_separation = 30
        for i, line in enumerate(self.description_lines):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (40, y_start + i * line_separation))

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the scene
        """
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (219, 229, 245), (20, 100, 760, 480), 0, 20)
        self.draw_description(screen)
        for button in self.buttons:
            button.draw(screen)
        for i, button in enumerate(self.buttons):
            x, y, width, height = button.rect
            font = pygame.font.Font("./fonts/nunito/Nunito-Light.ttf", 18)
            text = font.render(self.buttons_description[i], True, (0, 0, 0))
            screen.blit(text, (x + width + 20, y + 33))
