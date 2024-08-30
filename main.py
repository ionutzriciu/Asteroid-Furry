import pygame
import random
from os.path import join
from settings import *
from player import *
from menus import Menu
from support import Scoreboard, HighScoresManager
from bar_health_energy import * 
from meteors_stars import Meteor, Stars
from laser import Laser

# Initialize the mixer for sound effects
pygame.mixer.init()

class GameState:
    """
    Enumeration for game states.
    """
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    FAQ = "faq"
    LEADERBOARD = "leaderboard"

class Game:
    """
    The main game class that handles initialization, game loop, and state management.
    """
    def __init__(self):
        """
        Initialize the game, setting up the display, clock, state flags, sounds, and sprites.
        """
        # Initialize pygame
        pygame.init()

        # Set up display window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Asteroid Fury')

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Game state flags
        self.running = True
        self.current_state = GameState.MAIN_MENU

        # Sounds
        self.collision_sound = pygame.mixer.Sound(explosion_sound)  # Load collision sound
        pygame.mixer.music.load(main_menu_music)
        pygame.mixer.music.play(-1)  # Loop the music

        # Load background image
        self.image = pygame.image.load(join('data', 'images', 'bg', '1349322.png')).convert_alpha()

        # Initialize menu
        self.menu = Menu(self.display_surface)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.health = Health(self.all_sprites)
        self.energy = Energy(self.all_sprites)
        self.meteors = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.player = Player(self.all_sprites, self.lasers, self.health, self.energy)
        self.score = Scoreboard(self.all_sprites)

        # Time tracking and spawn settings
        self.spawn_time_meteors = pygame.time.get_ticks()
        self.spawn_time_stars = pygame.time.get_ticks()
        self.initial_spawn_interval = random.randint(1000, 2000)
        self.spawn_interval_meteors = self.initial_spawn_interval
        self.spawn_interval_stars = 500
        self.min_spawn_interval = 150
        self.spawn_decrease_rate = 5
        self.meteors_spawned = 0
        self.max_meteors = 30
        self.max_stars = 20

        # High scores
        self.high_scores_manager = HighScoresManager()

    def spawn_stars(self):
        """
        Spawn stars at regular intervals.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time_stars >= self.spawn_interval_stars and len(self.stars) < self.max_stars:
            for _ in range(1):
                star = Stars(self.all_sprites)
                self.all_sprites.add(star)
                self.stars.add(star)
            self.spawn_time_stars = current_time

            if self.meteors_spawned % self.spawn_decrease_rate == 0:
                self.spawn_interval_stars = max(self.min_spawn_interval, self.spawn_interval_stars - 50)

    def spawn_meteors(self):
        """
        Spawn meteors at regular intervals.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time_meteors >= self.spawn_interval_meteors and len(self.meteors) < self.max_meteors:
            meteor = Meteor(self.all_sprites, self.meteors)
            self.all_sprites.add(meteor)
            self.meteors.add(meteor)
            self.spawn_time_meteors = current_time
            self.meteors_spawned += 10

            if self.meteors_spawned % self.spawn_decrease_rate == 0:
                self.spawn_interval_meteors = max(self.min_spawn_interval, self.spawn_interval_meteors - 100)

    def collisions(self):
        """
        Handle collisions between the player, meteors, and lasers.
        """
        player_collisions = pygame.sprite.spritecollide(self.player, self.meteors, False, pygame.sprite.collide_mask)
        for meteor in player_collisions:
            PlayerExplosion(self.player.rect.center, self.all_sprites)
            self.collision_sound.play()
            self.health.reduce(10)

        for laser in self.lasers:
            laser_collision = pygame.sprite.spritecollide(laser, self.meteors, True, pygame.sprite.collide_mask)
            for meteor in laser_collision:
                self.collision_sound.play()
                laser.kill()
                self.score.increase_score()
                AnimatedExplosion(laser.rect.midtop, self.all_sprites)

    def game_over(self):
        """
        Handle the game over state, prompt for the player's name, and save high scores.
        """
        x = WINDOW_WIDTH // 2
        y = WINDOW_HEIGHT // 2
        text = 'New High Score !!! Enter your name: '

        button_width = 400
        button_height = 50
        default_box_color = ('#8e7cc3')
        button_text_color = (255, 255, 255)
        button_font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)

        button_rect = pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)
        pygame.draw.rect(self.display_surface, default_box_color, button_rect)
        text_surface = button_font.render(text, True, button_text_color)
        text_rect = text_surface.get_rect(center=(x, y - 50))
        self.display_surface.blit(text_surface, text_rect)

        pygame.display.flip()
        name = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name:  # Make sure a name has been entered
                            self.high_scores_manager.add_high_score(name, self.score.current_score)
                            self.display_high_scores()
                            self.reset_game()
                            self.current_state = GameState.MAIN_MENU  # Ensure the game stays in the menu after resetting
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            pygame.draw.rect(self.display_surface, default_box_color, button_rect)
            text_surface = button_font.render(text, True, button_text_color)
            self.display_surface.blit(text_surface, text_rect)
            name_surface = button_font.render(name, True, button_text_color)
            name_rect = name_surface.get_rect(center=button_rect.center)
            self.display_surface.blit(name_surface, name_rect)
            pygame.display.flip()

    def reset_game(self):
        """
        Reset the game to its initial state.
        """
        self.health.width = self.health.initial_width
        self.energy.energy_width = self.energy.initial_width
        self.score.current_score = 0
        self.spawn_time_meteors = pygame.time.get_ticks()
        self.spawn_time_stars = pygame.time.get_ticks()
        self.spawn_interval_meteors = self.initial_spawn_interval
        self.spawn_interval_stars = 500
        self.meteors_spawned = 0
        self.all_sprites.empty()
        self.stars.empty()
        self.meteors.empty()
        self.lasers.empty()
        self.health = Health(self.all_sprites)
        self.energy = Energy(self.all_sprites)
        self.player = Player(self.all_sprites, self.lasers, self.health, self.energy)  # Ensure all parameters are passed
        self.score = Scoreboard(self.all_sprites)


    def display_high_scores(self):
        """
        Display the high scores on the screen.
        """
        high_scores = self.high_scores_manager.get_high_scores()
        self.display_surface.fill(('#adadff'))  # Clear screen
        font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)

        y_offset = 100
        for i, score_entry in enumerate(high_scores):
            text = f"{i + 1}. {score_entry['name']}: {score_entry['score']}"
            text_surface = font.render(text, True, (255, 255, 240))
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, y_offset + i * 50))
            self.display_surface.blit(text_surface, text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False  # Exit the loop to return to the main menu

    def game_run(self):
        """
        Main game loop that handles different game states.
        """
        while self.running:
            if self.current_state == GameState.MAIN_MENU:
                self.menu.display_menu()
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                selected_option = self.menu.handle_input()
                if selected_option == 'Play':
                    self.current_state = GameState.PLAYING
                elif selected_option == 'FAQ':
                    self.current_state = GameState.FAQ
                elif selected_option == 'Quit':
                    self.running = False
                elif selected_option == 'Leaderboard':
                    self.current_state = GameState.LEADERBOARD

            elif self.current_state == GameState.PLAYING:  # Gameplay loop
                dt = self.clock.tick(60) / 1000  # Delta time for smooth movement
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current_state = GameState.MAIN_MENU  # Go back to main menu

                self.display_surface.fill((0, 0, 0))
                self.display_surface.blit(self.image, (0, 0))
                self.all_sprites.draw(self.display_surface)
                self.all_sprites.update(dt)
                self.health.increase(5)
                self.spawn_stars()
                self.collisions()
                self.spawn_meteors()
                pygame.display.flip()

                if self.health.width <= 0:
                    self.current_state = GameState.GAME_OVER
                    self.game_over()

            elif self.current_state == GameState.FAQ:
                self.menu.display_faq()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            self.current_state = GameState.MAIN_MENU

            elif self.current_state == GameState.LEADERBOARD:
                self.display_high_scores()
                self.current_state = GameState.MAIN_MENU  # Go back to the main menu after displaying

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.game_run()
