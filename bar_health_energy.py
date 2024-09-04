import pygame
from abc import ABC, abstractmethod

class Bar(pygame.sprite.Sprite,ABC):
    def __init__(self, groups, initial_width, height, color, cooldown_duration, position):
        super().__init__(groups)  

        self.initial_width = initial_width
        self.width = initial_width
        self.height = height
        self.color = color
        self.cooldown_duration = cooldown_duration
        self.rect_center = position
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.rect_center)

        self.can_regenerate = True
        self.last_update_time = pygame.time.get_ticks()

    @abstractmethod
    def increase(self, amount):
        pass

    @abstractmethod
    def reduce(self, amount):
        pass

    def update_image(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.rect_center)


class Health(Bar):
    def __init__(self, groups):
        super().__init__(groups, initial_width=300, height=10, color=(0, 255, 0), cooldown_duration=800, position=(170, 650))

    def increase(self, amount):
        if pygame.time.get_ticks() >= self.last_update_time + self.cooldown_duration:
            self.width += amount
            if self.width > self.initial_width:
                self.width = self.initial_width
            self.last_update_time = pygame.time.get_ticks()
            self.update_image()

    def reduce(self, amount):
        self.width -= amount
        if self.width < 0:
            self.width = 0
        self.update_image()


class Energy(Bar):
    def __init__(self, groups):
        super().__init__(groups, initial_width=200, height=10, color=(0, 128, 255), cooldown_duration=100, position=(170, 665))

    def increase(self, amount):
        if pygame.time.get_ticks() >= self.last_update_time + self.cooldown_duration:
            self.width += amount
            if self.width > self.initial_width:
                self.width = self.initial_width
            self.last_update_time = pygame.time.get_ticks()
            self.update_image()

    def reduce(self, amount):
        self.width -= amount
        if self.width < 0:
            self.width = 0
        self.update_image()
