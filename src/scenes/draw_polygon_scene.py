import pygame
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
        self.done = Button(
            690,
            10,
            100,
            50,
            "Listo",
            (0, 0, 255),
            (255, 255, 255),
            action=self.done_action,
        )
        self.undo = Button(
            690,
            70,
            100,
            50,
            "Deshacer",
            (0, 0, 255),
            (255, 255, 255),
            action=self.undo_action,
        )
        self.intersecting = False

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
        self.manager.set_scene("solver")
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
        if event.type == pygame.MOUSEMOTION:
            self.current_point = event.pos
            self.intersecting = self.check_intersection()
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and not self.done.is_clicked(event.pos)
            and not self.undo.is_clicked(event.pos)
            and not self.intersecting
        ):
            self.polygon.append(event.pos)

    def update(self):
        """
        Updates the scene
        """

    def check_intersection(self):
        """
        Checks if the current edge intersects an existing edge

        Returns
        -------
        bool
            True if there is an intersection, False otherwise
        """
        if len(self.polygon) < 2 or not self.current_point:
            return False
        new_edge = (self.polygon[-1], self.current_point)
        for i in range(len(self.polygon) - 2):
            existing_edge = (self.polygon[i], self.polygon[i + 1])
            if intersect_polygon(new_edge, existing_edge):
                return True
        return False

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the scene on
        """
        screen.fill((255, 255, 255))
        if self.current_point:
            pygame.draw.circle(screen, (0, 0, 0), self.current_point, 3)
        for i, point in enumerate(self.polygon):
            pygame.draw.circle(screen, (0, 0, 255), point, 5)
            if i < len(self.polygon) - 1:
                pygame.draw.line(screen, (0, 0, 0), point, self.polygon[i + 1])
        if len(self.polygon) > 0:
            color = (
                (150, 150, 150) if self.intersecting else (0, 0, 0)
            )  # Gris si intersecta
            pygame.draw.line(screen, color, self.polygon[-1], self.current_point)
        self.done.draw(screen)
        self.undo.draw(screen)
