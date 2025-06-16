import pygame
import numpy as np

from src.scenes import Scene
from src.utils import point_inside_polygon, get_circular_sector_as_polygon, polygon_area
from src.algorithms.fitness_algorithm import calculate_fitness_area


class ToyingWithConceptScene(Scene):
    """
    Class for the Toying With Concept scene
    """

    def __init__(self, manager):
        """
        Constructor for the ToyingWithConceptScene class
        """
        super().__init__(manager)
        self.description_lines = [
            "Una vez cargado el polígono y determinado el alcance, puedes mover",
            "el ratón por la pantalla para ver cuál es la región de visibilidad",
            "del punto que se encuentra debajo del ratón. Haz click para fijar el punto.",
        ]
        self.polygon = None
        self.radius = None
        self.current_point = None
        self.stationary_point = None
        self.sections = None
        self.valid = True
        self.polygon_area = 0.0
        self.area_text = "Área: "
        self.area = 0.0

    def set_polygon(self, polygon):
        """
        Set the polygon for the scene.

        Parameters
        ----------
        polygon: np.ndarray
            Polygon to set
        """
        self.polygon = polygon
        self.polygon_area = polygon_area(polygon)

    def set_radius(self, radius):
        """
        Set the radius for the scene.

        Parameters
        ----------
        radius: float
            Radius to set
        """
        self.radius = radius

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events of the scene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        if event.type == pygame.MOUSEMOTION:
            self.current_point = np.array(event.pos, dtype=float)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.stationary_point = np.array(event.pos, dtype=float)
            self.area, self.sections = calculate_fitness_area(
                self.polygon, self.stationary_point, self.radius, return_polygon=True
            )

    def update(self):
        """
        Updates the scene
        """
        if self.current_point is not None:
            self.valid = point_inside_polygon(
                self.polygon, self.current_point, closed=True
            )

    def draw_description(self, screen: pygame.Surface):
        """
        Draws the description of the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the description on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Regular.ttf", 17)
        y_start = 20
        line_separation = 30
        for i, line in enumerate(self.description_lines):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (20, y_start + i * line_separation))

    def draw_sections(self, screen: pygame.Surface):
        """
        Draw the sections of the visibility area

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the sections on
        """
        if self.sections is not None:
            if len(self.sections) == 0:
                if self.stationary_point is None:
                    # Draw a circle if no sections are available
                    pygame.draw.circle(
                        screen,
                        (243, 250, 246),
                        self.current_point,
                        self.radius,
                        0,
                    )
                else:
                    pygame.draw.circle(
                        screen,
                        (243, 250, 246),
                        self.stationary_point,
                        self.radius,
                        0,
                    )
            else:
                for section in self.sections:
                    if len(section) > 2:
                        # Plot the polygon and fill it
                        pygame.draw.polygon(screen, (243, 250, 246), section, 0)
                    else:
                        if self.stationary_point is None:
                            polygon = get_circular_sector_as_polygon(
                                self.current_point, section[0], section[1]
                            )
                        else:
                            polygon = get_circular_sector_as_polygon(
                                self.stationary_point, section[0], section[1]
                            )
                        pygame.draw.polygon(screen, (243, 250, 246), polygon, 0)

    def draw_area_text(self, screen: pygame.Surface):
        """
        Draws the status text on the screen

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the status text on
        """
        font = pygame.font.Font("./fonts/nunito/Nunito-Light.ttf", 15)
        area_text = self.area_text + f"{self.area:.2f}"
        text = font.render(area_text, True, (0, 0, 0))
        screen.blit(text, (550, 15))

        # Plot percentage of the polygon area
        if self.polygon is not None:
            percentage = (self.area / self.polygon_area) * 100
            percentage_text = f"Área cubierta: {percentage:.2f}%"
            text = font.render(percentage_text, True, (0, 0, 0))
            screen.blit(text, (550, 35))

    def draw(self, screen: pygame.Surface):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the scene
        """
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (230, 230, 232), (5, 120, 790, 495), 0)
        pygame.draw.rect(screen, (0, 0, 0), (5, 120, 790, 495), 1)
        self.draw_description(screen)
        if (
            self.current_point is not None
            and self.stationary_point is None
            and self.valid
        ):
            self.area, self.sections = calculate_fitness_area(
                self.polygon, self.current_point, self.radius, return_polygon=True
            )
            self.draw_sections(screen)
            pygame.draw.circle(
                screen,
                (255, 161, 161),
                self.current_point,
                3,
            )
        elif self.stationary_point is None and not self.valid:
            self.area = 0.0
            self.sections = None
        elif self.stationary_point is not None:
            self.draw_sections(screen)
            pygame.draw.circle(
                screen,
                (255, 161, 161),
                self.stationary_point,
                3,
            )
        self.draw_area_text(screen)
        if self.polygon is not None:
            pygame.draw.polygon(screen, (0, 0, 0), self.polygon, 1)
