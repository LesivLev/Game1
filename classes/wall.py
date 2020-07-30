import pygame

from classes.const import WIDTH, HEIGHT, PURPLE


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 200))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 8
        self.rect.centery = HEIGHT // 2