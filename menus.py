import pygame
from settings import *


class Menu:
    """
    Represents the game's main menu.

    Attributes:
        screen: The game screen where the menu is displayed.
        options: List of menu options.
        selected_option: The currently selected menu option.
        font: Font used for rendering menu options.
        title_font: Font used for rendering the menu title.
        title: The title of the game displayed in the menu.
    """

    def __init__(self, screen):
        """
        Initializes the Menu with the screen and default settings.

        Args:
            screen: The game screen where the menu will be displayed.
        """
        self.screen = screen
        self.options = ['Play', 'FAQ', 'Quit', 'Leaderboard']
        self.selected_option = 0
        self.font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)
        self.title_font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 100)  # Title font size
        self.title = 'ASTEROID FURY !!!'

    def display_menu(self):
        """
        Renders and displays the main menu on the screen.
        """
        self.screen.fill(('#adadff'))  # Clear screen with a light blue color

        # Render and display the title
        title_text = self.title_font.render(self.title, True, '#1d4971')  # Title color
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, 200))  # Centered horizontally at y = 200
        self.screen.blit(title_text, title_rect)

        # Render and display each menu option
        for idx, option in enumerate(self.options):
            color = ('#ace7f6') if idx == self.selected_option else ('#1d4971')  # Highlight selected option
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + idx * 100))
            self.screen.blit(text, rect)

    def display_faq(self):
        """
        Renders and displays the FAQ screen with game instructions and credits.
        """
        # FAQ content
        faq_text = [
            "Welcome to Asteroid Fury!",
            "Use arrow keys to move and spacebar to shoot.",
            "Keep spacebar pressed to perform a laser swipe",
            "Energy depletes when laser swipe is performed.",
            "Avoid meteors to keep your health intact.",
            "Energy and health autoregenerate.",
            "The ship moves faster sideways :)",
            "See if you can get to the top of the leaderboard",
            "Special thanks to MillionthVector, pngall, JadisGames, NenadSimic, Jan125,",
            "K.L.Jonasson for audio and graphics",
            "Code by Riciu Ionut",
            "Good luck and have fun!"
        ]

        # FAQ display parameters
        faq_font = pygame.font.Font(None, 36)  # Font for FAQ text
        y_offset = 50  # Initial y position for the text
        line_spacing = 30  # Space between lines
        self.screen.fill(('#adadff'))  # Clear the screen with a light blue color

        # Render and display each line of the FAQ
        for i, line in enumerate(faq_text):
            text_surface = faq_font.render(line, True, (255, 255, 255))  # White text
            self.screen.blit(text_surface, (100, y_offset + i * (text_surface.get_height() + line_spacing)))

        pygame.display.flip()  # Update the display

    def handle_input(self):
        """
        Handles user input to navigate the menu.

        Returns:
            The selected option as a string if Enter is pressed, otherwise None.
        """
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif keys[pygame.K_RETURN]:
            return self.options[self.selected_option]
        return None
