import pygame

from classes.const import BLUE


class Dog(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Определяем переменную как спрайт
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 340
        self.rect.centery = 340

    def update(self, zombie):
        self.speedx = 0
        self.speedy = 0

        if zombie.rect.x > self.rect.x:
            self.speedx = 3
        if zombie.rect.x < self.rect.x:
            self.speedx = -3
        if (zombie.rect.x == self.rect.x):
            self.speedx = 0
        if (zombie.rect.y > self.rect.y):
            self.speedy = 3
        if (zombie.rect.y < self.rect.y):
            self.speedy = -3
        if (zombie.rect.y == self.rect.y):
            self.speedy = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy