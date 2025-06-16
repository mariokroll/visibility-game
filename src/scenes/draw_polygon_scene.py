import pygame
import numpy as np

from src.scenes import Scene
from src.ui import Button
from src.utils import intersect_polygon


class DrawPolygonScene(Scene):
    """
    Class for the draw polygon scene
    """

    def __init__(self, manager):
        """
        Constructor for the DrawPolygonScene class

        Parameters
        ----------
        manager: SceneManager
            Scene manager
        """
        super().__init__(manager)
        self.polygon = []
        self.current_point = None
        self.description = [
            "Haga click en la pantalla para agregar un punto al polígono. Cuando termine, presione",
            "el botón 'Listo'. Para deshacer el último punto, presione el botón 'Deshacer'.",
        ]
        self.done = Button(
            620,
            125,
            150,
            70,
            "Listo",
            text_color=(0, 0, 0),
            action=self.done_action,
            font_size=20,
        )
        self.undo = Button(
            620,
            215,
            150,
            70,
            "Deshacer",
            text_color=(0, 0, 0),
            action=self.undo_action,
            font_size=20,
        )
        self.intersecting = False
        self.in_limits = True

    def get_polygon(self):
        """
        Returns the polygon drawn

        Returns
        -------
        list
            List of points of the polygon
        """
        return self.polygon

    def done_action(self):
        """
        Finishes the polygon
        """
        if len(self.polygon) < 3:
            return
        # If the polygon is not closed, close it
        if not np.allclose(self.polygon[0], self.polygon[-1]):
            self.polygon.append(self.polygon[0])
        self.manager.set_scene("choose_algorithm")
        self.manager.current_scene.set_polygon(self.polygon)

    def undo_action(self):
        """
        Undoes the last point
        """
        if len(self.polygon) > 0:
            self.polygon = self.polygon[:-1]

    def handle_event(self, event):
        """
        Handles events of the scene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        self.done.handle_event(event)
        self.undo.handle_event(event)
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and not self.done.is_clicked(event)
            and not self.undo.is_clicked(event)
            and not self.intersecting
        ):
            self.polygon.append(event.pos)
        if event.type == pygame.MOUSEMOTION:
            self.current_point = event.pos

    def check_limits(self):
        """
        Checks if the current point is in the limits of the drawing screen
        """
        if self.current_point:
            x, y = self.current_point
            if x < 5 or x > 795 or y < 120 or y > 595:
                self.in_limits = False
            else:
                self.in_limits = True

    def update(self):
        """
        Updates the scene
        """
        # Check if done or undo are possible
        if (len(self.polygon) < 3 and self.done.is_hovered()) or (
            len(self.polygon) == 0 and self.undo.is_hovered()
        ):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
        elif self.done.is_hovered() or self.undo.is_hovered():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Check if the current point is in the limits of the drawing screen
        if self.current_point:
            self.intersecting = self.check_intersection()
            self.check_limits()

    def check_intersection(self):
        """
        Checks if the current edge intersects an existing edge

        Returns
        -------
        bool
            True if there is an intersection, False otherwise
        """
        if len(self.polygon) < 3 or not self.current_point:
            return False
        new_edge = (self.polygon[-1], self.current_point)
        if intersect_polygon(
            new_edge, self.polygon[:-1], closed=True, line_is_infinite=False
        ):
            return True
        return False

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
        for i, line in enumerate(self.description):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (20, y_start + i * line_separation))

    def buttons_hovered(self) -> bool:
        """
        Checks if any button is hovered

        Returns
        -------
        bool
            True if any button is hovered, False otherwise
        """
        return self.done.is_hovered() or self.undo.is_hovered()

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the scene on
        """
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (230, 230, 232), (5, 120, 790, 495), 0)
        pygame.draw.rect(screen, (0, 0, 0), (5, 120, 790, 495), 1)
        self.draw_description(screen)
        if self.current_point and self.in_limits and not self.buttons_hovered():
            color = (255, 232, 232) if self.intersecting else (255, 161, 161)
            pygame.draw.circle(screen, color, self.current_point, 5)
        for i, point in enumerate(self.polygon):
            pygame.draw.circle(screen, (255, 161, 161), point, 4)
            if i < len(self.polygon) - 1:
                pygame.draw.line(screen, (0, 0, 0), point, self.polygon[i + 1])
        self.done.draw(screen)
        self.undo.draw(screen)
