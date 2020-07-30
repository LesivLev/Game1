import random

import pygame

from const import WIDTH, HEIGHT, GREEN


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Определяем переменную как спрайт
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        tmp = random.randint(0, 4)
        if (tmp == 0):
            self.rect.centery = 10
            self.rect.centerx = random.randint(0, WIDTH)
        elif (tmp == 1):
            self.rect.centery = HEIGHT - 10
            self.rect.centerx = random.randint(0, WIDTH)
        elif (tmp == 2):
            self.rect.centery = random.randint(0, HEIGHT)
            self.rect.centerx = 10
        elif (tmp == 3):
            self.rect.centery = random.randint(0, HEIGHT)
            self.rect.centerx = WIDTH - 10
        self.speedx = 0
        self.speedy = 0
        self.hp = 20
        self.speed = 1

    def Hp(self):
        self.hp -= 10

    def update(self, player, text=""):
        if text == "regen":
            self.regenerate()
            return
        self.speedx = 0
        self.speedy = 0

        if (player.rect.x > self.rect.x):
            self.speedx = self.speed
        if (player.rect.x < self.rect.x):
            self.speedx = -self.speed
        if (player.rect.x == self.rect.x):
            self.speedx = 0
        if (player.rect.y > self.rect.y):
            self.speedy = self.speed
        if (player.rect.y < self.rect.y):
            self.speedy = -self.speed
        if (player.rect.y == self.rect.y):
            self.speedy = 0

        if text == "pauza":
            self.speedx = 0
            self.speedy = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def regenerate(self):
        # Обновить координаты, восполнить жизни
        tmp = random.randint(0, 4)
        if (tmp == 0):
            self.rect.centery = -10
            self.rect.centerx = random.randint(-10, WIDTH + 10)
        elif (tmp == 1):
            self.rect.centery = HEIGHT + 10
            self.rect.centerx = random.randint(-10, WIDTH + 10)
        elif (tmp == 2):
            self.rect.centery = random.randint(-10, HEIGHT + 10)
            self.rect.centerx = -10
        elif (tmp == 3):
            self.rect.centery = random.randint(-10, HEIGHT + 10)
            self.rect.centerx = WIDTH + 10
        self.hp = 20