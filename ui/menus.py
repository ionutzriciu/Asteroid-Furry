import pygame
from os.path import join
from engine_support import WINDOW_WIDTH, WINDOW_HEIGHT

class GameState:
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    FAQ = "faq"
    LEADERBOARD = "leaderboard"
    

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ['Play', 'FAQ', 'Quit', 'Leaderboard']
        self.selected_option = 0
        self.font = pygame.font.Font(join('assets', 'images', 'Oxanium-Bold.ttf'), 40)
        self.title_font = pygame.font.Font(join('assets', 'images', 'Oxanium-Bold.ttf'), 100)  
        self.title = 'ASTEROID FURY !!!'

    def display_menu(self):
        self.screen.fill(('#adadff')) 

        title_text = self.title_font.render(self.title, True, '#1d4971')  
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, 200))  
        self.screen.blit(title_text, title_rect)

        for idx, option in enumerate(self.options):
            color = ('#ace7f6') if idx == self.selected_option else ('#1d4971')  
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + idx * 100))
            self.screen.blit(text, rect)

    def display_faq(self):
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

        faq_font = pygame.font.Font(None, 36) 
        y_offset = 50  
        line_spacing = 30  
        self.screen.fill(('#adadff'))  

        for i, line in enumerate(faq_text):
            text_surface = faq_font.render(line, True, (255, 255, 255))  
            self.screen.blit(text_surface, (100, y_offset + i * (text_surface.get_height() + line_spacing)))

        pygame.display.flip()  

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
        return None
    
    

