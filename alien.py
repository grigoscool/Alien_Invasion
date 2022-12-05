import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Кдасс создания пришельцa"""

    def __init__(self, ai_game):
        """Инициализирует пришельцев """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # загрузка изображения пришельца
        self.image = pygame.image.load('images/alien_new.png')
        self.rect = self.image.get_rect()

        # Каждый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение вещественной (точной) позиции пришельца
        self.x = float(self.rect.x)

    def check_edges(self):
        """Если пришелец у края экрана возвращает True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update(self):
       '''Перемещает инопланетный флот'''
       self.x += (self.settings.alien_speed * self.settings.fleet_direction)
       self.rect.x = self.x