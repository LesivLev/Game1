import math

import pygame

from const import YELLOW


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.speedx = 0
        self.speedy = 0
        self.speed = 7

    def next_zombie(self, all_zombies):
        curr = 1000000
        answer = None
        for zombie in all_zombies:
            tmp = math.fabs(self.rect.centerx - zombie.rect.centerx) + math.fabs(
                self.rect.centery - zombie.rect.centery)
            if tmp < curr:
                answer = zombie
                curr = tmp
        return answer
        # a = math.fabs(self.rect.centerx - zombie1.rect.centerx) + math.fabs(self.rect.centery - zombie1.rect.centery)
        # b = math.fabs(self.rect.centerx - zombie2.rect.centerx) + math.fabs(self.rect.centery - zombie2.rect.centery)
        # c = math.fabs(self.rect.centerx - zombie3.rect.centerx) + math.fabs(self.rect.centery - zombie3.rect.centery)

        # if min(a, b, c) == c:
        #     return zombie3
        # if min(a, b, c) == b:
        #     return zombie2
        # if min(a, b, c) == a:
        #     return zombie1

    def update(self, text=""):
        self.zombie = self.next_zombie()
        if self.zombie.rect.centerx > self.rect.x:
            self.speedx = self.speed
        if self.zombie.rect.centerx < self.rect.x:
            self.speedx = -self.speed
        if self.zombie.rect.centerx == self.rect.x:
            self.speedx = 0
        if self.zombie.rect.centery > self.rect.y:
            self.speedy = self.speed
        if self.zombie.rect.centery < self.rect.y:
            self.speedy = -self.speed
        if self.zombie.rect.centery == self.rect.y:
            self.speedy = 0

        if text == "pauza":
            self.speedx = 0
            self.speedy = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy
