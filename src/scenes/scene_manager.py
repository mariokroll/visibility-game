import pygame


class SceneManager:
    """
    Manager for the scenes of the game
    """

    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name: str, scene):
        """
        Adds scene to the manager

        Parameters
        ----------
        name: str
            Name of the scene
        scene: Scene
            Scene object
        """
        self.scenes[name] = scene

    def set_scene(self, name):
        """
        Sets the current scene

        Parameters
        ----------
        name: str
            Name of the scene
        """
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def handle_event(self, event):
        """
        Handles events of the scene

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle"""
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self):
        """
        Updates the scene
        """
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        """
        Draws the scene

        Parameters
        ----------
        screen: pygame.Surface
            Screen to draw the scene
        """
        if self.current_scene:
            self.current_scene.draw(screen)
