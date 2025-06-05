import pygame
from src.ui import Button
from src.scenes import Scene


class StartScene(Scene):
    """
    Class for the start scene
    """

    def __init__(self, manager):
        """
        Constructor for the StartScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.manager = manager
        self.title_lines = [
            "Maximización con técnicas metaheurísticas",
            "de la región de visibilidad con alcance limitado",
            "de un punto en un polígono simple",
        ]
        self.description_lines = [
            "Esta aplicación permite visualizar la resolución del problema de maximización de la",
            "región de visibilidad con alcance limitado de un punto en un polígono simple.",
            "Para ello, se utilizan tres técnicas metaheurísticas que son: Simulated Annealing,",
            f"Algoritmo Genético y Búsqueda Tabú. Para comenzar, pulse en el botón de 'Iniciar'",
        ]
        self.start_button = Button(
            300,
            400,
            200,
            100,
            "Iniciar",
            text_color=(0, 0, 0),
            font_size=30,
            action=self.start_action,
            font_path="./fonts/nunito/Nunito-Regular.ttf",
            border_radius=20,
        )

    def start_action(self):
        """
        Action to be performed when the start button is clicked
        """
        self.manager.set_scene("menu")

    def draw(self, screen):
        """
        Draw the start scene

        Parameters
        ----------
        screen: pygame.Surface
            The screen to draw on
        """
        screen.fill((255, 255, 255))
        self.draw_title(screen)
        pygame.draw.rect(screen, (219, 229, 245), (20, 180, 760, 400), 0, 20)
        self.draw_description(screen)
        self.start_button.draw(screen)

    def update(self):
        """
        Updates the scene
        """
        hovering = self.start_button.is_hovered()
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
        )

    def handle_event(self, event):
        """
        Handles events of the scene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        self.start_button.handle_event(event)

    def draw_title(self, screen):
        """
        Draw the title of the start scene

        Parameters
        ----------
        screen: pygame.Surface
            The screen to draw on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Bold.ttf", 30)
        y_start = 50
        line_spacing = 40
        for i, line in enumerate(self.title_lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(400, y_start + i * line_spacing))
            screen.blit(text, text_rect)

    def draw_description(self, screen):
        """
        Draw the description of the start scene

        Parameters
        ----------
        screen: pygame.Surface
            The screen to draw on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 18)
        y_start = 200
        line_spacing = 30
        for i, line in enumerate(self.description_lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.topleft = (60, y_start + i * line_spacing)
            screen.blit(text, text_rect)
