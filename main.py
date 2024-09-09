import pygame
import random
from os.path import join


from settings import *
from support import *

from player import Player  

from meteors_stars import Meteor, Stars
from explosions import PlayerExplosion, AnimatedExplosion

from ui import *
from high_score_resources import HighScoresManager, Scoreboard

pygame.mixer.init()

SPAWN_INTERVAL_STARS = 500
MIN_SPAWN_INTERVAL = 150
SPAWN_DECREASE_RATE = 5
MAX_METEORS = 30
MAX_STARS = 20
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50
DEFAULT_BOX_COLOR = '#8e7cc3'
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT_PATH = join('data', 'images', 'Oxanium-Bold.ttf')
BG_COLOR = (0, 0, 0)
FAQ_BG_COLOR = '#adadff'
FONT_SIZE = 40

class GameState:
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    FAQ = "faq"
    LEADERBOARD = "leaderboard"

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Asteroid Fury')
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MAIN_MENU

        self.collision_sound = pygame.mixer.Sound(explosion_sound)  
        pygame.mixer.music.load(main_menu_music)
        pygame.mixer.music.play(-1)  

        self.background_image = pygame.image.load(join('data', 'images', 'bg', '1349322.png')).convert_alpha()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        self.menu = Menu(self.display_surface)

        self.all_sprites = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.health = Health(self.all_sprites)
        self.energy = Energy(self.all_sprites)
        self.player = Player(self.all_sprites, self.lasers, self.health, self.energy)  
        self.score = Scoreboard(self.all_sprites)

        self.spawn_time_meteors = pygame.time.get_ticks()
        self.spawn_time_stars = pygame.time.get_ticks()
        self.initial_spawn_interval = random.randint(1000, 2000)
        self.spawn_interval_meteors = self.initial_spawn_interval
        self.spawn_interval_stars = SPAWN_INTERVAL_STARS
        self.meteors_spawned = 0

        self.high_scores_manager = HighScoresManager()

    def spawn_stars(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time_stars >= self.spawn_interval_stars and len(self.stars) < MAX_STARS:
            star = Stars(self.all_sprites)
            self.all_sprites.add(star)
            self.stars.add(star)
            self.spawn_time_stars = current_time

            if self.meteors_spawned % SPAWN_DECREASE_RATE == 0:
                self.spawn_interval_stars = max(MIN_SPAWN_INTERVAL, self.spawn_interval_stars - 50)

    def spawn_meteors(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time_meteors >= self.spawn_interval_meteors and len(self.meteors) < MAX_METEORS:
            meteor = Meteor(self.all_sprites, self.meteors)
            self.all_sprites.add(meteor)
            self.meteors.add(meteor)
            self.spawn_time_meteors = current_time
            self.meteors_spawned += 10

            if self.meteors_spawned % SPAWN_DECREASE_RATE == 0:
                self.spawn_interval_meteors = max(MIN_SPAWN_INTERVAL, self.spawn_interval_meteors - 100)

    def handle_collisions(self):
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

    def draw_text(self, text, position, color=BUTTON_TEXT_COLOR):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.display_surface.blit(text_surface, text_rect)

    def game_over(self):
        x = WINDOW_WIDTH // 2
        y = WINDOW_HEIGHT // 2
        input_box = pygame.Rect(x - BUTTON_WIDTH // 2, y - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

        name = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:  
                        self.high_scores_manager.add_high_score(name, self.score.current_score)
                        self.display_high_scores()
                        self.reset_game()
                        self.current_state = GameState.MAIN_MENU  
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            pygame.draw.rect(self.display_surface, DEFAULT_BOX_COLOR, input_box)
            self.draw_text('New High Score !!! Enter your name: ', (x, y - 50))
            self.draw_text(name, input_box.center)
            pygame.display.flip()

    def reset_game(self):
        self.health.width = self.health.initial_width
        self.energy.energy_width = self.energy.initial_width
        self.score.current_score = 0
        self.spawn_time_meteors = pygame.time.get_ticks()
        self.spawn_time_stars = pygame.time.get_ticks()
        self.spawn_interval_meteors = self.initial_spawn_interval
        self.spawn_interval_stars = SPAWN_INTERVAL_STARS
        self.meteors_spawned = 0
        self.all_sprites.empty()
        self.stars.empty()
        self.meteors.empty()
        self.lasers.empty()
        self.health = Health(self.all_sprites)
        self.energy = Energy(self.all_sprites)
        self.player = Player(self.all_sprites, self.lasers, self.health, self.energy)  
        self.score = Scoreboard(self.all_sprites)

    def display_high_scores(self):
        high_scores = self.high_scores_manager.get_high_scores()
        self.display_surface.fill(FAQ_BG_COLOR)
        y_offset = 100

        for i, score_entry in enumerate(high_scores):
            self.draw_text(f"{i + 1}. {score_entry['name']}: {score_entry['score']}", (WINDOW_WIDTH // 2, y_offset + i * 50))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.current_state == GameState.PLAYING and event.key == pygame.K_ESCAPE:
                    self.current_state = GameState.MAIN_MENU
                elif self.current_state == GameState.FAQ and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                    self.current_state = GameState.MAIN_MENU

    def game_run(self):
        while self.running:
            self.handle_events()

            if self.current_state == GameState.MAIN_MENU:
                self.menu.display_menu()
                pygame.display.flip()

                selected_option = self.menu.handle_input()
                if selected_option == 'Play':
                    self.current_state = GameState.PLAYING
                elif selected_option == 'FAQ':
                    self.current_state = GameState.FAQ
                elif selected_option == 'Quit':
                    self.running = False
                elif selected_option == 'Leaderboard':
                    self.current_state = GameState.LEADERBOARD

            elif self.current_state == GameState.PLAYING:
                dt = self.clock.tick(60) / 1000  
                self.display_surface.fill(BG_COLOR)
                self.display_surface.blit(self.background_image, (0, 0))
                self.all_sprites.draw(self.display_surface)
                self.all_sprites.update(dt)
                self.health.increase(5)
                self.spawn_stars()
                self.spawn_meteors()
                self.handle_collisions()
                pygame.display.flip()

                if self.health.width <= 0:
                    self.current_state = GameState.GAME_OVER
                    self.game_over()

            elif self.current_state == GameState.FAQ:
                self.menu.display_faq()
                pygame.display.flip()

            elif self.current_state == GameState.LEADERBOARD:
                self.display_high_scores()
                self.current_state = GameState.MAIN_MENU  

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.game_run()
