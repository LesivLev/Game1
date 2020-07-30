import pygame

from const import WIDTH, HEIGHT, RED


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Определяем переменную как спрайт
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()  # Берем прямоугольник, который отвечает за спрайт
        # у rect есть centerx, centery - центр по оси X прямоугльника и центр по оси Y прямоугольника
        # у rect есть left, right, top, bottom - левая граница, правая граница, верхняя граница, нижняя граница
        # у rect есть x, y - координата по оси X и по оси Y
        self.rect.centery = HEIGHT / 2
        self.rect.centerx = WIDTH / 2
        self.hp = 100
        self.speedx = 0  # скокрость передвижения спрайта по оси X
        self.speedy = 0
        self.score = 0

    def update(self, keystate, text=""):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5

        if text == "pauza":
            self.speedx = 0
            self.speedy = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def hit(self):
        self.hp -= 1

    def hitwall(self, wall, keystate):
        bottomSideHit = (self.rect.right >= wall.rect.left and self.rect.right <= wall.rect.right) or (
                self.rect.left >= wall.rect.left and self.rect.left <= wall.rect.right) and self.rect.bottom <= wall.rect.bottom and self.rect.bottom >= wall.rect.top
        topSideHit = (self.rect.right >= wall.rect.left and self.rect.right <= wall.rect.right) or (
                self.rect.left >= wall.rect.left and self.rect.left <= wall.rect.right) and self.rect.top >= wall.rect.bottom and self.rect.top <= wall.rect.top
        leftSideHit = self.rect.left <= wall.rect.left and self.rect.left >= wall.rect.right and (
                self.rect.top >= wall.rect.bottom and self.rect.top <= wall.rect.top) or (
                              self.rect.bottom >= wall.rect.bottom and self.rect.bottom <= wall.rect.top)
        rightSideHit = self.rect.right >= wall.rect.left and self.rect.right <= wall.rect.right and (
                self.rect.top >= wall.rect.bottom and self.rect.top <= wall.rect.top) or (
                               self.rect.bottom >= wall.rect.bottom and self.rect.bottom <= wall.rect.top)

        # if(self.rect.right >= wall.rect.left and self.rect.right <= wall.rect.right and (self.rect.top >= wall.rect.bottom and self.rect.top <= wall.rect.top) or (self.rect.bottom >= wall.rect.bottom and self.rect.bottom <= wall.rect.top)):
        #    self.rect.right = wall.rect.left
        # elif(self.rect.left <= wall.rect.left and self.rect.left >= wall.rect.right and (self.rect.top >= wall.rect.bottom and self.rect.top <= wall.rect.top) or (self.rect.bottom >= wall.rect.bottom and self.rect.bottom <= wall.rect.top)):
        #    self.rect.left = wall.rect.right
        # elif((self.rect.right >= wall.rect.left and self.rect.right <= wall.rect.right) or (self.rect.left >= wall.rect.left and self.rect.left <= wall.rect.right) and self.rect.top >= wall.rect.bottom and self.rect.top <= wall.rect.top):
        #     self.rect.top = wall.rect.bottom
        # elif((self.rect.right >= wall.rect.left and self.rect.right <= wall.rect.right) or (self.rect.left >= wall.rect.left and self.rect.left <= wall.rect.right) and self.rect.bottom <= wall.rect.bottom and self.rect.bottom >= wall.rect.top):
        #     self.rect.bottom = wall.rect.top
        if (bottomSideHit):
            if keystate[pygame.K_DOWN]:
                self.speedy = 5
            self.rect.y -= self.speedy
        if (topSideHit):
            if keystate[pygame.K_UP]:
                self.speedy = 5
            self.rect.y -= self.speedy
        if (leftSideHit):
            if keystate[pygame.K_LEFT]:
                self.speedy = 5
            self.rect.x -= self.speedx
        if (rightSideHit):
            if keystate[pygame.K_RIGHT]:
                self.speedy = 5
            self.rect.x -= self.speedx