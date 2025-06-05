import pygame


class Button:
    """
    Class to represent a button

    Attributes
    ----------
    x: int
        X coordinate of the button
    y: int
        Y coordinate of the button
    width: int
        Width of the button
    height: int
        Height of the button
    color: tuple
        Color of the button (r, g, b)
    text: str
        Text of the button
    text_color: tuple
        Color of the text (r, g, b)
    font_size: int
        Size of the font
    font: pygame.font.Font
        Font of the text
    action: function
        Function to call when the button is clicked
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color=(252, 224, 192),
        text_color=(255, 255, 255),
        hover_color=(255, 246, 232),
        font_size=30,
        action=None,
        font_path="./fonts/nunito/Nunito-Regular.ttf",
        border_radius=5,
    ):
        """
        Constructor for the Button class

        Parameters
        ----------
        x: int
            X coordinate of the button
        y: int
            Y coordinate of the button
        width: int
            Width of the button
        height: int
            Height of the button
        color: tuple
            Color of the button (r, g, b)
        text: str
            Text of the button
        text_color: tuple
            Color of the text (r, g, b)
        font_size: int
            Size of the font
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.button_color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(font_path, self.font_size)
        self.action = action
        self.border_radius = border_radius

    def draw(self, screen: pygame.Surface):
        """
        Method to draw the button on the screen

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the button on
        """
        pygame.draw.rect(
            screen, self.color, self.rect, border_radius=self.border_radius
        )
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_hovered(self) -> bool:
        """
        Method to check if the button is hovered

        Returns
        -------
        bool
            True if the button is hovered, False otherwise
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
            return True
        else:
            self.color = self.button_color
            return False

    def is_clicked(self, event) -> bool:
        """
        Method to check if the button is clicked

        Parameters
        ----------
        event: pygame.event.Event
            Event to check

        Returns
        -------
        bool
            True if the button is clicked, False otherwise
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered()

    def handle_event(self, event, *args):
        """
        Method to handle events of the button

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        if self.is_clicked(event) and self.action:
            self.action(*args)


class Slider:
    """
    Class to represent a slider

    Attributes
    ----------
    x: int
        X coordinate of the slider
    y: int
        Y coordinate of the slider
    width: int
        Width of the slider
    height: int
        Height of the slider
    min_value: int
        Minimum value of the slider
    max_value: int
        Maximum value of the slider
    start_value: int
        Initial value of the slider
    color: tuple
        Color of the slider (r, g, b)
    text_color: tuple
        Color of the text (r, g, b)
    font_size: int
        Size of the font
    background_color: tuple
        Color of the background (r, g, b)
    knob_color: tuple
        Color of the knob (r, g, b)
    title: Optional[str]
        Title of the slider
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        min_value,
        max_value,
        start_value,
        color=(0, 0, 0),
        text_color=(0, 0, 0),
        font_size=30,
        background_color=(0, 0, 255),
        knob_color=(251, 185, 109),
        title="",
        font_path="./fonts/nunito/Nunito-Regular.ttf",
    ):
        """
        Constructor for the Slider class

        Parameters
        ----------
        x: int
            X coordinate of the slider
        y: int
            Y coordinate of the slider
        width: int
            Width of the slider
        height: int
            Height of the slider
        min_value: int
            Minimum value of the slider
        max_value: int
            Maximum value of the slider
        start_value: int
            Initial value of the slider
        color: tuple
            Color of the slider (r, g, b)
        text_color: tuple
            Color of the text (r, g, b)
        font_size: int
            Size of the font
        background_color: tuple
            Color of the background (r, g, b)
        knob_color: tuple
            Color of the knob (r, g, b)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.background_color = background_color
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(font_path, self.font_size)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        text_width, text_height = self.font.size(str(self.max_value))
        self.background = pygame.Rect(
            self.x - 10,
            self.y - text_height // 2,
            self.width + text_width + 40,
            self.height + text_height,
        )
        self.knob_radius = 10
        self.knob_x = (
            self.x
            + (self.value - self.min_value)
            / (self.max_value - self.min_value)
            * self.width
        )
        self.knob_color = knob_color
        self.dragging = False  # True if the knob is being dragged
        self.title = title

    def handle_event(self, event):
        """
        Method to handle events of the slider

        Parameters
        ----------
        event: pygame.event.Event
            Event to handle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            pos = pygame.mouse.get_pos()
            self.knob_x = min(max(pos[0], self.x), self.x + self.width)
            self.value = int(
                (self.knob_x - self.x) / self.width * (self.max_value - self.min_value)
                + self.min_value
            )

    def draw(self, screen: pygame.Surface):
        """
        Method to draw the slider on the screen

        Parameters
        ----------
        screen: pygame.Surface
            Surface to draw the slider on
        """
        pygame.draw.rect(screen, self.background_color, self.background, 2)
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.circle(
            screen,
            self.knob_color,
            (self.knob_x, self.y + self.height // 2),
            self.knob_radius,
        )
        text = self.font.render(str(self.value), True, self.text_color)
        text_rect = text.get_rect(centery=self.rect.centery)
        text_rect.x = self.x + self.width + 10

        if self.title:
            title = self.font.render(self.title, True, self.text_color)
            title_height = title.get_height()
            title_rect = title.get_rect(
                bottomleft=(self.x - 10, self.y - title_height // 2)
            )
            screen.blit(title, title_rect)
        screen.blit(text, text_rect)

    def get_value(self):
        """
        Method to get the value of the slider

        Returns
        -------
        int
            Value of the slider
        """
        return self.value
