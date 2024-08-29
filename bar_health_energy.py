import pygame

class Bar(pygame.sprite.Sprite):
    """
    Base class for any bar (Health, Energy) with common functionality.
    
    Attributes:
        initial_width: The initial width of the bar.
        width: The current width of the bar.
        height: The height of the bar.
        color: The color of the bar.
        cooldown_duration: The cooldown duration for regeneration.
    """
    def __init__(self, groups, initial_width, height, color, cooldown_duration, position):
        super().__init__(groups)

        self.initial_width = initial_width
        self.width = initial_width
        self.height = height
        self.color = color
        self.cooldown_duration = cooldown_duration
        self.rect_center = position
        
        # Initialize the bar
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.rect_center)

        # Timer mechanics
        self.can_regenerate = True
        self.last_update_time = pygame.time.get_ticks()

    def increase(self, amount):
        """
        Increases the bar's width by a specified amount, up to its initial width.
        """
        current_time = pygame.time.get_ticks()
        if self.can_regenerate and current_time >= self.last_update_time + self.cooldown_duration:
            if self.width < self.initial_width:
                self.width += amount
                if self.width > self.initial_width:
                    self.width = self.initial_width
                self.last_update_time = current_time
                self.update_image()

    def reduce(self, amount):
        """
        Reduces the bar's width by a specified amount, down to zero.
        """
        self.width -= amount
        if self.width < 0:
            self.width = 0
        self.update_image()

    def update_image(self):
        """Updates the bar's image and rect."""
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.rect_center)


class Health(Bar):
    """
    Represents the health bar for the player.
    """
    def __init__(self, groups):
        super().__init__(groups, initial_width=300, height=10, color=(0, 255, 0), cooldown_duration=800, position=(170, 650))

    def increase_health(self):
        """Increases the player's health."""
        self.increase(amount=5)

    def reduce_health(self):
        """Reduces the player's health."""
        self.reduce(amount=10)


class Energy(Bar):
    """
    Represents the energy bar for the player.
    """
    def __init__(self, groups):
        super().__init__(groups, initial_width=200, height=10, color=(0, 128, 255), cooldown_duration=100, position=(170, 665))

    def increase_energy(self):
        """Increases the player's energy."""
        self.increase(amount=5)

    def reduce_energy(self):
        """Reduces the player's energy."""
        self.reduce(amount=5)